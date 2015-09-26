import sys
import re
import traceback
from collections import OrderedDict

import pymorphy2

morph = pymorphy2.MorphAnalyzer()

try:
    from tests import test_strings
except ImportError:
    print("Failed to import tests. Skipping.")
    test_strings = None

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
    'As of June 2012, you can get help at the fan-created dwarffortresswiki.org.':  # TODO: make independent to the year number
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
    'Пова': 'Готовить',
    'Вари': 'Пиво',

    # реагенты
    'сырой рыба': 'свежая рыба',

    'Ничего не ловится в центре  болотах.': 'Ничего не ловится в центральных болотах.',
    'Ничего не ловится в востоке болотах.': 'Ничего не ловится в восточных болотах.',

    'NEW': 'НОВОЕ',
}

replaced_parts = OrderedDict([
    ("Ремесленникство", "мастерство"),
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
])


############################################################################
# роды - значения не менять, т.к. используются как индексы
masculine = 0  # м. род
feminine = 1  # ж. род
neuter = 2  # ср. род
plural = 3  # мн. ч.

gender_names = ('masc', 'femn', 'neut', 'plur')

# падежи
nominative = 0  # именительный
genitive = 1  # родительный
dative = 2  # дательный
accusative = 3  # винительный
instrumental = 4  # творительный
ablative = instrumental
prepositional = 5  # предложный
locative = prepositional

case_names = ("nomn", "gent", "datv", "accs", "ablt", "loct")

gender_item = {
    # предметы
    # masculine
    "тренировочный топор": masculine, "щит": masculine, "баклер": masculine,
    "стол": masculine, "трон": masculine, "горшок": masculine, "шкаф": masculine,
    "ларец": masculine, "гроб": masculine, "игрушечный кораблик": masculine,
    "игрушечный молоток": masculine, "игрушечный топорик": masculine,
    "кубок": masculine, "костыль": masculine, "шлем": masculine,
    "капюшон": masculine, "сапог": masculine, "ботинок": masculine, "башмак": masculine,
    "песок": masculine, "кувшин": masculine, "барабан": masculine, "стул": masculine,
    "мешок": masculine, "боевой топор": masculine, "короткий меч": masculine,
    "тренировочный меч": masculine, "арбалет": masculine, "боевой молот": masculine,
    "амулет": masculine, "нагрудник": masculine, "инструмент": masculine,
    "улей": masculine, "рюкзак": masculine, "жилет": masculine, "плащ": masculine, "носок": masculine,
    "колчан": masculine, "силок": masculine, "шлюз": masculine, "люк": masculine, "сундук": masculine,
    "саркофаг": masculine, "ящик": masculine, "мемориал": masculine,
    "головной убор": masculine, "кинжал": masculine, "болт": masculine, "рычаг": masculine,

    # feminine
    "кирка": feminine, "наковальня": feminine, "булава": feminine,
    "кружка": feminine, "кровать": feminine, "головоломка": feminine,
    "статуя": feminine, "бочка": feminine, "дверь": feminine,
    "мини-кузница": feminine, "шина": feminine, "статуэтка": feminine,
    "кольчуга": feminine, "шапка": feminine, "вагонетка": feminine, "тачка": feminine,
    "труба": feminine, "арфа": feminine, "флейта-пикколо": feminine,
    "корона": feminine, "перчатка": feminine, "Клетка": feminine, "клетка": feminine,
    "стойка": feminine, "решётка": feminine, "туника": feminine, "цепь": feminine,
    "броня": feminine, "обувь": feminine, "крышка": feminine, "звезда": feminine,
    "бирюза": feminine,

    # neuter
    "тренировочное копьё": neuter, "гнездо": neuter, "ведро": neuter, "копьё": neuter,
    "кольцо": neuter, "Ведро": neuter,
    # plural
    "кирки": plural, "тренировочные топоры": plural, "наковальни": plural, "булавы": plural,
    "копья": plural, "кружки": plural, "стулья": plural,
    "боевые топоры": plural, "болты": plural, "боевые молоты": plural, "топоры": plural,
    "арбалеты": plural, "щиты": plural, "рукавицы": plural, "поножи": plural,
    "нагрудники": plural, "брёвна": plural, "тренировочные мечи": plural,
    "цереуса": plural, "ведра": plural, "гробы": plural, "молотки": plural,
    "статуи": plural, "ларцы": plural, "механизмы": plural, "головоломки": plural,
    "игрушечные кораблики": plural, "столы": plural, "кольчужный": plural,
    "ларецы": plural, "тренировочные копья": plural, "флейты-пикколо": plural,
    "игрушечные молотки": plural, "игрушечные топорики": plural,
    "мини-кузницы": plural, "стрелы": plural, "дротики": plural, "баклеры": plural,
    "короткие мечи": plural, "мечи": plural, "слитки": plural, "шины": plural, "костыли": plural, "бочки": plural,
    "клетки": plural, "ульи": plural, "горшки": plural, "гнёзда": plural, "вёдра": plural,
    "фляги": plural, "бурдюки": plural, "блоки": plural, "барабаны": plural,
    "браслеты": plural, "скипетры": plural, "короны": plural, "статуэтки": plural, "кольца": plural,
    "серьги": plural, "колчаны": plural, "рюкзаки": plural, "мешоки": plural,
    "верёвки": plural, "кольчуги": plural, "шлемы": plural, "одежды": plural,
    "шапки": plural, "капюшоны": plural, "сапоги": plural, "ботинки": plural, "башмаки": plural,
    "рейтузы": plural, "штаны": plural, "амулеты": plural, "кувшины": plural,
    "вагонетки": plural, "тачки": plural, "флейты": plural, "трубы": plural, "арфы": plural, "Поделки": plural,
    "монеты": plural, "Блоки": plural, "Наконечники стрел": plural, "шкафы": plural, "двери": plural,
    "кровати": plural, "жернова": plural, "троны": plural, "стойки": plural, "сундуки": plural, "изделия": plural,
    "перчатки": plural, "брюки": plural, "доспехи": plural, "щиты/баклеры": plural, "плащи": plural,
    "рубахи": plural, "накидки": plural, "робы": plural, "жилеты": plural, "туники": plural, "тоги": plural,

    # самоцветы
    # masculine
    "хрусталь": masculine, "морганит": masculine, "кошачий глаз": masculine, "опал": masculine,
    # feminine
    "яшма": feminine, "шпинель": feminine, "тигровая яшма": feminine,
    # neuter

    # plural
    "шерлы": plural, "прозапалы": plural, "кровавики": plural, "моховые агаты": plural, "хризопразы": plural,
    "сердолики": plural,
    "изысканные огненные опалы": plural, "костяные опалы": plural, "моховые опалы": plural,
    "молочные кварцы": plural, "цитрины": plural, "пириты": plural, "зелёные турмалины": plural,
    "белые халцедоны": plural, "лунные камни": plural, "красные пиропы": plural,
    "синие гранаты": plural, "чёрные цирконы": plural, "демантоиды": plural, "биксбиты": plural, "топазы": plural,
    "кунциты": plural, "фиолетовые спессартины": plural,
    "гелиодоры": plural, "гошениты": plural, "аметисты": plural, "аквамарины": plural, "хризобериллы": plural,
    "арлекины": plural,
    "изумруды": plural, "александриты": plural, "морионы": plural, "лазуриты": plural, "празеолиты": plural,
    "лавандовые нефриты": plural,
    "розовые нефриты": plural, "восковые опалы": plural, "янтарные опалы": plural, "золотистые опалы": plural,
    "ракушечные опалы": plural,
    "авантюрины": plural, "альмандины": plural, "родолиты": plural, "танзаниты": plural, "золотистые бериллы": plural,
    "топазолиты": plural,
    "светло-жёлтые алмазы": plural, "рубицеллы": plural, "сардониксы": plural, "белые нефриты": plural,
    "ананасовые опалы": plural,
    "трубчатые опалы": plural, "розовые кварцы": plural, "зелёные цирконы": plural, "зелёные нефриты": plural,
    "красные цирконы": plural,
    "яшмовые опалы": plural, "розовые турмалины": plural, "огненные опалы": plural, "желейные опалы": plural,
    "коричневые цирконы": plural, "жёлтые цирконы": plural, "жёлтые спессартины": plural, "чистые гранаты": plural,
    "чистые цирконы": plural, "чёрные опалы": plural, "кристаллические опалы": plural,
    "слоистые огненные опалы": plural,
    "дымчатые кварцы": plural, "смолистые опалы": plural, "светло": plural, "розовые опалы": plural,
    "розовые перриты": plural,
    # masculine
    "кол": masculine, "винт": masculine, "шар": masculine, "диск": masculine,
    # neuter
    "лезвие топора": neuter,
    # plural
    "колья": plural, "шары": plural, "винты": plural, "диски": plural, "лезвия топоров": plural,

    # Травы
    "морошка": feminine,

    "червь": masculine,
    "коза": feminine,
    "галька": feminine
}

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
}

adjective_endings_masculine = {"ый", "ой", "ий"}

adjective_cases = {
    "ый":  # медный, шелковый etc.
    (
        ("ый", "ая", "ое", "ые"),  # именительный - nominative
        ("ого", "ой", "ого", "ых"),  # родительный - genitive
        ("ому", "ой", "ому", "ым"),  # дательный - dative
        ("ый", "ую", "ое", "ые"),  # винительный  - accusative
        ("ым", "ой", "ым", "ыми"),  # творительный  - instrumental
        ("ом", "ой", "ом", "ых"),  # предложный  - prepositional
    ),
    "ой":  # золотой, густой etc.
    (
        ("ой", "ая", "ое", "ые"),  # именительный - nominative
        ("ого", "ой", "ого", "ых"),  # родительный - genitive
        ("ому", "ой", "ому", "ым"),  # дательный - dative
        ("ого", "ую", "ое", "ых"),  # винительный  - accusative
        ("ым", "ой", "ым", "ыми"),  # творительный  - instrumental
        ("ом", "ой", "ом", "ых"),  # предложный  - prepositional
    ),
    "шой":  # большой etc.
    (
        ("шой", "шая", "шое", "шие"),  # именительный - nominative
        ("шого", "шой", "шого", "ших"),  # родительный - genitive
        ("шому", "шой", "шому", "шим"),  # дательный - dative
        ("шого", "шую", "шое", "ших"),  # винительный  - accusative
        ("шим", "шой", "шим", "шими"),  # творительный  - instrumental
        ("шом", "шой", "шом", "ших"),  # предложный  - prepositional
    ),
    "ний":  # синий etc.
    (
        ("ний", "няя", "нее", "ние"),  # именительный - nominative
        ("него", "нюю", "нее", "них"),  # родительный - genitive
        ("нему", "ней", "нему", "ним"),  # дательный - dative
        ("него", "нюю", "нее", "них"),  # винительный  - accusative
        ("ним", "ней", "ним", "ними"),  # творительный  - instrumental
        ("нем", "ней", "нем", "них"),  # предложный  - prepositional
    ),
    "кий":  # гигантский, высокий etc.
    (
        ("кий", "кая", "кое", "кие"),  # именительный - nominative
        ("кого", "кой", "кого", "ких"),  # родительный - genitive
        ("кому", "кой", "кому", "ким"),  # дательный - dative
        ("кого", "кую", "кое", "ких"),  # винительный  - accusative
        ("ким", "кой", "ким", "кими"),  # творительный  - instrumental
        ("ком", "кой", "ком", "ких"),  # предложный  - prepositional
    ),
    "жий":  # рыжий etc.
    (
        ("жий", "жая", "жее", "жие"),  # именительный - nominative
        ("жего", "жей", "жего", "жих"),  # родительный - genitive
        ("жему", "жей", "жему", "жим"),  # дательный - dative
        ("жего", "жую", "жее", "жих"),  # винительный  - accusative
        ("жим", "жей", "жим", "жими"),  # творительный  - instrumental
        ("жем", "жей", "жем", "жих"),  # предложный  - prepositional
    ),
    "чий":  # летучий etc.
    (
        ("чий", "чая", "чее", "чие"),  # именительный - nominative
        ("чего", "чей", "чего", "чих"),  # родительный - genitive
        ("чему", "чей", "чему", "чим"),  # дательный - dative
        ("чего", "чую", "чее", "чих"),  # винительный  - accusative
        ("чим", "чей", "чим", "чими"),  # творительный  - instrumental
        ("чем", "чей", "чем", "чих"),  # предложный  - prepositional
    ),
}

accusative_case = {
    'булава': "булаву",
    'кирка': "кирку",
    'кольчуга': "кольчугу",
    'шапка': "шапку",
    'рукавица': "рукавицу",
    'наковальню': "наковальню",
    'игрушку': "игрушку",
    'вагонетка': "вагонетку",
    'тачка': "тачку",
    'флягу': "флягу",
    'одежда': "одежду",
    'рубаха': "рубуху",
    'роба': "робу",
    'варежка': "варежку",
    'бочка': "бочку",
    'доспешная стойка': "доспешную стойку",
    'статуя': "статую",
    'оружейная стойка': "оружейную стойку",
    'Секция трубы': "секцию трубы",
    'перчатка': "перчатку",
    'клетку': "клетку",
    'туника': "тунику",
    'ловушка для': "ловушку для",
    'дверь': "дверь",
    'цепь': "цепь",
    'решетку': "решетку",
    'шину': "шину",
}

ending_fem = {
    "ва", "ца", "ма", "ия", "на", "ха", "ка", "ба", "да",
    "шь", "чь", "жь"
}

ending_masc = {
    "ск", "ой", "ал", "ат", "ик", "ир", "ут"
}

ending_neut = {}

ending_plur = {"ны", "лы", "ы"}

dict_ending_s = {
    'готовая еда': 'готовая еда',
    'питьё': 'питьё',
    'ведро': 'вёдра',
    'верёвка': 'верёвки',
    'шина': 'шины',
    'костыль': 'костыли',
    'колчан': 'колчаны',
    'рюкзак': 'рюкзаки',
    'наковальня': 'наковальни',
    'доспешная стойка': 'доспешные стойки',
    'оружейная стойка': 'оружейные стойки',
    'дверь': 'двери',
    'шлюз': 'шлюзы',
    'кровать': 'кровати',
    'трон': 'троны',
    'стул': 'стулья',
    'гроб': 'гробы',
    'статуя': 'статуи',
    'дублёная шкура': 'дублёные шкуры',
    'большой самоцвет': 'большие самоцветы',
    'монета': 'монеты',
    'мемориал': 'мемориалы',
    'шкаф': 'шкафы',
    'стол': 'столы',
    'оружие': 'оружие',
    'сундук': 'сундуки',
    'щит': 'щиты',  #
    'баклер': 'баклеры',  #
    'мешок': 'мешки',
    'ларец': 'ларцы',
    'кружка': 'кружки',
    'капкан': 'капканы',
    'животное': 'животные',
    'крышка люка': 'крышки люка',
    'решётка': 'решётки',
    'ручная мельница': 'ручные мельницы',
    'жёрнов': 'жернова',
    'окно': 'окна',
    'ловушка для животных': 'ловушки для животных',
    'цепь': 'цепи',
    'клетка': 'клетки',
    'контейнер': 'контейнеры',
    'ящик': 'ящики',
    'бочка': 'бочки',
    'часть ловушки': 'части ловушек',
    'фляга': 'фляги',
    'кубок': 'кубки',
    'игрушка': 'игрушки',
    'инструмент': 'инструменты',
    'музыкальный инструмент': 'музыкальные инструменты',
    'статуэтка': 'статуэтки',
    'амулет': 'амулеты',
    'скипетр': 'скипетры',
    'корона': 'короны',
    'кольцо': 'кольца',
    'серьга': 'серьги',
    'браслет': 'браслеты',
    'бурдюк': 'бурдюки',
    'наконечник стрелы баллисты': 'наконечники стрелы баллисты',
    'тотем': 'тотемы',
    'труп': 'трупы',
    'часть тела': 'части тела',
    'конечность/тело гипс': 'гипс для конечностей тела',
    'душите': 'душит',  # strangle - strangles
    'ребро': 'рёбра',
    'инженер': 'инженеры',
    'егерь': 'егеря',
    'шахтёр': 'шахтёры',
    'кузнец': 'кузнецы',
    'камнерез': 'камнерезы',
    'ювелир': 'ювелиры',
    'рыбник': 'рыбники',
    'фермер': 'фермеры',
    'борец': 'борцы',
    'Элитный борец': 'Элитные борцы',
    'Лорд топора': 'Лорды топора',
    'Лорд булавы': 'Лорды булавы',
    'Лорд молота': 'Лорды молота',
    'Мастер меча': 'Мастера меча',
    'Мастер копья': 'Мастера копья',
    'очко': 'очков'
}

pm_genders = {'masc': masculine, 'femn': feminine, 'neut': neuter, 'plur': plural, None: None}


def pm_gender(parse):
    tag = parse.tag
    print(tag)
    if tag.number == 'plur':
        gender = tag.number
    else:
        gender = tag.gender
    print(gender)
    return pm_genders[gender]


def legacy_gender(obj):
    if obj in gender_item:
        return gender_item[obj]
    elif len(obj) >= 2:
        ending2 = obj[-2:]
        ending1 = obj[-1:]
        if ending2 in ending_masc:
            return masculine
        elif ending2 in ending_fem:
            return feminine
        elif ending2 in ending_neut:
            return neuter
        elif ending2 in ending_plur or ending1 in ending_plur:
            return plural
    print("Gender not recognized for '%s'" % obj)
    return None


def most_probable(parse, score=None):
    if score is None:
        score = parse[0].score
    for p in parse:
        assert score >= p.score
        if score - p.score > 1e-5:
            break
        yield p


gender_exceptions = {'шпинель'}


def get_gender(obj, cases=None):
    def is_suitable(parse):
        if len(parse) >= 2 and parse[0].score > parse[1].score:
            return True
        score = parse[0].score
        gender = pm_gender(parse[0])
        for p in most_probable(parse[1:], score):
            if pm_gender(p) != gender:
                return False
        return True

    print("get_gender('%s')" % obj)
    parse = morph.parse(obj)
    if cases is not None:
        parse = list(filter(lambda x: any(case_names[case] in x.tag for case in cases), parse))
    if obj not in gender_exceptions and is_suitable(parse):
        print('pymorphy2 method')
        return pm_gender(parse[0])
    else:
        print('Using legacy method')
        return legacy_gender(obj)


import heapq


# Cut'n'paste from pymorphy2 with some modifications to ignore forms with extra tags
def custom_inflect(form, required_grammemes):
    self = form._morph
    possible_results = [f for f in self.get_lexeme(form)
                        if required_grammemes <= f[1].grammemes]

    if not possible_results:
        required_grammemes = self.TagClass.fix_rare_cases(required_grammemes)
        possible_results = [f for f in self.get_lexeme(form)
                            if required_grammemes <= f[1].grammemes]

    grammemes = form[1].updated_grammemes(required_grammemes)

    def similarity(frm):
        tag = frm[1]
        return len(grammemes & tag.grammemes) - len(grammemes ^ tag.grammemes) * 0.1  # The more extra tags, the less the similarity
    res = heapq.nlargest(1, possible_results, key=similarity)
    return None if not res else res[0]


adj_except = {
    # 'заснеженный',  # склоняет как разговорное - "заснежённый", нужно - "заснеженный"
    # 'заточенный',  # склоняет как разговорное - "заточённый"
}


def inflect_adjective(adjective, gender, case=nominative, animated=None):
    print('inflect_adjective(%s, %s)' % (adjective, case_names[case]))
    if adjective.lower() in adj_except:
        ending3 = adjective[-3:]
        ending2 = adjective[-2:]
        if ending3 in adjective_cases:
            return adjective[:-3] + adjective_cases[ending3][case][gender]
        elif ending2 in adjective_cases:
            return adjective[:-2] + adjective_cases[ending2][case][gender]
        print("Failed to declinate '%s' to the %s case." % (adjective, case_names[case]))
        return None
    else:
        assert gender is not None
        parse = morph.parse(adjective)
        parse = [p for p in parse if 'ADJF' in p.tag or 'PRTF' in p.tag]
        assert len(parse) > 0
        parse = parse[0]
        form_set = {gender_names[gender], case_names[case]}
        if animated is not None and gender in {masculine, plural}:
            form_set.add('anim' if animated else 'inan')
        print('form_set:', form_set)
        new_form = custom_inflect(parse, form_set)
        if new_form is None:
            form_set = {gender_names[gender], case_names[case]}
            print('form_set:', form_set)
            new_form = custom_inflect(parse, form_set)
        ret = new_form.word
        print('%s -> %s' % (adjective, ret))
        return ret


# существительные+ прилаг
endings_to_genitive = {
    'ца': 'цы', 'ма': 'мы', 'ка': 'ки', 'фа': 'фы', 'ба': 'бы', 'са': 'сы',
    'ья': 'ьи', 'на': 'ны', 'да': 'ды', 'ха': 'хи', 'ва': 'вы', 'за': 'зы',
    'га': 'ги', 'ра': 'ры', 'ла': 'лы', 'ай': 'ая', 'ёл': 'ла', 'ок': 'ка',
    'сь': 'ся', 'ль': 'ли', 'ец': 'ца', 'ан': 'ана', 'яя': 'ей', 'ня': 'ни',
    'вь': 'вя', 'нь': 'ня', 'ёс': 'са', 'дь': 'дя', 'рь': 'ри', 'жа': 'жа',
    'ий': 'ого', 'ый': 'ого', 'ви': 'ви', 'ёр': 'ра', 'ие': 'их', 'ек': 'ек',
    'шь': 'ши', 'ая': 'ой', 'ли': 'ли', 'ей': 'ья', 'ея': 'еи', 'дя': 'дя', 'еа': 'еа',
    'ру': 'ру', 'го': 'го', 'по': 'по', 'ёж': 'ежа', 'ое': 'ого', 'но': 'на', 'ры': 'р',
    'во': 'ва', 'со': 'са', 'ст': 'ста', 'ко': 'ка', 'хи': 'хов', 'ые': 'ых',
    'цы': 'цы', 'ой': 'ой', 'ки': 'ки', 'ти': 'ти', 'си': 'си', 'ус': 'си',
    'та': 'та', 'ед': 'ьда', 'чи': 'чи', 'ри': 'ри', 'па': 'па', 'му': 'му', 'ев': 'ьва',
    'зе': 'зе', 'бо': 'бо', 'ёк': 'ька', 'ия': 'ии', 'пи': 'пи', 'ще': 'ща', 'то': 'та',
    'адь': 'ади', 'едь': 'едя', 'ось': 'ося', 'ысь': 'ыси', 'лёк': 'лька',
    'орь': 'ря', 'бей': 'бья', 'тей': 'тея', 'очь': 'очь', 'ами': 'и',
    'ней': 'ней', 'овь': 'ови', 'чая': 'чей', 'усь': 'уся', 'ана': 'ана',
    'ошь': 'ши', 'рна': 'рен', 'ика': 'ика', 'чка': 'чка',
    'ной': 'ной', 'чья': 'чьей', 'вой': 'вого', 'ень': 'еня', 'ова': 'овой',
    'шой': 'шого', 'аус': 'ауса', 'дой': 'дого', 'жая': 'жей', 'ьдь': 'ьди',
    'оус': 'оуса', 'кой': 'кого', 'лец': 'льца', 'мей': 'мея', 'пой': 'пого',
    'ако': 'ако', 'лус': 'луса', 'щая': 'щей', 'шки': 'шков', 'ель': 'еля',
    'хек': 'хека', 'ижа': 'ижы', 'лль': 'ля', 'ота': 'оты', 'бый': 'бой',
    'лок': 'локов',
}

iskl = {
    'барсук-медоед': 'барсука-медоеда',
    'угорь-конгер': 'угря-конгера',
    'макака-резус': 'макаки-резус',
    'паук-отшельник': 'паука-отшельника',
    'пауканец-отшельник': 'пауканца-отшельника',
    'белка-летяга': 'белки-летяги',
    'паук-скакун': 'паука-скакуна',
    'человек-вомбат': 'человека-вомбата',
    'человек-виргинский': 'человека-виргинского',
    'человек-динго': 'человека-динго',
    'человек-ласка': 'человека-ласки',
    'гиена': 'гиены',
    'ласточка': 'ласточки',
    'грибной': 'грибного',
    'голова': 'головы',
    'луной': 'лунного',
    'ай-ай': 'ай-ай',
    'акула-молот': 'акулы-молота',
    'скат-хвостокол': 'ската-хвостокола',
    'акула-нянька': 'акулы-няньки',
    'медведь-губач': 'медведя-губача',
    'медведевик-губач': 'медведевика-губача',
    'луна-рыба': 'луна-рыбы',
    'рыба-меч': 'рыбы-меч',
    'белколюд-летяга': 'белколюда-летяги',
    'рыба-клоун': 'рыбы-клоуна',
    'боция-клоун': 'боции-клоуна',
    'рыба-нож': 'рыбы-нож',
    'корова': 'коровы',
    'сумерками': 'сумеречной',
    'камень': 'каменных',
    'шпинель': 'шпинели',
}

gent_case_except = {
    'луговник',  # определяет как глагол
    'шпинель',  # определяет как сущ. м.р.
    'стена',  # определяет как сущ. м.р.
    'лиса',  # определяет как сущ. м.р.
    'споры',  # в родительный падеж ставит как "споров"
}


def genitive_case_single_noun(word):
    print('genitive_case_single_noun')
    print(word)
    parse = list(filter(lambda x: x.tag.POS == 'NOUN', most_probable(morph.parse(word))))
    if word.lower() in gent_case_except or not parse:
        if word in iskl:
            return iskl[word]
        elif word[-3:] in endings_to_genitive:
            return word[:-3] + endings_to_genitive[word[-3:]]
        elif word[-2:] in endings_to_genitive:
            return word[:-2] + endings_to_genitive[word[-2:]]
        elif word[-1] in {"к", "т", "н"}:
            return word + "а"
    else:
        genitive = parse[0].inflect({'gent'})
        return genitive.word


def inflect_noun(word, case):
    parse = list(filter(lambda x: x.tag.POS == 'NOUN', most_probable(morph.parse(word))))
    assert parse is not None
    new_form = parse[0].inflect({case_names[case]})
    return new_form.word


def is_adjective(word):
    parse = morph.parse(word)
    is_adj = any_in_tag({'ADJF'}, parse) or any_in_tag({'PRTF'}, parse)
    if is_adj:
        print(word, 'is adj')
    else:
        print(word, "isn't adj")
    return is_adj


def genitive_case_list(words):
    print("genitive_case_list(%s)" % repr(words))
    print(words)
    gender = get_gender(words[-1])
    if gender is None:
        print("Assuming gender of '%s' is masculine" % words[-1])
        gender = masculine
    for word in words:
        if is_adjective(word):
            word = inflect_adjective(word, gender, genitive)
        else:
            word = genitive_case_single_noun(word)
        yield word


def genitive_case(word):
    return ' '.join(genitive_case_list(word.split()))


#############################################################################

animals_female = {"собака", "самка", "крольчиха", "гусыня", "утка", "кошка", "ослица", "кобыла", "корова", "овца",
                  "свинья",
                  "коза", "курица", "свинка", "буйволица", "важенка", "лама", "альпака", "цесарка", "пава", "индейка", }

body_parts = {"панцирь", "скелет", "искалеченный труп", "останки", "кость", "кожа", "шёлк", "волокна", "шерсть", "мех",
              " хвост"}

re_01 = re.compile(r"^[(+*-«☼]*((р?)(из\s[\w\s\-/]+\b))")

corr_item_01_except = {
    "боевой",  # Avoid recognition "боевой" as a female surname in genitive
    # "кирки",  # Avoid recognition "кирки" as a noun in genitive
    # "бочка",  # Avoid recognition "бочка" as "бочок" in genitive
}


def any_in_tag(gram, parse):
    return any(gram in p.tag for p in parse)


def corr_item_01(s):
    print('corr_item_01')
    hst = re_01.search(s)
    initial_string = hst.group(1)
    p_symbol = hst.group(2)
    words = hst.group(3).split()
    start_sym = ""
    end_sym = ""
    if p_symbol:
        start_sym = "≡"
        if words[-1][-1] == 'р':
            words[-1] = words[-1][:-1]
            end_sym = start_sym
    print(words)
    if len(words) == 2:
        parse = list(filter(lambda x: {'NOUN', 'gent'} in x.tag, morph.parse(words[1])))
        assert len(parse) == 1
        replacement_string = parse[0].normal_form
    elif words[1] == 'древесины':
        # Ultra simple case
        if 'дерева' in words:  # 'из древесины миндального дерева'
            cut_index = words.index('дерева') + 1
        elif 'пекан' in words:  # 'из древесины ореха пекан'
            cut_index = words.index('пекан') + 1
        elif any_in_tag({'NOUN', 'gent'}, morph.parse(words[2])):  # 'из древесины яблони'
            cut_index = 3
        else:
            cut_index = -1
        replacement_string = ' '.join(words[cut_index:] + words[:cut_index])
    elif (all(any_in_tag({'ADJF', 'gent'}, morph.parse(adj)) for adj in words[1:-1]) and
         any_in_tag({'NOUN', 'gent'}, morph.parse(words[-1]))):
        # All words after 'из' except the last word are adjectives in genitive
        # The last is a noun in genitive
        material = words[-1]
        gender = get_gender(material, cases={genitive})
        parse = list(filter(lambda x: {'NOUN', 'gent'} in x.tag, morph.parse(material)))
        material = parse[0].normal_form
        adjs = words[1:-1]
        adjs = [inflect_adjective(adj, gender, case=nominative) for adj in adjs]
        replacement_string = ' '.join(adjs) + ' ' + material
    elif (words[2] not in corr_item_01_except and len(words) > 3 and
          any_in_tag({'gent'}, morph.parse(words[1])) and  # The second word is in genitive
          any_in_tag({'NOUN', 'gent'}, morph.parse(words[2]))):  # The third word is a noun in genitive
        # Complex case, eg. "из висмутовой бронзы"
        print('Complex case')
        of_material = " ".join(words[:3])
        words = words[3:]
        if len(words) == 1:
            first_part = words[0]
        else:
            obj = words[-1]
            gender = get_gender(obj)
            adjs = (inflect_adjective(adj, gender) or adj for adj in words[:-1])
            first_part = "%s %s" % (" ".join(adjs), obj)
        replacement_string = first_part + " " + of_material
    elif any_in_tag({'NOUN', 'gent'}, morph.parse(words[1])) and words[1] != 'древесины':
        # Simple case, eg. "из бронзы"
        print('Simple case')
        of_material = " ".join(words[:2])
        words = words[2:]
        item = words[-1]
        if of_material in make_adjective:
            gender = get_gender(item)
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
        assert False

    if start_sym:
        replacement_string = start_sym + replacement_string + end_sym
    elif end_sym:
        replacement_string += end_sym

    s = s.replace(initial_string, replacement_string)
    return s


# выражения типа "рогатый филин яйцо"
def corr_item_3(s):
    print(3)
    hst = re_3.search(s)
    if re_3_1.search(s):
        print(3.1)
        hst = re_3_1.search(s)
        s = hst.group(1) + " " + genitive_case(hst.group(3) + " " + hst.group(2))
        return s.capitalize()
    if hst.group(3) in replaced_parts:
        print(3.2)
        new_word = replaced_parts[hst.group(3)]
    else:
        print(3.3)
        new_word = hst.group(3)
    if hst.group(2) in make_adjective:
        print(3.4)
        s = s.replace(hst.group(0), hst.group(1) + new_word + " " + make_adjective[hst.group(2)])
    else:
        print(3.5)
        s = s.replace(hst.group(0), hst.group(1) + new_word + " " + genitive_case(hst.group(2)))
    print(3.0)
    return s


# выражения типа "приготовленные(рубленная) гигантский крот лёгкие"
re_prepared = re.compile(r"\W((приготовленные|рубленная)\s(.+)\s(\w+))")


def corr_prepared(s):
    print('corr_prepared(%r)' % s)
    hst = re_prepared.search(s)
    s = s.replace(hst.group(1), hst.group(2) + " " + hst.group(4) + " " + genitive_case(hst.group(3)))
    return s


re_skin = re.compile(r'(\(?)(.+)\s(из кожи)')


# выражения типа "горный козёл из кожи"
def corr_item_skin(s):
    print('corr_item_skin')
    hst = re_skin.search(s)
    s = s.replace(hst.group(0), hst.group(1) + "кожа " + genitive_case(hst.group(2)))
    return s


# выражения типа "свинохвост из волокон (ткань+шёлк+шерсть)"
re_clothes = re.compile(
    r'^[Xx\(+*-«☼]*((.+)\s(из волокон|из шёлка|из шерсти|из кожи|из копыт|из кости|из рогов|из бивней|из панциря|из зубов)\s(\w+\s?\w+))')


def corr_clothes(s):
    print('corr_clothes')
    hst = re_clothes.search(s)
    print(hst.group(1))
    s = s.replace(hst.group(1), hst.group(4) + " " + hst.group(3) + " " + genitive_case(hst.group(2)))
    s = s.replace("левый", "левая")
    s = s.replace("правый", "правая")
    return s


# выражения типа "древесина дуба брёвна"
re_wooden_logs = re.compile(r'(древесина)\s(\w+)\s(брёвна)')


def corr_wooden_logs(s):
    print(7)
    hst = re_wooden_logs.search(s)
    of_wood = "из " + hst.group(2)
    if of_wood in make_adjective:
        adj = inflect_adjective(make_adjective[of_wood], plural)
        s = s.replace(hst.group(0), adj + " " + hst.group(3))  # берёзовые брёвна
    else:
        s = s.replace(hst.group(0), hst.group(1) + " " + hst.group(2))  # древесина акации
    return s


# выражения типа "(бриолетовый восковые опалы)"
re_gem_cutting = re.compile(r'((бриолетовый|большой|огранённый|огранённый|грубый)\s[\w\s-]+)')


def corr_gem_cutting(s):
    print('corr_gem_cutting')
    hst = re_gem_cutting.search(s)
    words = hst.group(1).split()
    if words[-1] in body_parts:
        print('Redirect to corr_item_body_parts')
        return corr_item_body_parts(s)

    print(words)
    gender = get_gender(words[-1])
    print("gender:", gender)

    new_list = []
    for word in words[:-1]:
        if word in make_adjective:
            adj = make_adjective[word]
            word = inflect_adjective(adj, gender)
        new_list.append(word)

    new_list.append(words[-1])

    return s.replace(hst.group(0), " ".join(new_list))


# выражения типа "гигантский из ясеня лезвия топоров"
re_weapon_trap_parts = re.compile(
    r'(шипованный|огромный|большой|заточенный|гигантский|большой, зазубренный)\s(из\s[\w\s]+\b)')


def corr_weapon_trap_parts(s):
    print('corr_weapon_trap_parts')
    hst = re_weapon_trap_parts.search(s)
    adj = hst.group(1)
    words = hst.group(2).split()
    if " ".join(words[:2]) in make_adjective:
        print(9.1)
        material = " ".join(words[:2])
        print("material:", material)
        obj = " ".join(words[2:])
        print("object:", obj)
        gender = gender_item[obj]
        print("object gender:", gender)
        if adj not in make_adjective and " " in adj:
            adj_words = adj.split()
            new_words = [inflect_adjective(make_adjective[word], gender) for word in adj_words]
            new_adj = " ".join(new_words)
        else:
            new_adj = inflect_adjective(make_adjective[adj], gender)
        print(adj, ":", new_adj)
        new_word_2 = inflect_adjective(make_adjective[material], gender)
        print(material, ":", new_word_2)
        s = s.replace(hst.group(0), "%s %s %s" % (new_adj, new_word_2, obj))
    else:
        print(9.2)
        material = " ".join(words[:3])
        print("material:", material)
        obj = " ".join(words[3:])
        print("object:", obj)
        gender = gender_item[obj]
        if adj not in make_adjective and " " in adj:
            adj_words = adj.split()
            new_words = [inflect_adjective(make_adjective[word], gender) for word in adj_words]
            new_adj = " ".join(new_words)
        else:
            new_adj = inflect_adjective(make_adjective[adj], gender)
        print(adj, ":", new_adj)
        s = s.replace(hst.group(0), "%s %s %s" % (new_adj, obj, material))
    return s


# "животные"
def corr_item_10(s):
    print(10)
    s = s.replace("сырой", "сырая")
    if any(s.find(item) != -1 for item in animals_female):
        s = s.replace("(Ручной)", "(Ручная)")
        s = s.replace("боевой", "боевая")
        s = s.replace("Ничей", "Ничья")
        s = s.replace("охотничий", "охотничья")

    return s


posessive_adjectives = {
    'жаба': 'жабий',
    'корова': 'коровий',
    'медведь': 'медвежий'
}

re_container = re.compile(r'((\b.+)\s(бочка|мешок|ящик)\s\((.*?)(\)|$))')

replace_containment = {
    "Семя": "семена",
    "Специи": "специй",
    "Самоцвет": "самоцветы",
    "Слиток/Блок": "слитков/блоков",
}


# выражения типа "(дварфийское пиво бочка (из ольхи))"
def corr_container(s):
    print("corr_container")
    if s[0] == 'р':
        if s[-1] == 'р':
            s = '≡' + s[1:-1] + '≡'
        elif s[1].isupper():
            s = '≡' + s[1:]
    hst = re_container.search(s)
    initial_string = hst.group(1)
    print('initial_string:', initial_string)
    containment = hst.group(2)
    if containment in replace_containment:
        containment = replace_containment[containment]
    if containment.endswith('кровь'):
        words = containment.split()
        assert len(words) == 2
        if words[0] in posessive_adjectives:
            words[0] = posessive_adjectives[words[0]]
        else:
            words.reverse()
        containment = " ".join(words)
    if containment.startswith('из '):
        containment = containment[3:]  # Already in genitive case
    else:
        containment = genitive_case(containment)
    container = hst.group(3)
    of_material = hst.group(4)
    if not of_material:
        print('Void material')
        replacement_string = container + ' ' + containment
    elif (' ' not in of_material and is_adjective(of_material) or
          of_material in make_adjective or of_material[3:] in make_adjective):
        print('Case 1')
        if ' ' not in of_material and is_adjective(of_material):
            adjective = of_material
        elif of_material in make_adjective:
            adjective = make_adjective[of_material]
        elif of_material[3:] in make_adjective:
            adjective = make_adjective[of_material[3:]]
        else:
            adjective = None
        gender = get_gender(container)
        adjective = inflect_adjective(adjective, gender)
        replacement_string = adjective + " " + container + " " + containment
    else:
        print('Case 2')
        words = of_material.split()
        if len(words) >= 2 and words[-2] == 'из' and words[-1] in {'волокон', 'шёлка', 'шёлк', 'шерсти', 'кожи'}:
            material_source = ' '.join(genitive_case_list(words[:-2]))
            parse = morph.parse(words[-1])
            if not any_in_tag({'gent'}, parse):
                parse = [p for p in parse if {'NOUN', 'nomn'} in p.tag][0]
                words[-1] = custom_inflect(parse, {'gent'}).word
            material = ' '.join(words[-2:])
            material = material + " " + material_source
        elif of_material.startswith('из '):
            material = of_material
        else:
            gen_case = list(genitive_case_list(of_material.split()))
            if None not in gen_case:
                material = 'из ' + ' '.join(gen_case)
            else:
                material = of_material
        replacement_string = "%s %s (%s" % (container, containment, material)
        if initial_string[-1] == ')':
            replacement_string += ')'
    s = s.replace(initial_string, replacement_string.capitalize())
    return s


# Элементы рельефа, крепости и т.п.
re_13 = re.compile(
    r'(.+)\s(Подъем|Стена|Кластер|валун|склон|Пол Пещеры|лестница вверх/вниз|пол пещеры|Лестница Вверх|Лестница Вниз|галька|деревце|лестница вверх|лестница вниз|подъем|пол)\b')


#    (прилагательное) (первое дополнение) (второе дополнение) =>
# => (прилагательное) (второе дополнение) из (первое дополнение)


def corr_item_12(s):
    print(12)
    hst = re_13.search(s)
    group1 = hst.group(1)
    obj = hst.group(2)
    if obj == "деревце":
        if group1.split(" ")[0] == "Мёртвый":
            s = "Мёртвое деревце (" + ''.join(hst.group(0).split(" ")[1:-1]) + ")"
        else:
            s = "Деревце (" + group1 + ")"
        return s.capitalize()

    if " " in group1:
        print(12.1)
        words = group1.split(" ")
        first_words = []
        gender = get_gender(obj)
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
            print("12.1.1")
            s = "%s из %s" % (obj, " ".join(words))
        else:
            print("12.1.2")
            s = "%s %s из %s" % (" ".join(first_words), obj, " ".join(words))
    else:
        print(12.2)
        material = group1
        s = "%s из %s" % (obj, genitive_case(material))

    if "иза" in s:
        s = s.replace(" иза", "")
    return s.capitalize()


# "Густой и тп"
def corr_item_13(s):
    print(13)
    hst = re_13_1.search(s)
    adjective = hst.group(1)
    obj = hst.group(2)

    if " " in obj:
        print(13.1)
        words = obj.split(" ")
        if is_adjective(words[0]):
            print("13.1.1")
            gender = get_gender(words[-1])
            new_word = inflect_adjective(words[0], gender, nominative)
            s = s.replace(words[0], new_word)
            new_word = inflect_adjective(adjective, gender, nominative)
            s = s.replace(adjective, new_word)
    else:
        print(13.2)
        gender = get_gender(obj)
        new_word = inflect_adjective(adjective, gender, nominative)
        if new_word:
            print("13.2.1")
            s = new_word + " " + obj

    return s.capitalize()


# "Скелет, останки и тп"
re_body_parts = re.compile(
    r'^[{]?((\w+\s?\w+?|)\s(панцирь|скелет|труп|останки|кость|кожа|шёлк|волокна|шерсть|мех|хвост|труп|голень))\}?\b')


def corr_item_body_parts(s):
    print('corr_item_body_parts')
    hst = re_body_parts.search(s)
    initial_string = hst.group(1)
    words = hst.group(2).split()
    if words[-1] in {"частичный", "искалеченный"}:
        replacement_string = "%s %s %s" % (words[-1], hst.group(3), " ".join(genitive_case_list(words[:-1])))
    else:
        if any('GRND' in morph.parse(word)[0].tag for word in words):  # Ignore participles
            return None
        replacement_string = hst.group(3) + " " + " ".join(genitive_case_list(words))
    return s.replace(initial_string, replacement_string.capitalize())


# "Изделия из стекла"
def corr_item_15(s):
    print(15)
    hst = re_14.search(s)
    s = hst.group(1) + " " + hst.group(3) + " " + make_adjective[hst.group(2)]
    return s.capitalize()


re_forge = re.compile(r"(^Ковать|^Делать|^Чеканить|^Изготовить|^Кузница)\s(из\s[\w\s?]+\b)")


# кузница
def corr_forge(s):
    print('corr_forge')
    hst = re_forge.search(s)
    verb = hst.group(1)
    words = hst.group(2).split()
    print('Verb:', verb)
    print('words:', words)
    assert len(words) >= 3
    if (any_in_tag({'ADJF', 'gent'}, morph.parse(words[1])) and  # The second word is an adj in gent
            any_in_tag({'NOUN', 'gent'}, morph.parse(words[2]))):  # The third word is a noun in gent
        print('Complex case')
        of_material = words[:3]
        obj = words[3:]
    else:
        assert any_in_tag({'NOUN', 'gent'}, morph.parse(words[1]))
        print('Simple case')
        of_material = words[:2]
        obj = words[2:]
        print('of_material:', of_material)
        print('obj:', obj)

    of_material = ' '.join(of_material)
    print(obj)
    item_index = None
    if len(obj) == 1:
        item_index = 0
        parse = morph.parse(obj[item_index])
        p = list(filter(lambda x: {'NOUN'} in x.tag and 'Surn' not in x.tag, parse))
        gender = get_gender(obj[item_index], cases={nominative})
        if not any_in_tag({'accs'}, p):
            obj[0] = p[0].inflect({'accs'}).word
    else:
        for i, x in enumerate(obj):
            parse = morph.parse(x)
            p = list(filter(lambda x: {'NOUN'} in x.tag and 'Surn' not in x.tag, parse))
            if p:
                item_index = i
                gender = get_gender(obj[item_index])
                obj[i] = p[0].inflect({'accs'}).word
                break  # Words after the 'item' must be leaved in genitive case
            elif not any_in_tag('accs', parse):
                obj[i] = parse[0].inflect({'accs'}).word

    print(obj)
    print(obj[item_index])

    if not any_in_tag('accs', parse):
        obj[item_index] = parse[0].inflect({'accs'}).word

    if verb == 'Кузница':
        verb = 'Ковать'

    if of_material in make_adjective:
        print('gender of "%s" is %s' % (obj[item_index], gender_names[gender]))
        material = inflect_adjective(make_adjective[of_material], gender, accusative, animated=False)
        s = verb + " " + material + " " + ' '.join(obj)
    else:
        s = verb + " " + ' '.join(obj) + " " + of_material

    return s.capitalize()


def instrumental_case(word):
    print("instrumental_case(%s)" % repr(word))
    assert ' ' not in word
    gender = get_gender(word)
    if gender is None:
        print("Assuming gender of '%s' is masculine" % word)
        gender = masculine

    if is_adjective(word):
        word = inflect_adjective(word, gender, instrumental)
    else:
        word = inflect_noun(word, instrumental)

    return word


re_jewelers_shop = re.compile(
    r"(^Инкрустировать Готовые товары с|^Инкрустировать Предметы обстановки с|^Инкрустировать Снаряды с|^Огранить)\s(.+)")


# Ювелирная мастерская
def corr_jewelers_shop(s):
    print('corr_jewelers_shop')
    hst = re_jewelers_shop.search(s)
    gem = ""
    first_part = hst.group(1)
    words = hst.group(2).split()
    if first_part == "Огранить":
        # accusative case
        cases = None
        if words[0] == 'из':
            words = words[1:]
            cases = {genitive}
        item = words[-1]
        gender = get_gender(item, cases=cases)
        print(':', gender_names[gender])
        words = [inflect_adjective(word, gender, accusative, animated=False) for word in words[:-1]]
        parse = list(filter(lambda x: {gender_names[gender], 'inan'} in x.tag, morph.parse(item)))
        if item == 'адамантина':
            item = 'адамантин'
        else:
            item = custom_inflect(parse[0], {'accs'}).word
        words.append(item)
    else:
        # instrumental/ablative case ('incrust with smth')
        words = [custom_inflect(morph.parse(word)[0], {'ablt'}).word for word in words if word != 'из']
    print(words)
    if first_part.endswith(' с'):
        first_part = first_part[:-2]
    s = first_part + ' ' + ' '.join(words)
    return s.capitalize()


gender_item["лесное убежище"] = neuter
gender_item["крепость"] = feminine
gender_item["селение"] = neuter
gender_item["горный город"] = masculine
gender_item["городок"] = masculine
gender_item["гробница"] = feminine
gender_item["пригорки"] = plural

re_settlement = re.compile(r'(.*)\s(лесное убежище|крепость|селение|горный город|городок|гробница|пригорки)\s(.+)')


# убежище, крепость
def corr_settlement(s):
    print("corr_settlement")
    hst = re_settlement.search(s)
    adjective = hst.group(1).strip()
    settlement = hst.group(2)
    name = hst.group(3)

    if len(adjective) == 0:
        return "%s %s" % (settlement.capitalize(), name.capitalize())

    if adjective in {'Покинуть', 'Разрушить'}:
        return

    gender = get_gender(settlement)
    if " " not in adjective:
        adjective_2 = inflect_adjective(adjective, gender)
    else:
        adjective_2 = " ".join(inflect_adjective(word, gender) for word in adjective.split(" "))

    if adjective_2 is None:
        adjective_2 = adjective

    return "%s %s %s" % (adjective_2.capitalize(), settlement, name.capitalize())


# выбор материала
def corr_item_20(s):
    print(20)
    hst = re_19.search(s)
    if hst.group(2) in phrases:
        new_word = phrases[hst.group(2)]
    else:
        new_word = hst.group(2)
    if hst.group(1) == 'пряжа' or hst.group(1) == 'растительное волокно':
        material = make_adjective[hst.group(1)]
        s = new_word + " " + material
        return s.capitalize()
    gender = gender_item[new_word]
    material = make_adjective[hst.group(1)][gender]
    s = material + " " + new_word
    return s.capitalize()


# кожа, шерсть-длинные названия
def corr_item_21(s):
    print(21)
    hst = re_20.search(s)
    s = hst.group(2) + " " + genitive_case(hst.group(1))
    return s


re_stopped_construction = re.compile(r'(\w+) приостановили строительство (.*)\.')


def corr_stopped_construction(s):
    print("corr_stopped_construction")
    hst = re_stopped_construction.search(s)
    subj = hst.group(1)
    obj = hst.group(2)
    gen_case_obj = genitive_case(obj)
    if gen_case_obj.endswith('мастерской'):
        gen_case_obj = ' '.join(reversed(gen_case_obj.split()))

    return ("%s приостановили строительство %s." % (subj, gen_case_obj)).capitalize()


# Корректировка для окончания s - перевод существительного во множественное число или глагола в 3-е лицо ед.ч.
re_ending_s = re.compile(r'([а-яёА-ЯЁ][а-яёА-ЯЁ\s]*e?s\b)')


def corr_ending_s(s):
    print("corr_ending_s")
    hst = re_ending_s.search(s)
    group1 = hst.group(1)
    if group1[:-1] in dict_ending_s:
        s = s.replace(group1, dict_ending_s[group1[:-1]])
    else:
        words = group1.split()
        if words[-1][:-1] in dict_ending_s:
            s = s.replace(words[-1], dict_ending_s[words[-1][:-1]])
        else:
            print("Couldn't find correct -s form for %s." % words[-1][:-1])
            return None
    return s


# Clothier's shop

re_clothiers_shop = re.compile(r'(Делать|Изготовить|Вышивать) (ткань|шёлк|пряжа|кожа) (\w+)')

cloth_subst = {
    "ткань": ("Шить", "из ткани"),
    "шёлк": ("Шить", "шёлковый"),
    "пряжа": ("Вязать", "из пряжи"),
    "кожа": ("Шить", "из кожи"),
}

accusative_case["носок"] = "носок"
accusative_case["штаны"] = "штаны"
accusative_case["верёвка"] = "верёвку"
accusative_case["капюшон"] = "капюшон"
accusative_case["башмак"] = "башмак"
accusative_case["мундир"] = "мундир"
accusative_case["плащ"] = "плащ"
accusative_case["мешок"] = "мешок"
accusative_case["жилет"] = "жилет"
accusative_case["рубаха"] = "рубаху"


def corr_clothiers_shop(s):
    print("Corr clothier's/leather shop")
    hst = re_clothiers_shop.search(s)
    verb = hst.group(1)
    material = hst.group(2)
    product = hst.group(3)

    if verb == 'Вышивать':
        parse = morph.parse(material)[0]
        if material == 'пряжа':
            verb = 'Вязать'
            material = custom_inflect(parse, {'gent'}).word
            return '%s %s из %s' % (verb, product, material)
        else:
            material = custom_inflect(parse, {'loct'}).word
            return '%s %s на %s' % (verb, product, material)
    else:
        if product in {'щит', 'баклер'}:
            of_material = cloth_subst[material][1]  # Leave 'Делать'/'Изготовить' verb
        else:
            verb, of_material = cloth_subst[material]

        if product == "верёвка":
            verb = "Вить"

        gender = get_gender(product, {nominative})
        if gender == feminine:
            product_accus = accusative_case[product]
        else:
            product_accus = product

        if material in make_adjective:
            material_adj = inflect_adjective(make_adjective[material], gender, accusative, animated=False)
            return ' '.join([verb, material_adj, product_accus])
        else:
            return ' '.join([verb, product_accus, of_material])


re_werebeast = re.compile(r"были(\w+)")


def corr_werebeast(s):
    hst = re_werebeast.search(s)
    return s.replace(hst.group(0), hst.group(1) + "-оборотень")


re_become = re.compile(r"(.+)\s(стал)\s(.+)\.")


def corr_become(s):
    print("corr_become")
    hst = re_become.search(s)
    subj = hst.group(1)
    verb = hst.group(2)
    print(verb)
    words = hst.group(3).split()
    words = (instrumental_case(word) for word in words)
    return "%s %s %s." % (subj, verb, ' '.join(words))


re_with_his = re.compile(r'(.*) с (его|её)(.*)')


def corr_with_his(s):
    print("corr_with_his")
    hst = re_with_his.search(s)
    # return "%s своим%s" % (hst.group(1), instrumental_case(hst.group(3)))
    return "%s своим%s" % (hst.group(1), hst.group(3))  # пока хотя бы так


re_crafts = re.compile(r"([\w\s]+) (кольцо|кольца)")


def corr_crafts(s):
    print("corr_crafts")
    hst = re_crafts.search(s)
    obj = hst.group(2)
    description = hst.group(1)
    return s.replace(hst.group(0), "%s из %s" % (obj, genitive_case(description)))


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


def corr_histories_of(s):
    hst = re_histories_of.search(s)
    return 'Истории о%s и %s' % (histories_adjs[hst.group(1)], histories_adjs[hst.group(2)])


def corr_well(s):
    s = s.replace('колодец', 'хорошо')
    if 'чувствую' in s and 'себя' not in s:
        s = s.replace('чувствую', 'чувствую себя')
    elif 'делаю хорошо' in s:
        s = s.replace('делаю хорошо', 'в порядке')
    elif 'был хорошо' in s:
        s = s.replace('был хорошо', 'в порядке')
    return s


def corr_minced(s):
    s1 = ''
    while 'рублены' in s and 'рубленый' not in s:
        x, _, s = s.partition('рублены')
        s1 += x + 'рубленый '

    return s1 + s


############################################################################
# компилированные регулярные выражения
re_3 = re.compile(
    r'(\(?)(.+)\s(\bяйцо|требуха|железы|железа|мясо|кровь|сукровица|кольца|серьги|амулеты|браслеты|скипетры|коронаы|статуэтки\b)')
re_3_1 = re.compile(r"(\bЛужа|Брызги|Пятно)\s(.+)\s(кровь\b)")
re_11 = re.compile(r'(Ничей|охотничий|сырой)(.+)((Ручной)|♀)')
re_13_1 = re.compile(r'\b(Густой|Редкий|Заснеженный)\s(.+)')
re_14 = re.compile(r'\b(Делать|Изготовить|Делать\s?\w+?)\s(зелёное стекло|прозрачное стекло|хрусталь)\s(\w+)')
re_19 = re.compile(r'(металл|кожа|пряжа|растительное волокно|дерево|шёлк)\s(.+)')
re_20 = re.compile(r'(.+)\s(кожа|кость|волокно|шёлк)\b')

verbs = {
    "промахивается", "контракует", "punches", "атакует", "нападает", "хватает", "повален", "выпускает",
    "сталкивается", "выглядит", "kicks", "встаёт", "bites", "держится", "трясёт", "позволяет", "блокирует",
    "душит", "пропускает", "истёк",
    "помещает",  # помещатет удушающий захват - заменить на что-то другое
}


############################################################################
def Init():
    # phrases['Test'] = 'Test'
    pass


Init()

log = True
if log:
    log_file = open('changetext.log', 'a', 1, encoding='utf-8')
    from datetime import datetime

    print('\n', datetime.today(), '\n', file=log_file)
else:
    log_file = None

logged = set()


def _ChangeText(s):
    def ChangeText_internal(s):
        result = None
        # preprocessing:
        if s in phrases:
            result = phrases[s]

        while re_ending_s.search(s):  # убрать из trans.txt 686284|s|ы|
            s1 = corr_ending_s(s)
            if s1 is None:
                break
            s = s1
            result = s

        if re_werebeast.search(s):
            s = corr_werebeast(s)
            result = s
        if re_with_his.search(s):
            s = corr_with_his(s)
            result = s

        if 'Я ' in s and 'колодец' in s:
            s = corr_well(s)
            result = s

        if 'рублены' in s and 'рубленый ' not in s:
            s = corr_minced(s)
            result = s

        for item in replaced_parts:
            if item in s:
                s = s.replace(item, replaced_parts[item])
                result = s

        if re_histories_of.search(s):
            result = corr_histories_of(s)
        elif re_container.search(s):
            result = corr_container(s)
        elif re_01.search(s):
            print('re_01 passed')
            result = corr_item_01(s)
        elif re_clothes.search(s):
            result = corr_clothes(s)
        elif re_prepared.search(s):
            result = corr_prepared(s)
        elif re_skin.search(s):
            result = corr_item_skin(s)
        elif re_forge.search(s):
            result = corr_forge(s)
        elif re_weapon_trap_parts.search(s):
            result = corr_weapon_trap_parts(s)
        elif re_3.search(s):
            result = corr_item_3(s)
        elif re_wooden_logs.search(s):
            result = corr_wooden_logs(s)
        elif re_gem_cutting.search(s):
            result = corr_gem_cutting(s)
        elif re_11.search(s):
            result = corr_item_10(s)
        elif re_stopped_construction.search(s):
            result = corr_stopped_construction(s)
        elif re_13.search(s):
            result = corr_item_12(s)
        elif re_13_1.search(s):
            result = corr_item_13(s)
        elif re_14.search(s):
            result = corr_item_15(s)
        elif re_jewelers_shop.search(s):
            result = corr_jewelers_shop(s)
        elif re_settlement.search(s):
            result = corr_settlement(s)
            # elif re_19.search(s): # Отключено: дает ложные срабатывания в логе
            # result = corr_item_20(s) 
        elif re_clothiers_shop.search(s):
            result = corr_clothiers_shop(s)
        elif re_body_parts.search(s):
            result = corr_item_body_parts(s)
        elif re_20.search(s):
            result = corr_item_21(s)
        elif re_become.search(s):
            result = corr_become(s)
        elif re_crafts.search(s):
            result = corr_crafts(s)

        return result

    try:
        output = ChangeText_internal(s)
    except Exception:
        print('An error occured.', file=sys.stderr)
        print('Initial string:', '"' + s + '"', file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        print("", file=sys.stderr)
        output = None

    if log and s not in logged:
        print('%r --> %r' % (s, output), file=log_file)
        log_file.flush()
        logged.add(s)

    return output


def ChangeText(s):
    if type(s) is bytes:
        output = _ChangeText(s.decode("utf-16"))
        if output is None:
            return None
        else:
            return output.encode("utf-16")[2:] + bytes(2)  # Truncate BOM marker and add b'\0\0' to the end
    else:
        return _ChangeText(s)


def main():
    if test_strings:
        for key in test_strings:
            result = ChangeText(key)
            try:
                assert result == test_strings[key]
            except AssertionError:
                print("A test failed.")
                print("Given '%s'" % key)
                print("Expected '%s'" % test_strings[key])
                print("Got '%s'" % result)
                raise
        print('All tests are passed.')
    input()

if __name__ == '__main__':
    main()
