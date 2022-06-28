import re
import traceback

from changetext.common_state import get_state
from changetext.corrector import CorrectorRegistry
from changetext.replaced_parts import replaced_parts
from changetext.tag_correction import corr_tags, parse_tags
from changetext.utils import custom_parse, inflect_collocation
from changetext.whole_phrases import whole_phrases

preliminary_changes = CorrectorRegistry()


@preliminary_changes.register(predicate=lambda _: get_state().prev_tail)
def add_prev_tail(text, prev_tail):
    text = prev_tail + text
    get_state().prev_tail = ""
    return text


@preliminary_changes.register(predicate=lambda text: text in whole_phrases)
def corr_whole_phrases(text, _):
    return whole_phrases[text]


# Корректировка для окончания s - перевод существительного во множественное число или глагола в 3-е лицо ед.ч.
re_ending_s = re.compile(r"(\d+\s)?([а-яёА-ЯЁ][а-яёА-ЯЁ\s]*)e?s\b")


def corr_ending_s_internal(text):
    parse = [x for x in custom_parse(text) if {"NOUN", "nomn", "sing"} in x.tag or {"VERB", "2per"} in x.tag]

    if not parse:
        # Cannot determine part of speech
        return None

    new_forms = set()

    if parse[0].tag.POS == "NOUN":
        new_forms.add(parse[0].inflect({"plur"}).word)
    else:  # parse[0].tag.POS == 'VERB':
        new_forms.add(parse[0].inflect({"3per", "sing"}).word)

    if len(new_forms) > 1:
        # Cannot determine part of speech because of ambiguity
        return None

    return new_forms.pop()


dict_ending_s = {
    "готовая еда": "готовая еда",
    "питьё": "питьё",
    "стул": "стулья",
    "доспешная стойка": "доспешные стойки",
    "оружейная стойка": "оружейные стойки",
    "дублёная шкура": "дублёные шкуры",
    "большой самоцвет": "большие самоцветы",
    "баклер": "баклеры",
    "оружие": "оружие",
    "крышка люка": "крышки люка",
    "ручная мельница": "ручные мельницы",
    "ловушка для животных": "ловушки для животных",
    "часть ловушки": "части ловушек",
    "музыкальный инструмент": "музыкальные инструменты",
    "наконечник стрелы баллисты": "наконечники стрелы баллисты",
    "часть тела": "части тела",
    "конечность/тело гипс": "гипс для конечностей тела",
    "Элитный борец": "Элитные борцы",
    "Лорд топора": "Лорды топора",
    "Лорд булавы": "Лорды булавы",
    "Лорд молота": "Лорды молота",
    "Мастер меча": "Мастера меча",
    "Мастер копья": "Мастера копья",
}


def corr_ending_s(text):
    """
    >>> corr_ending_s("трупs [2]")
    'трупы [2]'
    """
    search_result = re_ending_s.search(text)
    number = search_result.group(1)
    group2 = search_result.group(2)
    if number and " " not in group2:
        number = int(number)
        parse = [x for x in custom_parse(group2) if {"NOUN", "nomn", "sing"} in x.tag]
        assert len(parse) == 1
        replacement_string = "{:d} {}".format(number, parse[0].make_agree_with_number(number).word)
    elif group2 in dict_ending_s:
        replacement_string = dict_ending_s[group2]
    elif " " not in group2:
        new_form = corr_ending_s_internal(group2)
        if new_form:
            replacement_string = new_form
        else:
            return None
    else:
        words = group2.split()
        if words[-1] in dict_ending_s:
            words[-1] = dict_ending_s[words[-1]]
            replacement_string = " ".join(words)
        else:
            new_form = corr_ending_s_internal(words[-1])
            if new_form:
                words[-1] = new_form
                replacement_string = " ".join(words)
            else:
                return None

    return text.replace(search_result.group(0), replacement_string)


@preliminary_changes.register(regex=re_ending_s)
def corr_ending_s_loop(text, _search_result):
    """
    >>> corr_ending_s_loop("трупs [2]")
    'трупы [2]'
    >>> corr_ending_s_loop("из красного дерева щитs/баклерs")
    'из красного дерева щиты/баклеры'
    >>> corr_ending_s_loop("коза из копыт кольцоs")
    'коза из копыт кольца'
    """
    result = text
    while re_ending_s.search(text):
        s1 = corr_ending_s(text)
        if s1 is None:
            break
        text = s1
        result = text
    return result


@preliminary_changes.register(regex=r"были(\w+)")
def corr_werebeast(text, search_result):
    """
    >>> corr_werebeast("Ura Wuspinicen, былимуравьед")
    'Ura Wuspinicen, муравьед-оборотень'
    >>> corr_werebeast(" былимуравьед крепко держится!")
    ' муравьед-оборотень крепко держится!'
    """
    return text.replace(search_result.group(0), search_result.group(1) + "-оборотень")


@preliminary_changes.register(regex=r"с (его|её|ваш) ([\w\s]*)")
def corr_with_his(text, search_result):
    """
    >>> corr_with_his("ладонь с его левое предплечье!")
    'ладонь своим левым предплечьем!'
    >>> corr_with_his("ладонь с ваш левое предплечье!")
    'ладонь своим левым предплечьем!'
    """
    return text.replace(
        search_result.group(0), "своим {}".format(inflect_collocation(search_result.group(2), {"ablt"}))
    )


@preliminary_changes.register(predicate=lambda text: "Я " in text and "колодец" in text)
def corr_well(text, _):
    """
    >>> corr_well('Я колодец')  # I am well
    'Я в порядке'
    >>> corr_well('Я чувствую колодец')  # I am feeling well
    'Я чувствую себя хорошо'
    >>> corr_well('"Я чувствую колодец"')
    '"Я чувствую себя хорошо"'
    """
    text = text.replace("колодец", "хорошо")
    if "чувствую" in text and "себя" not in text:
        text = text.replace("чувствую", "чувствую себя")
    elif "делаю хорошо" in text:
        text = text.replace("делаю хорошо", "в порядке")
    elif "был хорошо" in text:
        text = text.replace("был хорошо", "в порядке")
    elif "хорошо" in text:
        text = text.replace("хорошо", "в порядке")
    return text


@preliminary_changes.register(predicate=lambda text: "рублены" in text and "рубленый " not in text)
def corr_minced(text, _):
    s1 = ""
    while "рублены" in text and "рубленый" not in text:
        x, _, text = text.partition("рублены")
        s1 += x + "рубленый "

    return s1 + text


@preliminary_changes.register(predicate=lambda text: any(item in text for item in replaced_parts))
def corr_replace_parts(text, _):
    """
    >>> corr_replace_parts("Ремесленникство")
    'мастерство'
    >>> corr_replace_parts("Ремесленник мастерская")
    'Мастерская ремесленника'
    """
    result = text

    for item in replaced_parts:
        if item in text:
            text = text.replace(item, replaced_parts[item])
            result = text

    return result


@preliminary_changes.register(regex=r"[a-z](в <[a-z]+>)")
def corr_in_ending(text, search_result):
    """
    >>> corr_in_ending('Golololв <accs>, "Golololв <accs>", ')
    'Golololin, "Golololin", '
    """
    return text.replace(search_result.group(1), "in")


animal_genders = {"собака": ("пёс", "собака"), "кошка": ("кот", "кошка"), "лошадь": ("конь", "лошадь")}


@preliminary_changes.register(regex=r"(\w+), ([♂♀])")
def corr_animal_gender(text, search_result):
    """
    >>> corr_animal_gender("охотничий собака, ♀")
    'охотничий собака, ♀'
    >>> corr_animal_gender("охотничий собака, ♂")
    'охотничий пёс, ♂'
    >>> corr_animal_gender("Ничей боевой собака, ♀(Ручной)")
    'Ничей боевой собака, ♀(Ручной)'
    """
    gender = "♂♀".index(search_result.group(2))
    animal = search_result.group(1)
    if animal not in animal_genders:
        return None
    else:
        return text.replace(search_result.group(0), animal_genders[animal][gender] + ", " + search_result.group(2))


@preliminary_changes.register(regex=re.compile(r"(он|она|вы)\s+(не\s+)?(имеете?)", flags=re.IGNORECASE))
def corr_someone_has(text, search_result):
    """
    >>> corr_someone_has("Она   имеет")
    'У неё'
    >>> corr_someone_has("он     имеет")
    'у него'
    >>> corr_someone_has("Вы не имеете")
    'У вас нет'
    """
    pronoun = search_result.group(1).lower()
    if pronoun == "он":
        replacement_string = "у него"
    elif pronoun == "она":
        replacement_string = "у неё"
    elif pronoun == "вы":
        replacement_string = "у вас"
    else:
        return text

    if search_result.group(0)[0].isupper():
        replacement_string = replacement_string.capitalize()

    if search_result.group(2):
        replacement_string += " нет"

    text = text.replace(search_result.group(0), replacement_string)
    assert isinstance(text, str), text
    return text


@preliminary_changes.register(regex=r"(имеете?|был)\s+(\w+)")
def corr_has_verb(text, search_result):
    """
    >>> corr_has_verb(" имеет создал ")
    ' создал '
    >>> corr_has_verb(" был создал ")
    ' создал '
    >>> corr_has_verb(" был создать ")
    ' создал '
    >>> corr_has_verb(" имеет пришёл ")
    ' пришёл '
    >>> corr_has_verb(" имеет упал ")
    ' упал '
    >>> corr_has_verb(" имеет стрямкал ")
    ' стрямкал '
    """
    if search_result:
        word = search_result.group(2)
        parse = [p for p in custom_parse(word) if p.tag.POS in ("VERB", "INFN")]
        if parse:
            if not any({"past"} in p.tag for p in parse):
                word = parse[0].inflect({"VERB", "past", "sing"}).word
            return text.replace(search_result.group(0), word)


@preliminary_changes.register(regex=r"цвет ([\w\s]*)цвета")
def corr_color_of_color(text, search_result):
    """
    >>> corr_color_of_color("цвет серебристого цвета")
    'серебристый цвет'
    >>> corr_color_of_color("цвет цвета морской волны")
    'цвет морской волны'
    """
    if search_result:
        if not search_result.group(1):
            replacement = "цвет"
        else:
            color = search_result.group(1).strip()
            replacement = "{} цвет".format(inflect_collocation(color, {"nomn", "masc"}))
        return text.replace(search_result.group(0), replacement)


@preliminary_changes.register(
    predicate=lambda text: "<" in text and ">" in text and "<нет " not in text and "<#" not in text
)
def corr_tags_outer(text, _):
    try:
        result = corr_tags(text)
    except (AssertionError, ValueError) as err:
        print("corr_tags() raises exception {!r}:".format(err))
        print(traceback.format_exc())
        result = " ".join(
            part.strip(" ") if not part.startswith("<") else part.strip("<>").partition(":")[2]
            for part in parse_tags(text)
        )
    return result
