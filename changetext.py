import functools
import sys
import re
import traceback
import pymorphy2

from collections import OrderedDict

morph = pymorphy2.MorphAnalyzer()

unwanted_tags = ('Name', 'Surn', 'Infr')


def custom_parse(text):
    if text.lower().startswith('адамантин'):
        return morph.parse(text)  # Pymorphy2 thinks that adamantine is a surname and treats it properly
    else:
        return [p for p in morph.parse(text) if all(tag not in p.tag for tag in unwanted_tags)]


phrases = {
    'Slaves to Armok:  God of Blood': 'Рабы Армока - бога крови',
    'Chapter II: Dwarf Fortress': 'Глава II: Крепость дварфов',
    'Жмите ': 'Нажмите ',
    'прокрутка': 'для прокрутки',
    'Programmed by Tarn Adams': 'Программирование - Тарн Адамс',
    'Designed by Tarn and Zach Adams': 'Дизайн - Тарн Адамс и Зак Адамс',
    'Visit Bay 12 Games': 'Посетите Bay 12 Games',

    'Welcome to the alpha of Dwarf Fortress.':
        'Добро пожаловать в альфа-версию Dwarf Fortress.',
    'As there has been some time between releases, instability is to be expected.':
        'Поскольку между релизами прошло некоторое время, возможна нестабильность.',
    'Report crashes, hangs, lags, bugs and general disappointment at the forums.':
        'Сообщайте о вылетах, зависаниях, тормозах, багах и прочем на форумах',
    'They are at our website, bay12games.com.  Check there for updates.':
        'на нашем вебсайте bay12games.com.  Следите за обновлениями.',
    'You can also find an older yet more stable version of the game there.':
        'Там же вы можете найти более старые и стабильные версии игры.',

    # TODO: make independent to the year number
    'As of June 2012, you can get help at the fan-created dwarffortresswiki.org.':
        'Кроме того, вы можете получить помощь на dwarffortresswiki.org.',

    'Please make use of and contribute to this valuable resource.':
        'Пожалуйста, пользуйтесь и вносите свой вклад в этот ценный ресурс.',
    'If you enjoy the game, please consider supporting Bay 12 Games.':
        'Если игра вам понравилась, подумайте над тем, чтобы поддержать Bay 12 Games.',
    'There is more information at our web site and in the readme file.':
        'Дополнительную информацию вы можете получить на нашем веб сайте и в файле readme.',

    'Dwarf Fortress': 'Крепость дварфов',
    'Adventurer': 'Приключение',
    'Legends': 'Легенды',

    # реагенты
    'сырой рыба': 'свежая рыба',

    'Ничего не ловится в центре  болотах.': 'Ничего не ловится в центральных болотах.',
    'Ничего не ловится в востоке болотах.': 'Ничего не ловится в восточных болотах.',

    'NEW': 'НОВОЕ',
}

replaced_parts = OrderedDict([
    ("Ремесленникство", "мастерство"),
    ("ремесленникство", "мастерство"),
    ("предложить вашей мастерство", "предложить Вашей Мастеровитости"),
    ("FIRED_MAT-образующий", ""),
    ("FIRED_MAT", "обожжённый"),
    ("TALLOW SOAP_MAT-образующий", "мылообразующий"),
    ("SOAP_MAT-образующий", "мылообразующий"),
    ("SOAP_MAT", "мыло"),
    ("TALLOW", "жир"),
    ("GLAZE_MAT-образующий", "глазуреобразующий"),
    ("GLAZE_MAT", "глазурь"),
    ("CAN_GLAZE", "глазуруемый"),
    ("FLUX", "флюс"),
    ("GIPSUM", "гипс"),
    ("DRINK_MAT", "напиток"),
    ("FAT", "жир"),
    ("RENDER_MAT", "вытапливаемый"),
    # ("PRESS_LIQUID_MAT", ""),
    # ("HONEYCOMB_PRESS_MAT", ""),
    (' доверенное л ', ' доверенное лицо '),  # Temporary fix for 'hearthperson' cutting
    ('источника в.', 'источника воды.'),  # Temporary fix for 'No water source.' cutting
    ('большой, зазубренный', 'большой зазубренный'),
    ('ремесленник мастерская', 'мастерская ремесленника'),
    ('Ремесленник мастерская', 'Мастерская ремесленника'),
])

############################################################################
# masculine = 'masc'  # м. род
# feminine = 'femn'  # ж. род
# neuter = 'neut'  # ср. род
# plural = 'plur'  # мн. ч.

# Case names - as a reference only
# case_names = (
#     "nomn",  # именительный
#     "gent",  # родительный
#     "datv",  # дательный
#     "accs",  # винительный
#     "ablt",  # творительный
#     "loct",  # предложный
# )

make_adjective = {
    # металл
    'из меди': "медный",
    'из железа': 'железный',
    'из серебра': "серебряный",
    'из бронзы': "бронзовый",
    'из стали': "стальной",
    'из золота': "золотой",
    'из никеля': "никелевый",
    'из цинка': "цинковый",
    'из латуни': 'латунный',
    'из чугуна': 'чугунный',
    'из платины': 'платиновый',
    'из электрума': 'электрумный',
    'из олова': 'оловянный',
    'из свинца': 'свинцовый',
    'из алюминия': 'алюминиевый',
    'из нейзильбера': 'нейзильберовый',
    'из биллона': 'билонный',
    'из стерлинга': 'стерлинговый',
    'из висмута': 'висмутовый',
    'из адамантина': 'адамантиновый',

    # дерево
    'из сосны': 'сосновый',
    'из кедра': 'кедровый',
    'из дуба': 'дубовый',
    'дуб': 'дубовый',
    'из ореха': 'ореховый',
    'из клёна': 'кленовый',
    'клён': 'кленовый',
    'из ивы': 'ивовый',
    'из мангров': 'мангровый',
    'из пальмы': 'пальмовый',
    'из лиственницы': 'лиственничный',
    'из каштана': 'каштановый',
    'из ольхи': 'ольховый',
    'из берёзы': 'берёзовый',
    'из лумбанга': 'лумбанговый',

    # неорганическое
    'из кремня': 'кремневый',
    'из аргиллита': 'аргилитовый',
    'из песчаника': 'песчаниковый',
    'из алевролита': 'алевролитовый',
    'из сланца': 'сланцевый',
    'из известняка': 'известняковый',
    'из конгломерата': 'конгломератный',
    'из доломита': 'доломитовый',
    'из мела': 'меловый',
    'из гранита': 'гранитный',
    'из диорита': 'диоритовый',
    'из габбро': 'габбровый',
    'из риолита': 'риолитовый',
    'из базальта': 'базальтовый',
    'из андезита': 'андезитовый',
    'из дацита': 'дацитовый',
    'из обсидиана': 'обсидиановый',
    'из кварцита': 'кварцитовый',
    'из филита': 'филитовый',
    'из гнейса': 'гнейсовый',
    'из мрамора': 'мраморный',
    'из каменной глины': 'из каменной глины',
    'из каменной соли': 'из каменной соли',
    'из грифельного сланца': 'из грифельного сланца',
    'из аспидного сланца': 'из аспидного сланца',

    # неорганические камни минералы
    'из красного железняка': 'из красного железняка',
    'из бурого железняка': 'из бурого железняка',
    'из самородного золота': 'из самородного золота',
    'из гарниерита': 'гарниеритовый',
    'из самородной меди': 'из самородной меди',
    'из малахита': 'малахитовый',
    'из галенита': 'галенитовый',
    'из сфалерита': 'сфалеритовый',
    'из касситерита': 'касситеритовый',
    'из каменного угля': 'из каменного угля',
    'из бурого угля': 'из бурого угля',
    'из самородной платины': 'из самородной платины',
    'из киновари': 'киноварный',
    'из кобальтита': 'кобальтитовый',
    'из тетраэдрита': 'тетраэдритовый',
    'из рогового серебра': 'из рогового серебра',
    'из гипса': 'гипсовый',
    'из талька': 'тальковый',
    'из гагата': 'гагатовый',
    'из пудингового конгломерата': 'из пудингового конгломерата',
    'из окаменелой древесины': 'из окаменелой древесины',
    'из графита': 'графитовый',
    'из серы': 'серный',
    'из кимберлита': 'кимберлитовый',
    'из висмутина': 'висмутиновый',
    'из реальгара': 'реальгаровый',
    'из аурипигмента': 'аурипигментовый',
    'из стибнита': 'стибнитовый',
    'из марказита': 'марказитовый',
    'из сильвина': 'сильвиновый',
    'из криолита': 'криолитовый',
    'из периклаза': 'периклазовый',
    'из ильменита': 'ильменитовый',
    'из рутила': 'рутиловый',
    'из магнетита': 'магнетитовый',
    'из хромита': 'хромитовый',
    'из пиролюзита': 'пиролюзитовый',
    'из уранинита': 'уранинитовый',
    'из боксита': 'бокситовый',
    'из самородного алюминия': 'из самородного алюминия',
    'из буры': 'буровый',
    'из оливина': 'оливиновый',
    'из роговой обманки': 'из роговой обманки',
    'из каолинита': 'каолинитовый',
    'из серпентина': 'серпентиновый',
    'из ортоклаза': 'ортоклазовый',
    'из микроклина': 'микроклиновый',
    'из слюды': 'слюдяной',
    'из кальцита': 'кальцитовый',
    'из селитры': 'селитровый',
    'из алебастра': 'алебастровый',
    'из селенита': 'селенитовый',
    'из шелковистого шпата': 'из шелковистого шпата',
    'из ангидрита': 'ангедритовый',
    'из алунита': 'алунитовый',
    'из необработанного адамантина': 'из необработанного адамантина',
    'из слейда': 'слейдовый',
    # стекло и камни из одного слова
    'хрусталь': "из хрусталя",
    'морион': "из мориона",
    'моховой опал': "из мохового опала",
    'шерл': "из шерла",
    'лазурит': "из лазурита",
    'прозапал': "из прозапала",
    'кровавик': "из кровавика",
    'моховой агат': "из мохового агата",
    'хризопраз': "из хризопраза",
    'сердолик': "из сердолика",
    'вишнёвый опал': "из вишнёвого опала",
    'пейзажная яшма': "из пейзажной яшмы",
    'дымчатый кварц': "из дымчатого кварца",
    'цитрин': "из цитрина",
    'смолистый опал': "из смолистого опала",
    'пирит': "из пирита",
    'чистый турмалин': "из чистого турмалина",
    'серый халцедон': "из серого халцедона",
    'ракушечный опал': "из ракушечного опала",
    'костяной опал': "из костяного опала",
    'бастионный агат': "из бастионного агата",
    'молочный кварц': "из молочного кварца",
    'лунный камень': "из лунного камня",
    'яшмовый опал': "из яшмого опала",
    'ониксовый опал': "из ониксового опала",
    'горный хрусталь': "из горного хрусталя",
    'сардоникс': "из сардоникса",
    'чёрный циркон': "из чёрного циркона",
    'чёрный пироп': "из чёрного пиропа",
    'индиговый турмалин': "из индигового турмалина",
    'синий гранат': "из синего граната",
    'зелёный турмалин': "из зелёного турмалина",
    'демантоид': "из демантоида",
    'зелёный циркон': "из зелёного циркона",
    'красный циркон': "из красного циркона",
    'красный турмалин': "из красного турмалина",
    'красный пироп': "из красного пиропа",
    'биксбит': "из биксбита",
    'пурпурная шпинель': "из пурпурной шпинели",
    'александрит': "из александрита",
    'морганит': "из морганита",
    'фиолетовый спессартин': "из фиолетового спессартина",
    'кунцит': "из кунцита",
    'голиодор': "из голиодора",
    'жилейный опал': "из жилейного опала",
    'коричневый циркон': "из коричневого опала",
    'жёлтый циркон': "из жёлтого циркона",
    'жёлтый спессартин': "из жёлтого спессартина",
    'топаз': "из топаза",
    'рубицелл': "из рубицелла",
    'гошенит': "из гошенита",
    'кошачий глаз': "из кошачего глаза",
    'чистый циркон': "из чистого циркона",
    'аметист': "из аметиста",
    'аквамарин': "из аквамарина",
    'красная шпинель': "из красной шпинели",
    'хризоберилл': "из хризоберилла",
    'кристаллический опал': "из кристаллического опала",
    'опал арлекин': "из опала-арлекина",
    'слоистый огненный опал': "из слоистого огненного опала",
    'изумруд': "из изумруда",
    'зеленое стекло': "из зеленого стекла",
    'бесцветное стекло': "из бесцветного стекла",
    'гелиодор': "из гелиодора",
    'желейный опал': "из желейного опала",
    'лавандовый нефрит': "из лавандового нефрита",
    'розовый нефрит': "из розового нефрита",
    'восковой опал': "из воскового опала",
    'янтарный опал': "из янтарного опала",
    'золотистый опал': "из золотистого опала",
    'празеолит': 'из празеолита',
    'белый нефрит': "из белого нефрита",
    'ананасовый опал': "из ананасового опала",
    'трубчатый опал': "из трубчатого опала",
    'авантюрин': "из авантюрина",
    'розовый кварц': "из розового кварца",
    'зелёный нефрит': "из зелёного нефрита",
    'альмандин': "из альмандина",
    'розовый турмалин': "из розового турмалина",
    'огненный опал': "из огненного опала",
    'родолит': "из родолита",
    'танзанит': "из танзанита",
    'золотистый берилл': "из огненного опала",
    'топазолит': "из топазолита",
    'чистый гранат': "из чистого граната",
    'чёрный опал': "из чёрного опала",
    'светло-жёлтый алмаз': "из светло-жёлтого алмаза",
    'зелeное стекло': "из зеленого стекла",
    'прозрачное стекло': "из прозрачного стекла",
    'белый халцедон': "из белого халцедона",
    # размеры и др
    'большой': "большой",
    'гигантский': "гигантский",
    'заточенный': "заточенный",
    'огромный': "огромный",
    'шипованный': "шипованный",
    'зазубренный': "зазубренный",
    'кольчужный': "кольчужный",
    'изысканный': "изысканный",
    'большой,': "большой",
    'грубый': "грубый",

    # Формы огранки
    'бриолетовый': "бриолетовый",
    'огранённый розой': "огранённый розой",
    'огранённый подушечкой': "огранённый подушечкой",
    'плоскогранный': "плоскогранный",
    'прямоугольный': "прямоугольный",
    'гладкий': "гладкий",
    'овальный': "овальный",
    'круглый': "круглый",
    'сглаженный': "сглаженный",

    # кожа, шёлк
    'из кожи': "кожаный",
    'из шёлка': "шёлковый",
    'шёлк': 'шёлковый',

    # разные материалы
    'металл': "металлический",
    'кожа': "кожаный",
    'растительное волокно': 'из растительного волокна',
    'дерево': "деревянный",
    'кость': "костяной",
    'камень': 'каменный',
}

dict_ending_s = {
    'готовая еда': 'готовая еда',
    'питьё': 'питьё',
    'стул': 'стулья',
    'доспешная стойка': 'доспешные стойки',
    'оружейная стойка': 'оружейные стойки',
    'дублёная шкура': 'дублёные шкуры',
    'большой самоцвет': 'большие самоцветы',
    'баклер': 'баклеры',
    'оружие': 'оружие',
    'крышка люка': 'крышки люка',
    'ручная мельница': 'ручные мельницы',
    'ловушка для животных': 'ловушки для животных',
    'часть ловушки': 'части ловушек',
    'музыкальный инструмент': 'музыкальные инструменты',
    'наконечник стрелы баллисты': 'наконечники стрелы баллисты',
    'часть тела': 'части тела',
    'конечность/тело гипс': 'гипс для конечностей тела',
    'Элитный борец': 'Элитные борцы',
    'Лорд топора': 'Лорды топора',
    'Лорд булавы': 'Лорды булавы',
    'Лорд молота': 'Лорды молота',
    'Мастер меча': 'Мастера меча',
    'Мастер копья': 'Мастера копья',
}

gender_exceptions = {
    'шпинель': 'femn', 'гризли': 'masc',
}


def pm_gender(parse):
    tag = parse.tag
    # print(tag)
    if tag.number == 'plur':
        gender = tag.number
    else:
        gender = tag.gender
    # print(gender)
    return str(gender)  # explicitly convert to a string any internal types returned from pymorphy2


def get_gender(obj, known_tags=None):
    # print("get_gender(%r, known_tags=%r)" % (obj, known_tags))
    assert ' ' not in obj, 'get_gender() is not suitable for word collocations'

    if '-' in obj:
        obj = obj.split('-')
        if obj[0] in {'мини'}:
            obj = obj[1]
            # print('Using the second part of the hyphen-compound: %r' % obj)
        else:
            obj = obj[0]
            # print('Using the first part of the hyphen-compound: %r' % obj)

    parse = custom_parse(obj)
    if known_tags is not None:
        parse = [p for p in parse if known_tags in p.tag]

    if obj.lower() in gender_exceptions:
        return gender_exceptions[obj.lower()]
    else:
        if len(parse) > 0:
            gender = pm_gender(parse[0])
            for p in parse:
                if pm_gender(p) != gender:
                    # print("Gender cannot be recognized definitely for %r. Try to specify known tags (eg. case)" % obj)
                    return None
        else:
            # print("Gender not recoginzed for %r" % obj)
            return None
        return pm_gender(parse[0])


def get_main_word_gender(text):
    if ' ' not in text:
        return get_gender(text, known_tags={'nomn'})
    else:
        for word in text.split():
            if any_in_tag({'NOUN', 'nomn'}, custom_parse(word)):
                return get_gender(word, known_tags={'NOUN', 'nomn'})


def parse_as_adjective(adjective: str) -> list:
    parse = [p for p in custom_parse(adjective) if 'ADJF' in p.tag or 'PRTF' in p.tag]
    assert len(parse) > 0, 'parse: %r' % parse
    return parse


def inflect_adjective(adjective: str, gender: str, case='nomn', animated=None):
    # print('inflect_adjective(%s, %s)' % (adjective, case))
    assert gender is not None
    parse = parse_as_adjective(adjective)
    p = parse[0]
    form_set = {gender, case}
    if animated is not None and gender in {'masc', 'plur'}:
        form_set.add('anim' if animated else 'inan')
    # print('form_set:', form_set)
    new_form = p.inflect(form_set)
    if new_form is None:
        form_set = {gender, case}
        # print('form_set:', form_set)
        new_form = p.inflect(form_set)
    ret = new_form.word
    # print('%s -> %s' % (adjective, ret))
    return ret


gent_case_except = {
    'шпинель': 'шпинели',  # определяет как сущ. м.р.
    'стена': 'стены',  # определяет как сущ. м.р.
    'лиса': 'лисы',  # определяет как сущ. м.р.
    'споры': 'спор',  # в родительный падеж ставит как "споров"
}


def inflect_noun(word: str, case: str, orig_form=None):
    # print('inflect_noun(%r, %r, %r)' % (word, case, orig_form))
    parse = list(filter(lambda x: x.tag.POS == 'NOUN', custom_parse(word)))

    if orig_form:
        parse = [p for p in parse if orig_form in p.tag]

    if len(parse) == 0:
        # print('Failed to set %r to %s case.' % (word, case))
        return None

    new_form = parse[0].inflect({case})

    return new_form.word


def genitive_case_single_noun(word: str):
    # print('genitive_case_single_noun')
    # print(word)
    if word.lower() in gent_case_except:
        return gent_case_except[word.lower()]
    else:
        return inflect_noun(word, case='gent')


def is_adjective(word: str, parse=None):
    if parse is None:
        parse = custom_parse(word)
    return any('ADJF' in p.tag or 'PRTF' in p.tag for p in parse)


def genitive_case_list(words: list):
    # print("genitive_case_list(%r)" % words)
    if len(words) == 1:
        gender = get_gender(words[0], {'nomn'})
    else:
        gender = None
        for word in words:
            if any_in_tag({'NOUN', 'nomn'}, custom_parse(word)):
                gender = get_gender(word, {'NOUN', 'nomn'})
                break
        assert gender is not None

    for word in words:
        if is_adjective(word):
            word = inflect_adjective(word, gender, 'gent')
        else:
            word = genitive_case_single_noun(word)
        assert word is not None
        yield word


def genitive_case(word: str):
    return ' '.join(genitive_case_list(word.split()))


#############################################################################

animals_female = {"собака", "самка", "крольчиха", "гусыня", "утка", "кошка", "ослица", "кобыла", "корова", "овца",
                  "свинья",
                  "коза", "курица", "свинка", "буйволица", "важенка", "лама", "альпака", "цесарка", "пава", "индейка", }

body_parts = {"панцирь", "скелет", "искалеченный труп", "останки", "кость", "кожа", "шёлк", "волокна", "шерсть", "мех",
              "хвост"}

opening = {'!', '(', '*', '+', '-', '[', '{', '«', 'р', '☼', 'X', 'x'}
closing = {'«': '»', '[': ']', '(': ')', '{': '}'}


def open_brackets(func):
    @functools.wraps(func)
    def wrapper(text):
        start_i = 0
        end_i = len(text) - 1
        for c in text:
            if c in opening:
                start_i += 1
                if text[end_i] == closing.get(c, c):
                    end_i -= 1
            else:
                break

        if (start_i > 0 and text[start_i - 1] == 'р' and (end_i == len(text) - 1 or text[end_i + 1] != 'р')
            and not text[start_i:].startswith('из')) and not text[start_i].isupper():
            start_i -= 1

        leading_symbols = text[:start_i].replace('р', '≡')
        trailing_symbols = text[end_i + 1:].replace('р', '≡')

        return leading_symbols + func(text[start_i:end_i + 1]) + trailing_symbols

    return wrapper


re_item_general = re.compile(r"^[(+*-«☼]*((р?)(из\s[\w\s\-/]+\b))")

# corr_item_general_except = {
#     # "боевой",  # Avoid recognition "боевой" as a female surname in genitive
#     # "кирки",  # Avoid recognition "кирки" as a noun in genitive
#     # "бочка",  # Avoid recognition "бочка" as "бочок" in genitive
# }


def any_in_tag(gram, parse):
    return any(gram in p.tag for p in parse)


@open_brackets
def corr_item_general(text):
    # print('corr_item_general')
    search_result = re_item_general.search(text)
    initial_string = search_result.group(1)
    words = search_result.group(3).split()

    # print(words)
    if len(words) == 2:
        parse = list(filter(lambda x: {'NOUN', 'gent'} in x.tag, custom_parse(words[1])))
        assert len(parse) == 1
        replacement_string = parse[0].normal_form
    elif words[1] == 'древесины':
        # Ultra simple case
        if 'дерева' in words:  # 'из древесины миндального дерева'
            cut_index = words.index('дерева') + 1
        elif 'пекан' in words:  # 'из древесины ореха пекан'
            cut_index = words.index('пекан') + 1
        elif any_in_tag({'NOUN', 'gent'}, custom_parse(words[2])):  # 'из древесины яблони'
            cut_index = 3
        else:
            cut_index = -1
        replacement_string = ' '.join(words[cut_index:] + words[:cut_index])
    elif (all(any_in_tag({'ADJF', 'gent'}, custom_parse(adj)) for adj in words[1:-1]) and
          any_in_tag({'NOUN', 'gent'}, custom_parse(words[-1]))):
        # All words after 'из' except the last word are adjectives in genitive
        # The last is a noun in genitive
        material = words[-1]
        gender = get_gender(material, known_tags={'gent'})
        parse = list(filter(lambda x: {'NOUN', 'gent'} in x.tag, custom_parse(material)))
        material = parse[0].normal_form
        adjs = words[1:-1]
        adjs = [inflect_adjective(adj, gender, case='nomn') for adj in adjs]
        replacement_string = ' '.join(adjs) + ' ' + material
    # elif (words[2] not in corr_item_general_except and len(words) > 3 and
    elif (len(words) > 3 and
          any_in_tag({'gent'}, custom_parse(words[1])) and  # The second word is in genitive
          any_in_tag({'NOUN', 'gent'}, custom_parse(words[2]))):  # The third word is a noun in genitive
        # Complex case, eg. "из висмутовой бронзы"
        # print('Complex case')
        of_material = " ".join(words[:3])
        words = words[3:]
        if len(words) == 1:
            first_part = words[0]
        else:
            obj = words[-1]
            gender = get_gender(obj, 'NOUN')
            adjs = (inflect_adjective(adj, gender) or adj for adj in words[:-1])
            first_part = "%s %s" % (" ".join(adjs), obj)
        replacement_string = first_part + " " + of_material
    elif any_in_tag({'NOUN', 'gent'}, custom_parse(words[1])) and words[1] != 'древесины':
        # Simple case, eg. "из бронзы"
        # print('Simple case')
        of_material = " ".join(words[:2])
        words = words[2:]
        item = words[-1]

        for word in words:
            if any_in_tag({'NOUN', 'nomn'}, custom_parse(word)):
                item = word
                break

        if of_material in make_adjective:
            gender = get_gender(item, {'nomn'})

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
        raise ValueError('Unknown case: %r' % text)

    text = text.replace(initial_string, replacement_string)
    return text


re_3 = re.compile(r'(\(?)(.+)\s(\bяйцо|требуха|железы|железа|мясо|кровь|сукровица|кольца|серьги|амулеты|браслеты'
                  r'|скипетры|коронаы|статуэтки\b)')

re_3_1 = re.compile(r"(\bЛужа|Брызги|Пятно)\s(.+)\s(кровь\b)")


# выражения типа "рогатый филин яйцо"
def corr_item_3(text):
    """
    >>> corr_item_3('рогатый филин яйцо')
    'яйцо рогатого филина'
    """
    # print(3)
    search_result = re_3.search(text)
    if re_3_1.search(text):
        # print(3.1)
        search_result = re_3_1.search(text)
        text = search_result.group(1) + " " + genitive_case(search_result.group(3) + " " + search_result.group(2))
        return text.capitalize()
    if search_result.group(3) in replaced_parts:
        # print(3.2)
        new_word = replaced_parts[search_result.group(3)]
    else:
        # print(3.3)
        new_word = search_result.group(3)
    if search_result.group(2) in make_adjective:
        # print(3.4)
        text = text.replace(search_result.group(0),
                            search_result.group(1) + new_word + " " + make_adjective[search_result.group(2)])
    else:
        # print(3.5)
        text = text.replace(search_result.group(0),
                            search_result.group(1) + new_word + " " + genitive_case(search_result.group(2)))
    # print(3.0)
    return text


# выражения типа "приготовленные(рубленная) гигантский крот лёгкие"
re_prepared = re.compile(r"\W((приготовленные|рубленная)\s(.+)\s(\w+))")


def corr_prepared(text):
    # print('corr_prepared(%r)' % s)
    search_result = re_prepared.search(text)
    groups = search_result.groups()
    result = text.replace(groups[0], "{} {} {}".format(groups[1], groups[3], genitive_case(groups[2])))
    return result


re_skin = re.compile(r'(\(?)(.+)\s(из кожи|из шерсти)')


# выражения типа "горный козёл из кожи"
def corr_item_skin(text):
    """
    >>> corr_item_skin("горный козёл из кожи")
    'кожа горного козла'
    
    >>> corr_item_skin("альпака из шерсти")
    'шерсть альпака'
    """
    # print('corr_item_skin')
    search_result = re_skin.search(text)
    material = inflect_noun(search_result.group(3).split()[-1], 'nomn')  # кожа, шерсть и т.д.
    text = text.replace(search_result.group(0),
                        search_result.group(1) + material + ' ' + genitive_case(search_result.group(2)))
    return text


# выражения типа "свинохвост из волокон (ткань+шёлк+шерсть)"
re_clothes = re.compile(r'^[Xx\(+*-«☼]*((.+)\s'
                        r'(из волокон'
                        r'|из шёлка'
                        r'|из шерсти'
                        r'|из кожи'
                        r'|из копыт'
                        r'|из кости'
                        r'|из рога'
                        r'|из рогов'
                        r'|из бивней'
                        r'|из панциря'
                        r'|из зубов)'
                        r'\s(\w+\s?\w+))')


@open_brackets
def corr_clothes(text):
    # print('corr_clothes')
    search_result = re_clothes.search(text)
    # print(search_result.group(1))
    text = text.replace(search_result.group(1),
                        search_result.group(4) + " " + search_result.group(3)
                        + " " + genitive_case(search_result.group(2)))
    text = text.replace("левый", "левая")
    text = text.replace("правый", "правая")
    return text


# выражения типа "древесина дуба брёвна"
re_wooden_logs = re.compile(r'(древесина)\s(\w+)\s(брёвна)')


def corr_wooden_logs(text):
    """
    >>> corr_wooden_logs('древесина дуба брёвна')
    'дубовые брёвна'
    """
    # print('corr_wooden_logs')
    search_result = re_wooden_logs.search(text)
    of_wood = "из " + search_result.group(2)
    if of_wood in make_adjective:
        adj = inflect_adjective(make_adjective[of_wood], 'plur')
        text = text.replace(search_result.group(0), adj + " " + search_result.group(3))  # берёзовые брёвна
    else:
        text = text.replace(search_result.group(0),
                            search_result.group(1) + " " + search_result.group(2))  # древесина акации
    return text


# выражения типа "(бриолетовый восковые опалы)"
re_gem_cutting = re.compile(r'((бриолетовый|большой|огранённый|грубый)\s[\w\s-]+)')


def corr_gem_cutting(text):
    # print('corr_gem_cutting')
    search_result = re_gem_cutting.search(text)
    words = search_result.group(1).split()
    if words[-1] in body_parts:
        # print('Redirect to corr_item_body_parts')
        return corr_item_body_parts(text)

    # print(words)
    gender = get_gender(words[-1], {'NOUN', 'nomn'})
    # print("gender:", gender)

    new_list = []
    for word in words[:-1]:
        if word in make_adjective:
            adj = make_adjective[word]
            word = inflect_adjective(adj, gender)
        new_list.append(word)

    new_list.append(words[-1])

    return text.replace(search_result.group(0), " ".join(new_list))


# выражения типа "гигантский из ясеня лезвия топоров"
re_weapon_trap_parts = re.compile(
    r'(шипованный|огромный|большой|заточенный|гигантский|большой зазубренный)\s(из\s[\w\s]+\b)')


def corr_weapon_trap_parts(text):
    """
    >>> corr_weapon_trap_parts('гигантский из меди лезвия топоров')
    'гигантские медные лезвия топоров'
    """
    # print('corr_weapon_trap_parts')
    search_result = re_weapon_trap_parts.search(text)
    adj = search_result.group(1)
    words = search_result.group(2).split()
    if " ".join(words[:2]) in make_adjective:
        # print(9.1)
        material = " ".join(words[:2])
        # print("material:", material)
        obj = " ".join(words[2:])
        # print("object:", obj)
        gender = get_main_word_gender(obj)
        # print("object gender:", gender)
        if adj not in make_adjective and " " in adj:
            adj_words = adj.split()
            new_words = [inflect_adjective(make_adjective[word], gender) for word in adj_words]
            new_adj = " ".join(new_words)
        else:
            new_adj = inflect_adjective(make_adjective[adj], gender)
        # print(adj, ":", new_adj)
        new_word_2 = inflect_adjective(make_adjective[material], gender)
        # print(material, ":", new_word_2)
        text = text.replace(search_result.group(0), "%s %s %s" % (new_adj, new_word_2, obj))
    else:
        # print(9.2)
        material = " ".join(words[:3])
        # print("material:", material)
        obj = " ".join(words[3:])
        # print("object:", obj)
        gender = get_main_word_gender(obj)
        assert gender is not None
        if adj not in make_adjective and " " in adj:
            adj_words = adj.split()
            new_words = [inflect_adjective(make_adjective[word], gender) for word in adj_words]
            new_adj = " ".join(new_words)
        else:
            new_adj = inflect_adjective(make_adjective[adj], gender)
        # print(adj, ":", new_adj)
        text = text.replace(search_result.group(0), "%s %s %s" % (new_adj, obj, material))
    return text


animal_genders = {
    'собака': ('пёс', 'собака'),
    'кошка': ('кот', 'кошка'),
    'лошадь': ('конь', 'лошадь')
}

re_animal_gender = re.compile(r"(\w+), ([♂♀])")


def corr_animal_gender(text):
    # print('corr_animal_gender(%r)' % s)
    search_result = re_animal_gender.search(text)

    gender = '♂♀'.index(search_result.group(2))
    animal = search_result.group(1)
    if animal not in animal_genders:
        # print('Unknown animal: %r' % animal)
        return None
    else:
        return text.replace(search_result.group(0), animal_genders[animal][gender] + ", " + search_result.group(2))


re_animal = re.compile(r'(охотничий|боевой|сырой) (\w+)(\(Ручной\))?')


# "животные"
def corr_animal(text):
    # print('corr_animal')
    text = text.replace("сырой", "сырая")
    if any(item in text for item in animals_female):
        text = text.replace("(Ручной)", "(Ручная)")
        text = text.replace("боевой", "боевая")
        text = text.replace("Ничей", "Ничья")
        text = text.replace("охотничий", "охотничья")

    return text


posessive_adjectives = {
    'жаба': 'жабий',
    'корова': 'коровий',
    'медведь': 'медвежий'
}

re_container = re.compile(r'(\b.+)\s(бочка|мешок|ящик)\s\((.*?)(\)|$)')

replace_containment = {
    "Семя": "семена",
    "Специи": "специй",
    "Самоцвет": "самоцветы",
    "Слиток/Блок": "слитков/блоков",
}

materials = {'волокон', 'шёлка', 'шерсти', 'кожи'}


# выражения типа "(дварфийское пиво бочка (из ольхи))"
@open_brackets
def corr_container(text):
    """
    >>> corr_container('(дварфийское пиво бочка (из ольхи))')
    '(Бочка дварфийского пива (ольховая))'
    """
    # print("corr_container")
    search_result = re_container.search(text)
    initial_string = search_result.group(0)
    # print('initial_string:', initial_string)
    containment = search_result.group(1)
    if containment in replace_containment:
        containment = replace_containment[containment]
    if containment.endswith('кровь'):
        words = containment.split()
        if words[0] in posessive_adjectives:
            words[0] = posessive_adjectives[words[0]]
            words = genitive_case_list(words)
        else:
            words = [genitive_case_single_noun(words[-1])] + list(genitive_case_list(words[:-1]))
        containment = " ".join(words)
    elif containment.startswith('из '):
        containment = containment[3:]  # Words after 'из' are already in genitive case
    elif containment in {'слитков/блоков', 'специй'}:
        pass  # Already in genitive case
    elif containment.startswith('семена'):
        words = containment.split()
        words[0] = genitive_case(words[0])
        containment = ' '.join(words)
    else:
        containment = genitive_case(containment)
    container = search_result.group(2)
    of_material = search_result.group(3)
    if not of_material:
        # print('Void material')
        replacement_string = container + ' ' + containment
    elif (' ' not in of_material and is_adjective(of_material) or
          of_material in make_adjective or of_material[3:] in make_adjective):
        # print('Case 1')

        if ' ' not in of_material and is_adjective(of_material):
            adjective = of_material
        elif of_material in make_adjective:
            adjective = make_adjective[of_material]
        elif of_material[3:] in make_adjective:
            adjective = make_adjective[of_material[3:]]
        else:
            adjective = None
        gender = get_gender(container, {'nomn'})
        adjective = inflect_adjective(adjective, gender)
        # print([container, containment, adjective])
        replacement_string = '%s %s (%s)' % (container, containment, adjective)
    else:
        # print('Case 2')
        words = of_material.split()
        material = None
        if of_material.startswith('из ') or len(of_material) <= 2:
            # print('Material name is too short or it starts with "из"')
            material = of_material
        elif len(words) >= 2 and words[-2] == 'из' and (words[-1] in materials or
                                                        any(mat.startswith(words[-1]) for mat in materials)):
            # Try to fix truncated materail names, eg. '(ямный краситель мешок (гигантский пещерный паук из шёл'
            if words[-1] not in materials:  # Fix partial material name eg. 'шерст', 'шёлк'
                candidates = [mat for mat in materials if mat.startswith(words[-1])]
                if len(candidates) == 1:
                    words[-1] = candidates[0]
                else:
                    material = of_material  # Partial name is not recognized (too short)

            if not material:
                material = ' '.join(words[-2:] + list(genitive_case_list(words[:-2])))
        else:
            gen_case = list(genitive_case_list(of_material.split()))
            if None not in gen_case:
                material = 'из ' + ' '.join(gen_case)
            else:
                material = of_material
        replacement_string = "%s %s (%s" % (container, containment, material)
        if initial_string[-1] == ')':
            replacement_string += ')'
    text = text.replace(initial_string, replacement_string.capitalize())
    return text


# Элементы рельефа, крепости и т.п.
re_corr_relief = re.compile(
    r'(.+)\s(Подъем|Стена|Кластер|валун|склон|Пол Пещеры|лестница вверх/вниз|пол пещеры|'
    r'Лестница Вверх|Лестница Вниз|галька|деревце|лестница вверх|лестница вниз|подъем|пол)\b'
)


#    (прилагательное) (первое дополнение) (второе дополнение) =>
# => (прилагательное) (второе дополнение) из (первое дополнение)


def corr_relief(text):
    # print('corr_relief')
    search_result = re_corr_relief.search(text)
    group1 = search_result.group(1)
    obj = search_result.group(2)
    if obj == "деревце":
        if group1.split(" ")[0] == "Мёртвый":
            text = "Мёртвое деревце (" + ''.join(search_result.group(0).split(" ")[1:-1]) + ")"
        else:
            text = "Деревце (" + group1 + ")"
        return text.capitalize()

    if " " in group1:
        # print('several words')
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

        words = words[len(first_words):]

        if words[0] == "из":
            words = words[1:]
        else:
            words = genitive_case_list(words)

        if not first_words:
            # print("12.1.1")
            text = "%s из %s" % (obj, " ".join(words))
        else:
            # print("12.1.2")
            text = "%s %s из %s" % (" ".join(first_words), obj, " ".join(words))
    else:
        # print('one word')
        material = group1
        text = "%s из %s" % (obj, genitive_case(material))

    if "иза" in text:
        text = text.replace(" иза", "")
    return text.capitalize()


re_13_1 = re.compile(r'\b(Густой|Редкий|Заснеженный)\s(.+)')


# "Густой и тп"
def corr_item_13(text):
    # print(13)
    search_result = re_13_1.search(text)
    adjective = search_result.group(1)
    obj = search_result.group(2)

    if " " in obj:
        # print(13.1)
        words = obj.split(" ")
        if is_adjective(words[0]):
            # print("13.1.1")
            gender = get_gender(words[-1])
            new_word = inflect_adjective(words[0], gender, 'nomn')
            text = text.replace(words[0], new_word)
            new_word = inflect_adjective(adjective, gender, 'nomn')
            text = text.replace(adjective, new_word)
    else:
        # print(13.2)
        gender = get_gender(obj)
        new_word = inflect_adjective(adjective, gender, 'nomn')
        if new_word:
            # print("13.2.1")
            text = new_word + " " + obj

    return text.capitalize()


# "Скелет, останки и тп"
re_body_parts = re.compile(r'^{?((\w+\s?\w+?|)\s(панцирь|скелет|труп|останки|кость|кожа|шёлк|волокна|шерсть'
                           r'|мех|хвост|голень))}?\b')


def corr_item_body_parts(text):
    # print('corr_item_body_parts(%r)' % s)
    search_result = re_body_parts.search(text)
    initial_string = search_result.group(1)
    words = search_result.group(2).split()
    if words[-1] in {"частичный", "искалеченный"}:
        replacement_string = "%s %s %s" % (words[-1], search_result.group(3), " ".join(genitive_case_list(words[:-1])))
    else:
        if any('GRND' in custom_parse(word)[0].tag for word in words):  # Ignore participles
            return None
        replacement_string = search_result.group(3) + " " + " ".join(genitive_case_list(words))
    return text.replace(initial_string, replacement_string.capitalize())


re_craft_glass = re.compile(r'\b(Делать|Изготовить)\s([\w\s]*)(стекло|хрусталь)([\w\s]*)')


def corr_craft_glass(text):  # TODO: Combine into single crafting-related function
    # print('corr_craft_glass')
    search_result = re_craft_glass.search(text)
    material = search_result.group(3)
    # print('material: %r' % material)
    material_gender = get_gender(material)
    words = search_result.group(2).split()
    # print('words: %r' % words)
    product = search_result.group(4).split()
    # print('product: %r' % product)
    verb = search_result.group(1)
    if not product:
        verb = 'Варить'
        adjectives = (inflect_adjective(adj, material_gender, 'accs', animated=False) for adj in words)
        result = "%s %s %s" % (verb, ' '.join(adjectives), material)
    else:
        index = next((i for i, item in enumerate(words) if item in {'грубое', 'зелёное', 'прозрачное', 'грубый'}),
                     len(words))
        product_adjectives = words[:index]
        if any_in_tag({'NOUN', 'nomn'}, custom_parse(product[0])):
            product_gender = get_gender(product[0])
            product[0] = inflect_noun(product[0], case='accs')
        else:
            product_gender = get_gender(product[-1])
            product_adjectives += product[:-1]
            product = [inflect_noun(product[-1], case='accs')]

        product_adjectives = [inflect_adjective(adj, product_gender, case='accs', animated=False)
                              for adj in product_adjectives]
        material_adjectives = [inflect_adjective(adj, material_gender, case='gent', animated=False)
                               for adj in words[index:]]

        material = inflect_noun(material, case='gent')
        product_words = product_adjectives + product
        material_words = material_adjectives + [material]
        result = "%s %s из %s" % (verb, ' '.join(product_words), ' '.join(material_words))

    # print('result:', result)
    return text.replace(search_result.group(0), result)


re_craft_general = re.compile(r'(Делать|Изготовить)([\w\s]+)$')


def corr_craft_general(text):
    # print('corr_craft_general')
    search_result = re_craft_general.search(text)
    verb = search_result.group(1)
    words = search_result.group(2).split()
    # print('words:', words)
    product = None
    if len(words) > 1:
        for i, word in enumerate(words[1:], 1):
            if any_in_tag({'NOUN', 'nomn'}, custom_parse(word)) and word not in make_adjective:
                product = ' '.join(words[i:])
                words = words[:i]
                break
    else:
        product = words[0]
        words = []

    # print('product:', product)
    product_gender = get_main_word_gender(product)
    # print('gender:', product_gender)

    if ' ' not in product:
        orig_form = {'plur' if product_gender == 'plur' else 'sing', 'inan'}
        # print('orig_form =', orig_form)
        product = inflect_noun(product, 'accs', orig_form=orig_form)
        assert product is not None
    else:
        product = inflect_collocation(product, {'accs'})

    if words:
        if len(words) == 1 and words[0] not in make_adjective and not is_adjective(words[0]):
            material = inflect_noun(words[0], 'gent', orig_form={'nomn', 'inan'})  # рог -> (из) рога
            assert material is not None
            result = "%s %s из %s" % (verb, product, material)
        else:
            adjectives = [make_adjective[word] if word in make_adjective
                          else word if is_adjective(word) else None
                          for word in words]
            assert all(adj is not None for adj in adjectives)
            adjectives = [inflect_adjective(adj, product_gender, 'accs', animated=False) for adj in adjectives]
            result = ("%s %s %s" % (verb, ' '.join(adjectives), product))
    else:
        result = "%s %s" % (verb, product)

    return text.replace(search_result.group(0), result).capitalize()


re_forge = re.compile(r"(^Ковать|^Делать|^Чеканить|^Изготовить|^Кузница)\s(из\s[\w\s?]+\b)")


# кузница
def corr_forge(text):
    # print('corr_forge')
    search_result = re_forge.search(text)
    verb = search_result.group(1)
    words = search_result.group(2).split()
    # print('Verb:', verb)
    # print('words:', words)
    assert len(words) >= 3
    if (any_in_tag({'ADJF', 'gent'}, custom_parse(words[1])) and  # The second word is an adj in gent
            any_in_tag({'NOUN', 'gent'}, custom_parse(words[2]))):  # The third word is a noun in gent
        # print('Complex case')
        of_material = words[:3]
        obj = words[3:]
    else:
        assert any_in_tag({'NOUN', 'gent'}, custom_parse(words[1]))
        # print('Simple case')
        of_material = words[:2]
        obj = words[2:]
        # print('of_material:', of_material)
        # print('obj:', obj)

    of_material = ' '.join(of_material)
    # print(obj)
    item_index = None
    if len(obj) == 1:
        item_index = 0
        parse = custom_parse(obj[item_index])
        p = list(filter(lambda x: {'NOUN'} in x.tag and 'Surn' not in x.tag, parse))
        gender = get_gender(obj[item_index], known_tags={'nomn'})
        if not any_in_tag({'accs'}, p):
            obj[0] = p[0].inflect({'accs'}).word
    else:
        parse = None
        gender = None
        for i, word in enumerate(obj):
            parse = custom_parse(word)
            p = list(filter(lambda x: {'NOUN'} in x.tag and 'Surn' not in x.tag, parse))
            if p:
                item_index = i
                gender = get_gender(obj[item_index])
                obj[i] = p[0].inflect({'accs'}).word
                break  # Words after the 'item' must be leaved in genitive case
            elif not any_in_tag('accs', parse):
                obj[i] = parse[0].inflect({'accs'}).word

    # print(obj)
    # print(obj[item_index])

    if not any_in_tag('accs', parse):
        obj[item_index] = parse[0].inflect({'accs'}).word

    if verb == 'Кузница':
        verb = 'Ковать'

    if of_material in make_adjective:
        # print('gender of "%s" is %s' % (obj[item_index], gender))
        material = inflect_adjective(make_adjective[of_material], gender, 'accs', animated=False)
        text = verb + " " + material + " " + ' '.join(obj)
    else:
        text = verb + " " + ' '.join(obj) + " " + of_material

    return text.capitalize()


def instrumental_case(word):
    # print("instrumental_case(%s)" % repr(word))
    assert ' ' not in word
    gender = get_gender(word)
    if gender is None:
        # print("Assuming gender of '%s' is masculine" % word)
        gender = 'masc'

    if is_adjective(word):
        word = inflect_adjective(word, gender, 'ablt')
    else:
        word = inflect_noun(word, 'ablt')

    return word


re_jewelers_shop = re.compile(r"^(Инкрустировать Готовые товары с"
                              r"|Инкрустировать Предметы обстановки с"
                              r"|Инкрустировать Снаряды с"
                              r"|Огранить)\s(.+)")


# Ювелирная мастерская
def corr_jewelers_shop(text):
    # print('corr_jewelers_shop')
    search_result = re_jewelers_shop.search(text)
    first_part = search_result.group(1)
    words = search_result.group(2).split()
    if first_part == "Огранить":
        # accusative case
        tags = None
        if words[0] == 'из':
            words = words[1:]
            tags = {'gent'}
        item = words[-1]
        gender = get_gender(item, known_tags=tags)
        # print(':', gender)
        words = [inflect_adjective(word, gender, 'accs', animated=False) for word in words[:-1]]
        parse = list(filter(lambda x: {gender, 'inan'} in x.tag, custom_parse(item)))
        if item == 'адамантина':
            item = 'адамантин'
        else:
            item = parse[0].inflect({'accs'}).word
        words.append(item)
    else:
        # instrumental/ablative case ('incrust with smth')
        words = [custom_parse(word)[0].inflect({'ablt'}).word for word in words if word != 'из']
    # print(words)
    if first_part.endswith(' с'):
        first_part = first_part[:-2]
    text = first_part + ' ' + ' '.join(words)
    return text.capitalize()


re_settlement = re.compile(r'(.*)\s(лесное убежище|крепость|селение|горный город|городок|гробница|пригорки)\s(.+)')


# убежище, крепость
def corr_settlement(text):
    # print("corr_settlement")
    search_result = re_settlement.search(text)
    adjective = search_result.group(1).strip()
    settlement = search_result.group(2)
    name = search_result.group(3)

    if len(adjective) == 0:
        return "%s %s" % (settlement.capitalize(), name.capitalize())

    if adjective in {'Покинуть', 'Разрушить'}:
        return

    gender = get_main_word_gender(settlement)

    if " " not in adjective:
        adjective_2 = inflect_adjective(adjective, gender)
    else:
        adjective_2 = " ".join(inflect_adjective(word, gender) for word in adjective.split(" "))

    if adjective_2 is None:
        adjective_2 = adjective

    return "%s %s %s" % (adjective_2.capitalize(), settlement, name.capitalize())


re_material_selection = re.compile(r'(металл|кожа|пряжа|растительное волокно|дерево|шёлк)\s(.+)')


# выбор материала
def corr_material_selection(text):
    # print(20)
    search_result = re_material_selection.search(text)
    if search_result.group(2) in phrases:
        new_word = phrases[search_result.group(2)]
    else:
        new_word = search_result.group(2)
    if search_result.group(1) == 'пряжа' or search_result.group(1) == 'растительное волокно':
        material = make_adjective[search_result.group(1)]
        text = new_word + " " + material
        return text.capitalize()
    gender = get_gender(new_word)
    material = make_adjective[search_result.group(1)][gender]
    text = material + " " + new_word
    return text.capitalize()


re_animal_material = re.compile(r'(.+)\s(кожа|кость|волокно|шёлк)\b')


# кожа, шерсть-длинные названия
def corr_animal_material(text):
    # print(21)
    search_result = re_animal_material.search(text)
    text = search_result.group(2) + " " + genitive_case(search_result.group(1))
    return text


re_stopped_construction = re.compile(r'(\w+) приостановили строительство (.*)\.')


def corr_stopped_construction(text):
    # print("corr_stopped_construction")
    search_result = re_stopped_construction.search(text)
    subj = search_result.group(1)
    obj = search_result.group(2)
    # print(obj)

    if 'Ремесленник мастерская' in obj:
        gen_case_obj = ' '.join(
            genitive_case(word) for word in reversed(obj.split()))  # Put words into genitive case separately
    else:
        gen_case_obj = genitive_case(obj)

    return ("%s приостановили строительство %s." % (subj, gen_case_obj)).capitalize()


# Корректировка для окончания s - перевод существительного во множественное число или глагола в 3-е лицо ед.ч.
re_ending_s = re.compile(r'(\d+\s)?([а-яёА-ЯЁ][а-яёА-ЯЁ\s]*)e?s\b')


def corr_ending_s_internal(text):
    parse = [x for x in custom_parse(text)
             if {'NOUN', 'nomn', 'sing'} in x.tag or {'VERB', '2per'} in x.tag]

    if not parse:
        # print('Cannot determine part of speech of %r' % s)
        return None

    new_forms = set()
    for item in parse:  # FIXME: unused variable item
        if parse[0].tag.POS == 'NOUN':
            new_forms.add(parse[0].inflect({'plur'}).word)
        else:  # parse[0].tag.POS == 'VERB':
            new_forms.add(parse[0].inflect({'3per', 'sing'}).word)

    if len(new_forms) > 1:
        # print('Cannot determine part of speech of %r because of ambiguity:' % s)
        # print(parse)
        return None

    return new_forms.pop()


def corr_ending_s(text):
    # print("corr_ending_s")
    search_result = re_ending_s.search(text)
    number = search_result.group(1)
    group2 = search_result.group(2)
    if number and ' ' not in group2:
        number = int(number)
        parse = [x for x in custom_parse(group2) if {'NOUN', 'nomn', 'sing'} in x.tag]
        # print(parse)
        assert len(parse) == 1
        replacement_string = '%d %s' % (number, parse[0].make_agree_with_number(number).word)
    elif group2 in dict_ending_s:
        replacement_string = dict_ending_s[group2]
    elif ' ' not in group2:
        new_form = corr_ending_s_internal(group2)
        if new_form:
            replacement_string = new_form
        else:
            # print("Couldn't find correct -s form for %s." % group2)
            return None
    else:
        words = group2.split()
        if words[-1] in dict_ending_s:
            words[-1] = dict_ending_s[words[-1]]
            replacement_string = ' '.join(words)
        else:
            new_form = corr_ending_s_internal(words[-1])
            if new_form:
                words[-1] = new_form
                replacement_string = ' '.join(words)
            else:
                # print("Couldn't find correct -s form for %s." % words[-1])
                return None

    return text.replace(search_result.group(0), replacement_string)


# Clothier's shop

re_clothiers_shop = re.compile(r'(Делать|Изготовить|Вышивать|Ткать) (ткань|шёлк|пряжа|кожа)(\s?\w*)')

cloth_subst = {
    "ткань": ("Шить", "из ткани"),
    "шёлк": ("Шить", "шёлковый"),
    "пряжа": ("Вязать", "из пряжи"),
    "кожа": ("Шить", "из кожи"),
}


def corr_clothiers_shop(text):
    # print("Corr clothier's/leather shop")
    search_result = re_clothiers_shop.search(text)
    verb = search_result.group(1)
    material = search_result.group(2)
    product = search_result.group(3).strip()

    if not product:
        return None  # Leave as is eg. 'Ткать шёлк'
    elif verb == 'Вышивать':
        parse = custom_parse(material)[0]
        if material == 'пряжа':
            verb = 'Вязать'
            material = parse.inflect({'gent'}).word
            return '%s %s из %s' % (verb, product, material)
        else:
            material = parse.inflect({'loct'}).word
            return '%s %s на %s' % (verb, product, material)
    else:
        if product in {'щит', 'баклер'}:
            of_material = cloth_subst[material][1]  # Leave 'Делать'/'Изготовить' verb
        else:
            verb, of_material = cloth_subst[material]

        if product == "верёвка":
            verb = "Вить"

        gender = get_gender(product, {'nomn'})
        if gender == 'femn':
            product_accus = inflect_noun(product, case='accs')
        else:
            product_accus = product

        if material in make_adjective:
            material_adj = inflect_adjective(make_adjective[material], gender, 'accs', animated=False)
            return ' '.join([verb, material_adj, product_accus])
        else:
            return ' '.join([verb, product_accus, of_material])


re_werebeast = re.compile(r"были(\w+)")


def corr_werebeast(text):
    search_result = re_werebeast.search(text)
    return text.replace(search_result.group(0), search_result.group(1) + "-оборотень")


re_become = re.compile(r"(.+)\s(стал)\s(.+)\.")


def corr_become(text):
    # print("corr_become")
    search_result = re_become.search(text)
    subj = search_result.group(1)
    verb = search_result.group(2)
    # print(verb)
    words = search_result.group(3)
    words = inflect_collocation(words, {'ablt'})
    if subj.startswith('Животное'):
        return "Животное выросло и стало %s." % words
    else:
        return "%s %s %s." % (subj, verb, words)


re_with_his = re.compile(r'(с (его|её|ваш) (.*))[!]')


def corr_with_his(text):
    # print("corr_with_his")
    search_result = re_with_his.search(text)
    return text.replace(search_result.group(1), "своим %s" % (inflect_collocation(search_result.group(3), {'ablt'})))


re_rings = re.compile(r"([\w\s]+) (кольцо|кольца)")


def corr_rings(text):
    # print("corr_rings")
    search_result = re_rings.search(text)
    obj = search_result.group(2)
    description = search_result.group(1)
    return text.replace(search_result.group(0), "%s из %s" % (obj, genitive_case(description)))


# Title eg. "Histories of Greed and Avarice" for the Linux version
histories_adjs = {
    'Greed': ' жадности',
    'Avarice': 'б алчности',
    'Jealousy': ' зависти',
    'Cupidity': ' скупости',
    'Gluttony': 'б обжорстве',
    'Industry': 'производстве',
    'Enterprise': 'предприимчивости',
    'Resourcefulness': 'находчивости',
    'Determination': 'решительности',
    'Mettle': 'отваге',
    'Dynamism': 'стремительности',
    'Labor': 'работе',
    'Toil': 'труде',
    'Diligence': 'усердии',
    'Exertion': 'напряжении',
    'Tenacity': 'стойкости',
    'Perseverance': 'упорстве',
}

re_histories_of = re.compile(r"Histories of (\w+) and (\w+)")


def corr_histories_of(text):
    search_result = re_histories_of.search(text)
    return 'Истории о%s и %s' % (histories_adjs[search_result.group(1)], histories_adjs[search_result.group(2)])


def corr_well(text):
    """
    >>> corr_well('Я колодец')  # I am well
    'Я в порядке'
    
    >>> corr_well('Я чувствую колодец')  # I am feeling well
    'Я чувствую себя хорошо'
    """
    text = text.replace('колодец', 'хорошо')
    if 'чувствую' in text and 'себя' not in text:
        text = text.replace('чувствую', 'чувствую себя')
    elif 'делаю хорошо' in text:
        text = text.replace('делаю хорошо', 'в порядке')
    elif 'был хорошо' in text:
        text = text.replace('был хорошо', 'в порядке')
    elif 'хорошо' in text:
        text = text.replace('хорошо', 'в порядке')
    return text


def corr_minced(text):
    s1 = ''
    while 'рублены' in text and 'рубленый' not in text:
        x, _, text = text.partition('рублены')
        s1 += x + 'рубленый '

    return s1 + text


def corr_you_struck(text):
    # print('corr_you_struck')
    i = text.find('из ')
    you_struck = text[:i]
    words = text[i:-1].split()
    assert len(words) == 2
    parse = custom_parse(words[1])
    return you_struck + parse[0].normal_form + '!'


re_someone_has = re.compile(r"(он|она|вы)\s+(не\s+)?(имеете?)", flags=re.IGNORECASE)


def corr_someone_has(text):
    search_result = re_someone_has.search(text)
    pronoun = search_result.group(1).lower()
    if pronoun == 'он':
        replacement_string = 'у него'
    elif pronoun == 'она':
        replacement_string = 'у неё'
    elif pronoun == 'вы':
        replacement_string = 'у вас'
    else:
        return text

    if search_result.group(0)[0].isupper():
        replacement_string = replacement_string.capitalize()

    if search_result.group(2):
        replacement_string += ' нет'

    text = text.replace(search_result.group(0), replacement_string)
    assert isinstance(text, str), text
    return text


re_has_verb = re.compile(r"(имеете?|был)\s+(\w+)")


def corr_has_verb(text):
    search_result = re_has_verb.search(text)
    if search_result:
        word = search_result.group(2)
        parse = [p for p in custom_parse(word) if p.tag.POS == 'VERB']
        if parse:
            if not any({'past'} in p.tag for p in parse):
                word = parse[0].inflect({'past'}).word
            return text.replace(search_result.group(0), word)


re_in_ending = re.compile(r"[a-z](в <[a-z]+>)")


def corr_in_ending(text):
    search_result = re_in_ending.search(text)
    if search_result:
        return text.replace(search_result.group(1), 'in')


re_color_of_color = re.compile(r"цвет ([\w\s]*)цвета")


def corr_color_of_color(text):
    search_result = re_color_of_color.search(text)
    if search_result:
        if not search_result.group(1):
            replacement = "цвет"
        else:
            color = search_result.group(1).strip()
            replacement = '%s цвет' % inflect_collocation(color, {'nomn', 'masc'})
        return text.replace(search_result.group(0), replacement)


def tag_to_set(tag):
    return set(sum((ss.split() for ss in str(tag).split(',')), list()))


def common_tags(parse):
    common = tag_to_set(parse[0].tag)
    for p in parse[1:]:
        common &= tag_to_set(p.tag)
    return common


def get_form(word):
    common = common_tags(custom_parse(word))
    if 'plur' in common:
        common -= {'masc', 'femn', 'neut'}
    if 'masc' not in common:
        common -= {'anim', 'inan'}
    return {tag for tag in ['sing', 'plur', 'masc', 'femn', 'neut', 'anim', 'inan'] if tag in common}


def inflect_collocation(s, tags):
    # print('inflect_collocation(%r, %r)' % (s, tags))
    words = [x for x in s.split(' ') if x]  # skip empty strings
    j = None
    main_word = None
    for i, word in enumerate(words):
        parse = custom_parse(word)
        if any_in_tag({'NOUN'}, parse):
            p = next(p for p in parse if {'NOUN'} in p.tag)
            p = p.inflect(tags)
            words[i] = p.word if word[0].islower() else p.word.capitalize()
            j = i
            main_word = p
            break

    if main_word:
        if main_word.tag.number == 'plur':
            tags.add('plur')
        else:
            tags.add(main_word.tag.gender)

        if 'accs' in tags and 'plur' not in tags and 'masc' in tags:
            tags.add(main_word.tag.animacy)

    for i, word in enumerate(words[:j]):
        parse = custom_parse(word)
        if not is_adjective(word, parse):
            raise ValueError('%s is not an adjective' % word)
        p = next(p for p in parse if {'ADJF'} in p.tag)
        # print(p)
        # print(tags)
        p = p.inflect(tags)
        words[i] = p.word

    # print(words)
    return ' '.join(words) + (' ' if s.endswith(' ') else '')


def parse_tags(text):
    start = 0
    for i, c in enumerate(text):
        if c == '<':
            if start < i:
                yield text[start:i]
            start = i
        elif c == '>':
            yield text[start:i + 1]
            start = i + 1

    if start < len(text):
        yield text[start:]


re_sentence = re.compile(r'^([^\.!"]*)([\.!"].*)$')
re_split_enumeration = re.compile(r'(,| и )')


def is_enumeration_delimiter(text):
    return text in {',', ' и '}


def any_cyr(text):
    return any('а' <= x <= 'я' or x == 'ё' for x in text.lower())


re_number = re.compile(r'^(\d+)(.*)')


def cut_number(text):
    search_result = re_number.search(text)
    return search_result.group(1), search_result.group(2)


def smart_join(li):
    def add_spaces(text):
        add_space = False
        for part in text:
            part = part.strip()
            if part:
                if add_space and part[0].isalnum():
                    part = ' ' + part

                yield part
                if part[-1] not in set('"('):
                    add_space = True

    return ''.join(add_spaces(li))


def _inflect_enumeration(text, form):
    do_not_inflect = False
    for part in re_split_enumeration.split(text):
        if is_enumeration_delimiter(part) or do_not_inflect:
            yield part
        else:
            try:
                part = inflect_collocation(part, form)
            except ValueError:
                do_not_inflect = True
            yield part


def inflect_enumeration(s, form):
    li = list(_inflect_enumeration(s, form))
    # print(li)
    return smart_join(li)


def corr_tags(text):
    global prev_tail
    # print('corr_tags(%r)' % s)
    li = []
    get_index = None
    set_indices = set()
    capitalize_indices = set()
    inflect_next = set()
    for i, item in enumerate(parse_tags(text)):
        # print(repr(item))
        if not item.strip():
            pass
        elif item[0] == '<':
            item = item.strip('<>')
            if not item:
                return None
            tags, _, item = item.partition(':')
            tags = set(tags.split(','))
            # print(tags)

            if 'capitalize' in tags:
                tags.remove('capitalize')
                capitalize_indices.add(len(li))

            if item:
                # Inflect the word inside the tag after the colon
                word = item.strip()

                if 'get-form' in tags:
                    if get_index is not None:
                        raise ValueError('Duplicate <get-form> tag in %r' % text)
                    get_index = len(li)
                    tags.remove('get-form')
                elif 'set-form' in tags:
                    set_indices.add(len(li))
                    tags.remove('set-form')

                if tags:
                    if ' ' in word:
                        item = inflect_collocation(word, tags)
                    else:
                        p = custom_parse(word)[0]
                        item = p.inflect(tags).word
                        # if not make_lower and word[0].isupper():
                        if word[0].isupper():
                            item = item.capitalize()
                else:
                    # item = word if not make_lower else word.lower()
                    item = word
            else:
                # Inflect a part of text after the tag till the ending point of the sentence.
                inflect_next = tags
                continue
        elif inflect_next:
            sentence = re_sentence.search(item)
            if sentence:
                item = sentence.group(1)
                tail = sentence.group(2)
            else:
                tail = ''
            item = item.lstrip(' ')
            if not any_cyr(item.split(' ')[0]):
                if item.strip()[0].isdigit():
                    if 'loct' in tags:  # FIXME: possible uninitialized variable tags
                        tags.remove('loct')
                        tags.add('loc2')  # inflect into 'году' instead of 'годе'
                    item, tail1 = cut_number(item)
                    item += ' ' + custom_parse('год')[0].inflect(inflect_next).word + tail1.lstrip(',')
                elif (not li or not any_cyr(li[-1].rstrip().split(' ')[-1])) and tags == {'gent'}:
                    li.append('of ')
                pass
            else:
                if ',' in item:
                    item = inflect_enumeration(item, inflect_next)
                elif ' ' in item:
                    item = inflect_collocation(item, inflect_next)
                else:
                    p = custom_parse(item)[0]
                    item = p.inflect(tags).word
            item += tail
            inflect_next = set()
        else:
            pass
        li.append(item)

    delayed = ''
    if inflect_next:
        delayed += '<%s>' % ','.join(inflect_next)
        # print('Delay to the next string: %r' % prev_tail)

    if get_index is not None:
        # print(get_index)
        form = get_form(li[get_index])
        form -= {'anim', 'inan'}  # discard these two because they doesn't matter for the nominal case
        # print(form)
        for i in set_indices:
            word = li[i]
            if ' ' in word:
                item = inflect_collocation(word, form)
            else:
                p = custom_parse(word)[0]
                item = p.inflect(form).word
                if word[0].isupper():
                    item = item.capitalize()
            li[i] = item

    if capitalize_indices:
        for i in capitalize_indices:
            if i >= len(li):
                delayed += '<capitalize>'
            else:
                for part in li[i].split():
                    if part:
                        li[i] = li[i].replace(part, part.capitalize(), 1)
                        break

    if delayed:
        # print('Delay to the next string: %r' % delayed)
        prev_tail += delayed

    # print(li)
    return smart_join(li)


contexts = {
    '  Dwarf Fortress  ': 'main',
    'Овощи/фрукты/листья': 'kitchen',
    re.compile(r'Граждане \(\d+\)'): 'units',
    'Создано:': 'status',
}

contextual_replace = dict(
    kitchen={'Повар': 'Готовить'},
    units={'Рыба': 'Рыбачить'},
)


def corr_contextual(text):
    global context
    if text in contexts:
        context = contexts[text]
    else:
        for pattern in contexts:
            if not isinstance(pattern, str) and pattern.search(text):
                context = contexts[pattern]
                break

    current_context = context
    if context and context in contextual_replace:
        return contextual_replace[context].get(text, None)


############################################################################
class Logger:
    def __init__(self):
        self.logged = set()
        self.log_file = open('changetext.log', 'a', 1, encoding='utf-8')

    def write(self, text, output):
        if text not in self.logged:
            print('%r --> %r' % (text, output), file=self.log_file)
            self.log_file.flush()
            self.logged.add(text)


@functools.lru_cache()
def get_logger():
    return Logger()


prev_tail = ''
context = None


def init():
    global prev_tail, context

    prev_tail = ''
    context = None


init()


def change_text(text):
    global prev_tail
    if prev_tail:
        text = prev_tail + text
        prev_tail = ''

    result = None
    # preprocessing:
    if text in phrases:
        result = phrases[text]

    while re_ending_s.search(text):
        s1 = corr_ending_s(text)
        if s1 is None:
            break
        text = s1
        result = text

    if re_werebeast.search(text):
        text = corr_werebeast(text)
        result = text
    if re_with_his.search(text):
        text = corr_with_his(text)
        result = text

    if 'Я ' in text and 'колодец' in text:
        text = corr_well(text)
        result = text

    if 'рублены' in text and 'рубленый ' not in text:
        text = corr_minced(text)
        result = text

    for item in replaced_parts:
        if item in text:
            text = text.replace(item, replaced_parts[item])
            result = text

    result = corr_in_ending(text) or result
    if result:
        text = result

    result = corr_contextual(text) or result
    if result:
        text = result

    if re_animal_gender.search(text):
        new_string = corr_animal_gender(text)
        if new_string is not None:
            text = new_string
            result = text

    if re_someone_has.search(text):
        text = corr_someone_has(text)
        result = text

    result = corr_has_verb(text) or result
    if result:
        text = result

    result = corr_color_of_color(text) or result
    if result:
        text = result

    if '<' in text and '>' in text and '<нет ' not in text and not '<#' in text:
        try:
            result = corr_tags(text)
        except (AssertionError, ValueError) as err:
            print('corr_tags() raises exception %r:' % err)
            print(traceback.format_exc())
            result = ' '.join(part.strip(' ') if not part.startswith('<')
                              else part.strip('<>').partition(':')[2]
                              for part in parse_tags(text))
    elif re_histories_of.search(text):
        result = corr_histories_of(text)
    elif re_container.search(text):
        result = corr_container(text)
    elif re_item_general.search(text) and 'пол' not in text:
        print('re_item_general passed')
        result = corr_item_general(text)
    elif re_clothes.search(text):
        result = corr_clothes(text)
    elif re_prepared.search(text):
        result = corr_prepared(text)
    elif re_skin.search(text):
        result = corr_item_skin(text)
    elif re_forge.search(text):
        result = corr_forge(text)
    elif re_weapon_trap_parts.search(text):
        result = corr_weapon_trap_parts(text)
    elif re_3.search(text):
        result = corr_item_3(text)
    elif re_wooden_logs.search(text):
        result = corr_wooden_logs(text)
    elif re_craft_glass.search(text):
        result = corr_craft_glass(text)
    elif re_gem_cutting.search(text):
        result = corr_gem_cutting(text)
    elif re_animal.search(text):
        result = corr_animal(text)
    elif re_stopped_construction.search(text):
        result = corr_stopped_construction(text)
    elif re_corr_relief.search(text):
        result = corr_relief(text)
    elif re_13_1.search(text):
        result = corr_item_13(text)
    elif re_jewelers_shop.search(text):
        result = corr_jewelers_shop(text)
    elif re_settlement.search(text):
        result = corr_settlement(text)
        # elif re_material_selection.search(text): # Отключено: дает ложные срабатывания в логе
        # result = corr_material_selection(text)
    elif re_clothiers_shop.search(text):
        result = corr_clothiers_shop(text)
    elif re_craft_general.search(text):
        result = corr_craft_general(text)
    elif re_body_parts.search(text):
        result = corr_item_body_parts(text)
    elif re_animal_material.search(text):
        result = corr_animal_material(text)
    elif re_rings.search(text):
        result = corr_rings(text)
    elif text.startswith('Вы нашли из '):
        result = corr_you_struck(text)
    elif re_become.search(text):
        result = corr_become(text)

    assert result != ''  # Empty string may cause game crash
    return result


def utf16_codec(func):
    @functools.wraps(func)
    def wrapper(data):
        if isinstance(data, bytes):
            data = data.decode("utf-16-le")
            output = func(data)
            return output if output is None else output.encode("utf-16-le") + b"\0\0"
        else:
            return func(data)

    return wrapper


def log_exceptions_and_result(func):
    @functools.wraps(func)
    def wrapper(text):
        try:
            result = func(text)
        except Exception:
            if sys.stdout:
                sys.stdout.flush()
            print('An error occurred.', file=sys.stderr)
            print('Initial string: %r' % text, file=sys.stderr)
            print(traceback.format_exc(), file=sys.stderr)
            print("", file=sys.stderr)
            result = None

        get_logger().write(text, result)

        return result

    return wrapper


@utf16_codec
@log_exceptions_and_result
def ChangeText(text):
    return change_text(text)
