import re

from changetext.corrector import CorrectorRegistry
from changetext.open_brackets import open_brackets
from changetext.replaced_parts import replaced_parts
from changetext.utils import (
    any_in_tag,
    custom_parse,
    filter_noun,
    get_gender,
    get_main_word_gender,
    inflect_adjective,
    inflect_as_adjective,
    inflect_collocation,
    inflect_noun,
    is_adjective,
    make_adjective,
    to_genitive_case,
    to_genitive_case_list,
    to_genitive_case_single_noun,
)

final_changes = CorrectorRegistry()

# Title eg. "Histories of Greed and Avarice" for the Linux version
histories_adjs = {
    "Greed": " жадности",
    "Avarice": "б алчности",
    "Jealousy": " зависти",
    "Cupidity": " скупости",
    "Gluttony": "б обжорстве",
    "Industry": "производстве",
    "Enterprise": "предприимчивости",
    "Resourcefulness": "находчивости",
    "Determination": "решительности",
    "Mettle": "отваге",
    "Dynamism": "стремительности",
    "Labor": "работе",
    "Toil": "труде",
    "Diligence": "усердии",
    "Exertion": "напряжении",
    "Tenacity": "стойкости",
    "Perseverance": "упорстве",
}


@final_changes.register(regex=r"Histories of (\w+) and (\w+)")
def corr_histories_of(_, search_result):
    return "Истории о{} и {}".format(histories_adjs[search_result.group(1)], histories_adjs[search_result.group(2)])


possessive_adjectives = {"жаба": "жабий", "корова": "коровий", "медведь": "медвежий"}

replace_containment = {
    "Семя": "семена",
    "Специи": "специй",
    "Самоцвет": "самоцветы",
    "Слиток/Блок": "слитков/блоков",
}

materials = {"волокон", "шёлка", "шерсти", "кожи"}

re_container = re.compile(r"(\b.+)\s(бочка|мешок|ящик)\s\((.*?)(\)|$)")


@final_changes.register(regex=re_container)
@open_brackets
def corr_container(text, _):
    """
    >>> corr_container('(дварфийское пиво бочка (из ольхи))')
    '(Бочка дварфийского пива (ольховая))'
    >>> corr_container("(дварфийское вино бочка (из клёна) <#8>)")
    '(Бочка дварфийского вина (кленовая) <#8>)'
    >>> corr_container("(Семя бочка (из лумбанга) <#10>)")
    '(Бочка семян (лумбанговая) <#10>)'
    """
    search_result = re_container.search(text)
    initial_string = search_result.group(0)
    containment = search_result.group(1)
    if containment in replace_containment:
        containment = replace_containment[containment]
    if containment.endswith("кровь"):
        words = containment.split()
        if words[0] in possessive_adjectives:
            words[0] = possessive_adjectives[words[0]]
            words = to_genitive_case_list(words)
        else:
            words = [to_genitive_case_single_noun(words[-1])] + list(to_genitive_case_list(words[:-1]))
        containment = " ".join(words)
    elif containment.startswith("из "):
        containment = containment[3:]  # Words after 'из' are already in genitive case
    elif containment in {"слитков/блоков", "специй"}:
        pass  # Already in genitive case
    elif containment.startswith("семена"):
        words = containment.split()
        words[0] = to_genitive_case(words[0])
        containment = " ".join(words)
    else:
        containment = to_genitive_case(containment)
    container = search_result.group(2)
    of_material = search_result.group(3)
    if not of_material:
        replacement_string = container + " " + containment
    elif (
        " " not in of_material
        and is_adjective(of_material)
        or of_material in make_adjective
        or of_material[3:] in make_adjective
    ):
        if " " not in of_material and is_adjective(of_material):
            adjective = of_material
        elif of_material in make_adjective:
            adjective = make_adjective[of_material]
        elif of_material[3:] in make_adjective:
            adjective = make_adjective[of_material[3:]]
        else:
            adjective = None
        gender = get_gender(container, {"nomn"})
        adjective = inflect_adjective(adjective, gender)
        replacement_string = "{} {} ({})".format(container, containment, adjective)
    else:
        words = of_material.split()
        material = None
        if of_material.startswith("из ") or len(of_material) <= 2:
            material = of_material
        elif (
            len(words) >= 2
            and words[-2] == "из"
            and (words[-1] in materials or any(mat.startswith(words[-1]) for mat in materials))
        ):
            # Try to fix truncated materail names, eg. '(ямный краситель мешок (гигантский пещерный паук из шёл'
            if words[-1] not in materials:  # Fix partial material name eg. 'шерст', 'шёлк'
                candidates = [mat for mat in materials if mat.startswith(words[-1])]
                if len(candidates) == 1:
                    words[-1] = candidates[0]
                else:
                    material = of_material  # Partial name is not recognized (too short)

            if not material:
                material = " ".join(words[-2:] + list(to_genitive_case_list(words[:-2])))
        else:
            gen_case = list(to_genitive_case_list(of_material.split()))
            if None not in gen_case:
                material = "из " + " ".join(gen_case)
            else:
                material = of_material
        replacement_string = "{} {} ({}".format(container, containment, material)
        if initial_string[-1] == ")":
            replacement_string += ")"
    text = text.replace(initial_string, replacement_string.capitalize())
    return text


re_of_material_item = re.compile(r"^[(+*-«☼р]*(из [\w\s\-/]+\b)")


@final_changes.register(predicate=lambda text: "пол" not in text and re_of_material_item.search(text))
@open_brackets
def corr_of_material_item(text, _):
    """
    >>> corr_of_material_item("риз алевролита мемориал")
    '≡алевролитовый мемориал'
    >>> corr_of_material_item("из алевролита доспешная стойка")
    'алевролитовая доспешная стойка'
    >>> corr_of_material_item("(из висмутовой бронзы короткие мечи [3])")
    '(короткие мечи из висмутовой бронзы [3])'
    >>> corr_of_material_item("риз берёзы гробр")
    '≡берёзовый гроб≡'
    """
    search_result = re_of_material_item.search(text)
    initial_string = search_result.group(1)
    words = initial_string.split()

    if len(words) == 2:
        parse = list(filter(lambda x: {"NOUN", "gent"} in x.tag, custom_parse(words[1])))
        assert len(parse) == 1
        replacement_string = parse[0].normal_form
    elif words[1] == "древесины":
        # Ultra simple case
        if "дерева" in words:  # 'из древесины миндального дерева'
            cut_index = words.index("дерева") + 1
        elif "пекан" in words:  # 'из древесины ореха пекан'
            cut_index = words.index("пекан") + 1
        elif any_in_tag({"NOUN", "gent"}, custom_parse(words[2])):  # 'из древесины яблони'
            cut_index = 3
        else:
            cut_index = -1
        replacement_string = " ".join(words[cut_index:] + words[:cut_index])
    elif all(any_in_tag({"ADJF", "gent"}, custom_parse(adj)) for adj in words[1:-1]) and any_in_tag(
        {"NOUN", "gent"}, custom_parse(words[-1])
    ):
        # All words after 'из' except the last word are adjectives in genitive
        # The last is a noun in genitive
        material = words[-1]
        gender = get_gender(material, known_tags={"gent"})
        parse = list(filter(lambda x: {"NOUN", "gent"} in x.tag, custom_parse(material)))
        material = parse[0].normal_form
        adjs = words[1:-1]
        adjs = [inflect_adjective(adj, gender, case="nomn") for adj in adjs]
        replacement_string = " ".join(adjs) + " " + material
    # elif (words[2] not in corr_item_general_except and len(words) > 3 and
    elif (
        len(words) > 3
        and any_in_tag({"gent"}, custom_parse(words[1]))
        and any_in_tag({"NOUN", "gent"}, custom_parse(words[2]))  # The second word is in genitive
    ):  # The third word is a noun in genitive
        # Complex case, eg. "из висмутовой бронзы"
        of_material = " ".join(words[:3])
        words = words[3:]
        if len(words) == 1:
            first_part = words[0]
        else:
            obj = words[-1]
            gender = get_gender(obj, "NOUN")
            adjs = (inflect_adjective(adj, gender) or adj for adj in words[:-1])
            first_part = "{} {}".format(" ".join(adjs), obj)
        replacement_string = first_part + " " + of_material
    elif any_in_tag({"NOUN", "gent"}, custom_parse(words[1])) and words[1] != "древесины":
        # Simple case, eg. "из бронзы"
        of_material = " ".join(words[:2])
        words = words[2:]
        item = words[-1]

        for word in words:
            if any_in_tag({"NOUN", "nomn"}, custom_parse(word)):
                item = word
                break

        if of_material in make_adjective:
            gender = get_gender(item, {"nomn"})

            if gender is None:
                for item in reversed(words[:-2]):
                    gender = get_gender(item)
                    if gender is not None:
                        break
            adjective = make_adjective[of_material]
            adjective = inflect_adjective(adjective, gender)
            # If there are another adjectives, ensure that they are in the correct gender:
            for i, word in enumerate(words):
                if is_adjective(word) and get_gender(word) != gender:
                    word = inflect_adjective(word, gender)
                    words[i] = word
            replacement_string = adjective + " " + " ".join(words)
        else:
            replacement_string = " ".join(words) + " " + of_material
    else:
        raise ValueError("Unknown case: {!r}".format(text))

    text = text.replace(initial_string, replacement_string)
    return text


re_clothes = re.compile(
    r"^[Xx\(+*-«☼]*((.+)\s"
    r"(из волокон"
    r"|из шёлка"
    r"|из шерсти"
    r"|из кожи"
    r"|из копыт"
    r"|из кости"
    r"|из рога"
    r"|из рогов"
    r"|из бивней"
    r"|из панциря"
    r"|из зубов)"
    r"\s(\w+\s?\w+))"
)


@final_changes.register(regex=re_clothes)
@open_brackets
def corr_clothes(text, _):
    """
    >>> corr_clothes("свинохвост из волокон ткань")
    'ткань из волокон свинохвоста'
    >>> corr_clothes("(-«пещерный паук из шёлка левый варежка»-)")
    '(-«левая варежка из шёлка пещерного паука»-)'
    >>> corr_clothes("(гигантский пещерный паук из шёлка шапка)")
    '(шапка из шёлка гигантского пещерного паука)'
    """
    search_result = re_clothes.search(text)
    text = text.replace(
        search_result.group(1),
        "{} {} {}".format(search_result.group(4), search_result.group(3), to_genitive_case(search_result.group(2))),
    )
    text = text.replace("левый", "левая")
    text = text.replace("правый", "правая")
    return text


@final_changes.register(regex=r"[\^\W]((приготовленные|рубленная)\s(.+)\s(\w+))")
def corr_prepared(text, search_result):
    """
    >>> corr_prepared(" приготовленные гигантский крот лёгкие")
    ' приготовленные лёгкие гигантского крота'
    >>> corr_prepared("(приготовленные северный олень почки [5])")
    '(приготовленные почки северного оленя [5])'
    >>> corr_prepared("(приготовленные панда лёгкие [5])")
    '(приготовленные лёгкие панды [5])'
    >>> corr_prepared("(рубленная гризли печень [5])")
    '(рубленная печень гризли [5])'
    """
    # TODO:
    # >>> corr_prepared("(приготовленный волк мозг [5])")
    # '(приготовленный мозг волка [5])'
    # >>> corr_prepared(" рубленная гигантский крот лёгкие")
    # ' рубленные лёгкие гигантского крота'
    groups = search_result.groups()
    result = text.replace(groups[0], "{} {} {}".format(groups[1], groups[3], to_genitive_case(groups[2])))
    return result


@final_changes.register(regex=r"(\(?)(.+)\s(из кожи|из шерсти)")
def corr_item_skin(text, search_result):
    """
    >>> corr_item_skin("горный козёл из кожи")
    'кожа горного козла'

    >>> corr_item_skin("альпака из шерсти")
    'шерсть альпака'
    """
    material = inflect_noun(search_result.group(3).split()[-1], "nomn")  # кожа, шерсть и т.д.
    text = text.replace(
        search_result.group(0), search_result.group(1) + material + " " + to_genitive_case(search_result.group(2))
    )
    return text


@final_changes.register(regex=r"(^Ковать|^Делать|^Чеканить|^Изготовить|^Кузница)\s(из\s[\w\s?]+\b)")
def corr_forge(_, search_result):
    """
    >>> corr_forge("Ковать из меди болты")
    'Ковать медные болты'
    >>> corr_forge("Кузница из железа Наконечники стрел баллисты")
    'Ковать железные наконечники стрел баллисты'
    >>> corr_forge("Делать из адамантина Колчан")
    'Делать адамантиновый колчан'
    """
    verb = search_result.group(1)
    words = search_result.group(2).split()
    assert len(words) >= 3

    assert words[0] == "из"
    # Second word ia adjective in gent case
    second_is_adjf_in_gent = any_in_tag({"ADJF", "gent"}, custom_parse(words[1]))
    # Third word is noun in gent case
    third_is_noun_in_gent = any_in_tag({"NOUN", "gent"}, custom_parse(words[2]))
    if second_is_adjf_in_gent and third_is_noun_in_gent:
        of_material = words[:3]
        obj = words[3:]
    else:
        # Second word is noun in gent case
        assert any_in_tag({"NOUN", "gent"}, custom_parse(words[1]))
        of_material = words[:2]
        obj = words[2:]

    of_material = " ".join(of_material)
    noun_index = None
    parse = None
    gender = None

    if len(obj) == 1:
        noun_index = 0
        parse = custom_parse(obj[noun_index])
        noun = filter_noun(parse)
        gender = get_gender(obj[noun_index], known_tags={"nomn"})
        if not any_in_tag({"accs"}, noun):
            obj[0] = noun[0].inflect({"accs"}).word
    else:
        for i, word in enumerate(obj):
            parse = custom_parse(word)
            noun = filter_noun(parse)
            if noun:
                noun_index = i
                gender = get_gender(obj[noun_index])
                obj[i] = noun[0].inflect({"accs"}).word
                break  # Words after the 'item' must be left in genitive case
            elif not any_in_tag("accs", parse):
                obj[i] = parse[0].inflect({"accs"}).word

    assert parse is not None
    if not any_in_tag("accs", parse):
        obj[noun_index] = parse[0].inflect({"accs"}).word

    if verb == "Кузница":
        verb = "Ковать"

    if of_material in make_adjective:
        assert gender is not None
        material = inflect_adjective(make_adjective[of_material], gender, "accs", animated=False)
        text = verb + " " + material + " " + " ".join(obj)
    else:
        text = verb + " " + " ".join(obj) + " " + of_material

    return text.capitalize()


@final_changes.register(
    regex=r"(шипованный|огромный|большой|заточенный|гигантский|большой зазубренный)\s(из\s[\w\s]+\b)"
)
def corr_weapon_trap_parts(text, search_result):
    """
    >>> corr_weapon_trap_parts('гигантский из меди лезвия топоров')
    'гигантские медные лезвия топоров'
    >>> corr_weapon_trap_parts('большой зазубренный из берёзы диски')
    'большие зазубренные берёзовые диски'
    """
    adj = search_result.group(1)
    words = search_result.group(2).split()
    if " ".join(words[:2]) in make_adjective:
        material = " ".join(words[:2])
        obj = " ".join(words[2:])
        gender = get_main_word_gender(obj)
        new_adj = inflect_as_adjective(adj, gender)
        new_word_2 = inflect_adjective(make_adjective[material], gender)
        text = text.replace(search_result.group(0), "{} {} {}".format(new_adj, new_word_2, obj))
    else:
        material = " ".join(words[:3])
        obj = " ".join(words[3:])
        gender = get_main_word_gender(obj)
        assert gender is not None
        new_adj = inflect_as_adjective(adj, gender)
        text = text.replace(search_result.group(0), "{} {} {}".format(new_adj, obj, material))
    return text


@final_changes.register(regex=r"(\bЛужа|Брызги|Пятно)\s(.+)\s(кровь\b)")
def corr_blood_stain(_text, search_result):
    """
    >>> corr_blood_stain("Лужа кот кровь")
    'Лужа крови кота'
    >>> corr_blood_stain("Пятно росомаха кровь")
    'Пятно крови росомахи'
    """
    text = search_result.group(1) + " " + to_genitive_case(search_result.group(3) + " " + search_result.group(2))
    return text.capitalize()


@final_changes.register(
    regex=r"(\(?)(.+)\s(\bяйцо|требуха|железы|железа|мясо|кровь|сукровица|кольца|серьги|амулеты"
    r"|браслеты|скипетры|короны|статуэтки\b)"
)
def corr_item_3(text, search_result):
    """
    >>> corr_item_3('рогатый филин яйцо')
    'яйцо рогатого филина'
    >>> corr_item_3("(киви мясо [5])")
    '(мясо киви [5])'
    >>> corr_item_3("(белый аист яйцо)")
    '(яйцо белого аиста)'
    """
    group_3 = search_result.group(3)
    if group_3 in replaced_parts:
        group_3 = replaced_parts[group_3]

    if search_result.group(2) in make_adjective:
        group_2 = make_adjective[search_result.group(2)]
    else:
        group_2 = to_genitive_case(search_result.group(2))

    text = text.replace(search_result.group(0), search_result.group(1) + group_3 + " " + group_2)

    return text


@final_changes.register(regex=r"(древесина)\s(\w+)\s(брёвна)")
def corr_wooden_logs(text, search_result):
    """
    >>> corr_wooden_logs('древесина дуба брёвна')
    'дубовые брёвна'
    """
    of_wood = "из " + search_result.group(2)
    if of_wood in make_adjective:
        adj = inflect_adjective(make_adjective[of_wood], "plur")
        text = text.replace(search_result.group(0), adj + " " + search_result.group(3))  # берёзовые брёвна
    else:
        text = text.replace(
            search_result.group(0), search_result.group(1) + " " + search_result.group(2)
        )  # древесина акации
    return text


@final_changes.register(regex=r"\b(Делать|Изготовить)\s([\w\s]*)(стекло|хрусталь)([\w\s]*)")
def corr_craft_glass(text, search_result):  # TODO: Combine into single crafting-related function
    """
    >>> corr_craft_glass("Делать грубый зелёное стекло")
    'Варить грубое зелёное стекло'
    >>> corr_craft_glass("Делать гигантский хрусталь лезвие топора")
    'Делать гигантское лезвие топора из хрусталя'
    """
    material = search_result.group(3)
    material_gender = get_gender(material)
    words = search_result.group(2).split()
    product = search_result.group(4).split()
    verb = search_result.group(1)
    if not product:
        verb = "Варить"
        adjectives = (inflect_adjective(adj, material_gender, "accs", animated=False) for adj in words)
        result = "{} {} {}".format(verb, " ".join(adjectives), material)
    else:
        index = next(
            (i for i, item in enumerate(words) if item in {"грубое", "зелёное", "прозрачное", "грубый"}), len(words)
        )
        product_adjectives = words[:index]
        if any_in_tag({"NOUN", "nomn"}, custom_parse(product[0])):
            product_gender = get_gender(product[0])
            product[0] = inflect_noun(product[0], case="accs")
        else:
            product_gender = get_gender(product[-1])
            product_adjectives += product[:-1]
            product = [inflect_noun(product[-1], case="accs")]

        product_adjectives = [
            inflect_adjective(adj, product_gender, case="accs", animated=False) for adj in product_adjectives
        ]
        material_adjectives = [
            inflect_adjective(adj, material_gender, case="gent", animated=False) for adj in words[index:]
        ]

        material = inflect_noun(material, case="gent")
        product_words = product_adjectives + product
        material_words = material_adjectives + [material]
        result = "{} {} из {}".format(verb, " ".join(product_words), " ".join(material_words))

    return text.replace(search_result.group(0), result)


animals_female = {
    "собака",
    "самка",
    "крольчиха",
    "гусыня",
    "утка",
    "кошка",
    "ослица",
    "кобыла",
    "корова",
    "овца",
    "свинья",
    "коза",
    "курица",
    "свинка",
    "буйволица",
    "важенка",
    "лама",
    "альпака",
    "цесарка",
    "пава",
    "индейка",
}

body_parts = {
    "панцирь",
    "скелет",
    "искалеченный труп",
    "останки",
    "кость",
    "кожа",
    "шёлк",
    "волокна",
    "шерсть",
    "мех",
    "хвост",
}


@final_changes.register(regex=r"((бриолетовый|большой|огранённый|грубый)\s[\w\s-]+)")
def corr_gem_cutting(text, search_result):
    """
    >>> corr_gem_cutting("(бриолетовый восковые опалы)")
    '(бриолетовые восковые опалы)'
    >>> corr_gem_cutting("большой шерлы")
    'большие шерлы'
    """
    words = search_result.group(1).split()
    if words[-1] in body_parts:
        return corr_item_body_parts(text)

    gender = get_gender(words[-1], {"NOUN", "nomn"})

    new_list = []
    for word in words[:-1]:
        if word in make_adjective:
            adj = make_adjective[word]
            word = inflect_adjective(adj, gender)
        elif is_adjective(word):
            word = inflect_adjective(word, gender)
        new_list.append(word)

    new_list.append(words[-1])

    return text.replace(search_result.group(0), " ".join(new_list))


@final_changes.register(regex=r"(охотничий|боевой|сырой) (\w+)(\(Ручной\))?")
def corr_animal(text, _):
    """
    >>> corr_animal("охотничий собака, ♀")
    'охотничья собака, ♀'
    >>> corr_animal("Ничей боевой собака, ♀(Ручной)")
    'Ничья боевая собака, ♀(Ручная)'
    """

    text = text.replace("сырой", "сырая")
    if any(item in text for item in animals_female):
        text = text.replace("(Ручной)", "(Ручная)")
        text = text.replace("боевой", "боевая")
        text = text.replace("Ничей", "Ничья")
        text = text.replace("охотничий", "охотничья")

    return text


@final_changes.register(regex=r"(\w+) приостановили строительство (.*)\.")
def corr_stopped_construction(_, search_result):
    """
    >>> corr_stopped_construction(" дварфы приостановили строительство Стена.")
    'Дварфы приостановили строительство стены.'
    >>> corr_stopped_construction(" дварфы приостановили строительство Ремесленник мастерская.")
    'Дварфы приостановили строительство мастерской ремесленника.'
    >>> corr_stopped_construction(" дварфы приостановили строительство Ювелирная мастерская.")
    'Дварфы приостановили строительство ювелирной мастерской.'
    """
    subj = search_result.group(1)
    obj = search_result.group(2)

    if "Ремесленник мастерская" in obj:
        gen_case_obj = " ".join(
            to_genitive_case(word) for word in reversed(obj.split())
        )  # Put words into genitive case separately
    else:
        gen_case_obj = to_genitive_case(obj)

    return ("{} приостановили строительство {}.".format(subj, gen_case_obj)).capitalize()


@final_changes.register(
    regex=r"(.+)\s(Подъем|Стена|Кластер|валун|склон|Пол Пещеры|лестница вверх/вниз|пол пещеры|"
    r"Лестница Вверх|Лестница Вниз|галька|деревце|лестница вверх|лестница вниз|подъем|пол)\b"
)
def corr_relief(_, search_result):
    """
    >>> corr_relief("Мёртвый клён деревце")
    'Мёртвое деревце (клён)'
    >>> corr_relief("Глинистый суглинок Стена")
    'Стена из глинистого суглинка'
    >>> corr_relief("кремень подъем")
    'Подъем из кремня'
    """

    group1 = search_result.group(1)
    obj = search_result.group(2)
    if obj == "деревце":
        if group1.split(" ")[0] == "Мёртвый":
            text = "Мёртвое деревце ({})".format("".join(search_result.group(0).split(" ")[1:-1]))
        else:
            text = "Деревце ({})".format(group1)
        return text.capitalize()

    if " " in group1:
        words = group1.split(" ")
        first_words = []
        gender = get_main_word_gender(obj)

        for word in words:
            if word in {"Заснеженный", "Неотесанный", "Влажный"}:
                if gender is not None:
                    new_word = inflect_adjective(word, gender)
                    if not new_word:
                        new_word = word
                else:
                    new_word = word
                first_words.append(new_word)
            else:
                break

        words = words[len(first_words) :]

        if words[0] == "из":
            words = words[1:]
        else:
            words = to_genitive_case_list(words)

        if not first_words:
            text = "{} из {}".format(obj, " ".join(words))
        else:
            text = "{} {} из {}".format(" ".join(first_words), obj, " ".join(words))
    else:
        material = group1
        text = "{} из {}".format(obj, to_genitive_case(material))

    if "иза" in text:
        text = text.replace(" иза", "")
    return text.capitalize()


@final_changes.register(regex=re.compile(r"\b(Густой|Редкий|Заснеженный)\s(.+)"))
def corr_adjective_relief(text, search_result):
    """
    >>> corr_adjective_relief("Заснеженный Густой овсяница")
    'Заснеженная густая овсяница'
    >>> corr_adjective_relief("Густой мюленбергия")
    'Густая мюленбергия'
    >>> corr_adjective_relief("Густой морошка")
    'Густая морошка'
    >>> corr_adjective_relief("Заснеженный Густой куропаточья трава")
    'Заснеженная густая куропаточья трава'
    """
    adjective = search_result.group(1)
    obj = search_result.group(2)

    if " " in obj:
        words = obj.split(" ")
        if is_adjective(words[0]):
            gender = get_gender(words[-1])
            new_word = inflect_adjective(words[0], gender, "nomn")
            text = text.replace(words[0], new_word)
            new_word = inflect_adjective(adjective, gender, "nomn")
            text = text.replace(adjective, new_word)
    else:
        gender = get_gender(obj)
        new_word = inflect_adjective(adjective, gender, "nomn")
        if new_word:
            text = "{} {}".format(new_word, obj)

    return text.capitalize()


@final_changes.register(
    regex=r"^(Инкрустировать Готовые товары с"
    r"|Инкрустировать Предметы обстановки с"
    r"|Инкрустировать Снаряды с"
    r"|Огранить)\s(.+)"
)
def corr_jewelers_shop(_, search_result):
    """
    >>> corr_jewelers_shop("Огранить из необработанного адамантина")
    'Огранить необработанный адамантин'
    >>> corr_jewelers_shop("Инкрустировать Предметы обстановки с из необработанного адамантина")
    'Инкрустировать предметы обстановки необработанным адамантином'
    >>> corr_jewelers_shop("Огранить из фарфора")
    'Огранить фарфор'
    """

    first_part = search_result.group(1)
    words = search_result.group(2).split()
    if first_part == "Огранить":
        # accusative case
        tags = None
        if words[0] == "из":
            words = words[1:]
            tags = {"gent"}
        item = words[-1]
        gender = get_gender(item, known_tags=tags)
        words = [inflect_adjective(word, gender, "accs", animated=False) for word in words[:-1]]
        parse = list(filter(lambda x: {gender, "inan"} in x.tag, custom_parse(item)))
        if item == "адамантина":
            item = "адамантин"
        else:
            item = parse[0].inflect({"accs"}).word
        words.append(item)
    else:
        # instrumental/ablative case ('incrust with smth')
        words = [custom_parse(word)[0].inflect({"ablt"}).word for word in words if word != "из"]

    if first_part.endswith(" с"):
        first_part = first_part[:-2]
    text = first_part + " " + " ".join(words)
    return text.capitalize()


@final_changes.register(regex=r"(.*)\s(лесное убежище|крепость|селение|горный город|городок|гробница|пригорки)\s(.+)")
def corr_settlement(_, search_result):
    """
    >>> corr_settlement(" человеческий крепость Belrokalle")
    'Человеческая крепость Belrokalle'
    >>> corr_settlement(" эльфийский лесное убежище Etathuatha")
    'Эльфийское лесное убежище Etathuatha'
    >>> corr_settlement(" дварфийский горный город КилрудОстач")
    'Дварфийский горный город Килрудостач'
    >>> corr_settlement(" лесное убежище Cinilidisa")
    'Лесное убежище Cinilidisa'
    """
    adjective = search_result.group(1).strip()
    settlement = search_result.group(2)
    name = search_result.group(3)

    if len(adjective) == 0:
        return "{} {}".format(settlement.capitalize(), name.capitalize())

    if adjective in {"Покинуть", "Разрушить"}:
        return

    gender = get_main_word_gender(settlement)

    if " " not in adjective:
        adjective_2 = inflect_adjective(adjective, gender)
    else:
        adjective_2 = " ".join(inflect_adjective(word, gender) for word in adjective.split(" "))

    if adjective_2 is None:
        adjective_2 = adjective

    return "{} {} {}".format(adjective_2.capitalize(), settlement, name.capitalize())


# Clothier's shop
cloth_subst = {
    "ткань": ("Шить", "из ткани"),
    "шёлк": ("Шить", "шёлковый"),
    "пряжа": ("Вязать", "из пряжи"),
    "кожа": ("Шить", "из кожи"),
}


@final_changes.register(regex=r"(Делать|Изготовить|Вышивать|Ткать) (ткань|шёлк|пряжа|кожа)(\s?\w*)")
def corr_clothiers_shop(_, search_result):
    """
    >>> corr_clothiers_shop("Делать ткань роба")
    'Шить робу из ткани'
    >>> corr_clothiers_shop("Делать шёлк роба")
    'Шить шёлковую робу'
    >>> corr_clothiers_shop("Изготовить ткань мешок")
    'Шить мешок из ткани'
    >>> corr_clothiers_shop("Вышивать кожа изображение")
    'Вышивать изображение на коже'
    >>> corr_clothiers_shop("Делать пряжа рубаха")
    'Вязать рубаху из пряжи'
    >>> corr_clothiers_shop("Делать ткань верёвка")
    'Вить верёвку из ткани'
    """
    verb = search_result.group(1)
    material = search_result.group(2)
    product = search_result.group(3).strip()

    if not product:
        return None  # Leave as is eg. 'Ткать шёлк'
    elif verb == "Вышивать":  # Sew
        if material == "пряжа":
            # вязать <product> из пряжи
            verb, preposition, material = "Вязать", "из", "пряжи"
        else:
            # вышивать <product> на <material>
            preposition = "на"
            material = inflect_noun(material, case="loct", orig_form={"nomn"})

        return "{} {} {} {}".format(verb, product, preposition, material)
    else:
        if product in {"щит", "баклер"}:
            _, of_material = cloth_subst[material]  # Don't change the verb, leave 'Делать'/'Изготовить'
        else:
            verb, of_material = cloth_subst[material]

        if product == "верёвка":
            verb = "Вить"

        product_accus = inflect_noun(product, case="accs", orig_form={"nomn"})

        if material in make_adjective:  # "шёлк" -> "шёлковый"
            gender = get_gender(product, {"nomn"})
            material_adj = inflect_adjective(make_adjective[material], gender, "accs", animated=False)
            return "{} {} {}".format(verb, material_adj, product_accus)  # {Шить} {шёлковую} {робу}
        else:
            return "{} {} {}".format(verb, product_accus, of_material)  # {Шить} {робу} {из ткани}


@final_changes.register(regex=r"(Делать|Изготовить|Украшать)([\w\s/]+)$")
def corr_craft_general(text, search_result):
    """
    >>> corr_craft_general("Изготовить камень дверь")
    'Изготовить каменную дверь'
    >>> corr_craft_general("Делать деревянный ловушка для животных")
    'Делать деревянную ловушку для животных'
    >>> corr_craft_general("Украшать кость")
    'Украшать кость'
    >>> corr_craft_general("Делать деревянный изделия")
    'Делать деревянные изделия'
    """
    verb = search_result.group(1)
    words = search_result.group(2).split()
    product = None
    if len(words) > 1:
        for i, word in enumerate(words[1:], 1):
            if any_in_tag({"NOUN", "nomn"}, custom_parse(word)) and word not in make_adjective:
                product = " ".join(words[i:])
                words = words[:i]
                break
    else:
        product = words[0]
        words = []

    product_gender = get_main_word_gender(product)

    if " " not in product:
        orig_form = {"plur" if product_gender == "plur" else "sing", "inan"}
        product = inflect_noun(product, "accs", orig_form=orig_form)
        assert product is not None
    else:
        product = inflect_collocation(product, {"accs"})

    if words:
        if len(words) == 1 and words[0] not in make_adjective and not is_adjective(words[0]):
            material = inflect_noun(words[0], "gent", orig_form={"nomn", "inan"})  # рог -> (из) рога
            assert material is not None
            result = "{} {} из {}".format(verb, product, material)
        else:
            adjectives = [
                make_adjective[word] if word in make_adjective else word if is_adjective(word) else None
                for word in words
            ]
            assert all(adj is not None for adj in adjectives)
            adjectives = [inflect_adjective(adj, product_gender, "accs", animated=False) for adj in adjectives]
            result = "{} {} {}".format(verb, " ".join(adjectives), product)
    else:
        result = "{} {}".format(verb, product)

    return text.replace(search_result.group(0), result).capitalize()


@final_changes.register(
    regex=r"^{?((\w+\s?\w+?|)\s" r"(панцирь|скелет|труп|останки|кость|кожа|шёлк|волокна|шерсть|мех|хвост|голень))}?\b"
)
def corr_item_body_parts(text, search_result):
    """
    >>> corr_item_body_parts("{крыса останки}")
    '{Останки крысы}'
    >>> corr_item_body_parts("мотылёк останки")
    'Останки мотылька'
    >>> corr_item_body_parts("кеа труп")
    'Труп кеа'
    >>> corr_item_body_parts("{сипуха голень}")
    '{Голень сипухи}'
    """
    initial_string = search_result.group(1)
    words = search_result.group(2).split()
    if words[-1] in {"частичный", "искалеченный"}:
        replacement_string = "{} {} {}".format(
            words[-1],
            search_result.group(3),
            " ".join(to_genitive_case_list(words[:-1])),
        )
    else:
        if any("GRND" in custom_parse(word)[0].tag for word in words):  # Ignore participles
            return None
        replacement_string = search_result.group(3) + " " + " ".join(to_genitive_case_list(words))
    return text.replace(initial_string, replacement_string.capitalize())


@final_changes.register(regex=r"(.+)\s(кожа|кость|волокно|шёлк)\b")
def corr_animal_material(_, search_result):
    """
    >>> corr_animal_material("гигантская летучая мышь кожа")
    'кожа гигантской летучей мыши'
    >>> corr_animal_material("гигантский белый аист кожа")
    'кожа гигантского белого аиста'
    """
    return search_result.group(2) + " " + to_genitive_case(search_result.group(1))


@final_changes.register(regex=r"([\w\s]+) (кольцо|кольца)")
def corr_rings(text, search_result):
    obj = search_result.group(2)
    description = search_result.group(1)
    return text.replace(search_result.group(0), "{} из {}".format(obj, to_genitive_case(description)))


@final_changes.register(predicate=lambda text: text.startswith("Вы нашли из "))
def corr_you_struck(text, _):
    """
    >>> corr_you_struck('Вы нашли из пиролюзита!')
    'Вы нашли пиролюзит!'
    >>> corr_you_struck('Вы нашли из каменного угля!')
    'Вы нашли каменный уголь!'
    """
    text = text.rstrip("!")
    you_struck, of, material = text.partition(" из ")

    words = material.split()
    assert len(words) >= 1
    if len(words) == 1:
        result = inflect_noun(words[0], "accs")
    else:
        result = inflect_collocation(material, {"accs"})

    return "{} {}!".format(you_struck, result)


@final_changes.register(regex=r"(.+)\s(стал)\s(.+)\.")
def corr_become(_, search_result):
    """
    >>> corr_become("Udil Vuthiltobul стал рекрут.")
    'Udil Vuthiltobul стал рекрутом.'
    >>> corr_become("Udil Vuthiltobul стал рыбник.")
    'Udil Vuthiltobul стал рыбником.'
    >>> corr_become("`***CLOTH' Rovodokir стал портной.")
    "`***CLOTH' Rovodokir стал портным."
    >>> corr_become("Животное вырос и стал Ничей козёл.")
    'Животное выросло и стало ничьим козлом.'
    >>> corr_become("Животное вырос и стал Ничей важенка.")
    'Животное выросло и стало ничьей важенкой.'
    """
    subj = search_result.group(1)
    verb = search_result.group(2)
    words = search_result.group(3)
    words = inflect_collocation(words, {"ablt"})
    if subj.startswith("Животное"):
        return "Животное выросло и стало {}.".format(words)
    else:
        return "{} {} {}.".format(subj, verb, words)
