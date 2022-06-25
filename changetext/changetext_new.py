from collections import OrderedDict

from changetext.corrector import Corrector
from changetext.utils import to_genitive_case, make_adjective

corrector = Corrector()

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


# выражения типа "приготовленные(рубленная) гигантский крот лёгкие"
@corrector.final_change(r"\W((приготовленные|рубленная)\s(.+)\s(\w+))")
def corr_prepared(text, search_result):
    """
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

    # print('corr_prepared(%r)' % s)
    groups = search_result.groups()
    result = text.replace(groups[0], "{} {} {}".format(groups[1], groups[3], to_genitive_case(groups[2])))
    return result


@corrector.final_change(r"(\bЛужа|Брызги|Пятно)\s(.+)\s(кровь\b)")
def corr_puddle(_text, search_result):
    text = search_result.group(1) + " " + to_genitive_case(search_result.group(3) + " " + search_result.group(2))
    return text.capitalize()


@corrector.final_change(r'(\(?)(.+)\s(\bяйцо|требуха|железы|железа|мясо|кровь|сукровица|кольца|серьги|амулеты|браслеты'
                        r'|скипетры|коронаы|статуэтки\b)')
def corr_item_3(text, search_result):
    """
    >>> corr_item_3('рогатый филин яйцо')
    'яйцо рогатого филина'
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


@corrector.final_change(r"\W((приготовленные|рубленная)\s(.+)\s(\w+))")
def corr_prepared(text, search_result):
    """
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
    groups = search_result.groups()
    result = text.replace(groups[0], "{} {} {}".format(groups[1], groups[3], to_genitive_case(groups[2])))
    return result


def change_text(text):
    return corrector.change_text(text)
