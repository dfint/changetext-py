import pytest

import changetext
from changetext import change_text
from changetext.tag_correction import corr_tags


@pytest.fixture
def init_change_text():
    changetext.init()


def test_tag_wrap():
    change_text("whatever <gent>")
    assert change_text("голова") == "головы"


def test_tag_spaces(init_change_text):
    assert (
        change_text("Lyrical Wisp. По  возможности она предпочитает употреблять<accs>  ячий сыр и")
        == "Lyrical Wisp. По  возможности она предпочитает употреблять ячий сыр и"
    )
    assert (
        change_text("вино из плодов восковницы. Она совершенно не выносит<accs> комары.")
        == "вино из плодов восковницы. Она совершенно не выносит комаров."
    )
    assert change_text('Anurnir, " <capitalize> Wondrous Land"') == 'Anurnir, "Wondrous Land"'


@pytest.mark.parametrize(
    "text, expected",
    [
        ("<capitalize>капитан ополчения встаёт.", "Капитан ополчения встаёт."),
        (
            "Lyrical Wisp. По  возможности она предпочитает употреблять<accs>  ячий сыр и",
            "Lyrical Wisp. По  возможности она предпочитает употреблять ячий сыр и",
        ),
        (
            "Она  гражданин  <gent>  <capitalize>  Livid Dyes.  Она  член <gent>  <capitalize>",
            "Она  гражданин Livid Dyes.  Она  член",
        ),
        (
            "В <loct> начале осени <gent> 8, <get-form:Я> <set-form:пел>:  'О Music!' был",
            "В начале осени 8 года Я пел:  'О Music!' был",
        ),
        (
            "весны <gent> 1 в <loct> Oakgrasping как часть <gent> Stern Celebration.",
            "весны 1 года в Oakgrasping как часть Stern Celebration.",
        ),
        (
            "В  <loct> начале  осени <gent> 10,  Factional Confederacy  провели соревнование с",
            "В начале осени 10 года  Factional Confederacy  провели соревнование с",
        ),
        (
            "<gent> Driving. Здесь были 5 конкуренты включая Ezif. Ezif одержал победу.",
            "of Driving. Здесь были 5 конкуренты включая Ezif. Ezif одержал победу.",
        ),
        ("Разоблачение <gent:Башня>", "Разоблачение Башни"),
        ("Дайте мне <accs,inan:Башня>", "Дайте мне Башню"),
        ("Здравые рассуждения о <loct:Башня>", "Здравые рассуждения о Башне"),
        ("<get-form:Она> <set-form:пел>: 'О  дварфы!'", "Она пела: 'О  дварфы!'"),
        ("<set-form:Мог> ли это быть <get-form:Могила>?", "Могла ли это быть Могила?"),
        ("Горный Город во времена <gent: Эра Мифов>", "Горный Город во времена Эры Мифов"),
        ("был похищен из Passplagues <ablt> птица рух Mot.", "был похищен из Passplagues птицей рух Mot."),
        (
            "Вы бьёте <accs> гоблин клерк в <accs> верхняя часть тела",
            "Вы бьёте гоблина клерк в верхнюю часть тела",
        ),  # FIXME: "клерка"
        ("украшать <ablt> кость", "украшать костью"),
        # ('Украшать <ablt> слоновая кость/зуб': 'Украшать слоновой костью/зубом'),
        ("Impaling в <loct> 1.", "Impaling в 1 году."),
        (
            "Mirrorseal <ablt> Blunt Smith <gent> Mute Work в <loct> начале весны <gent> 5.",
            "Mirrorseal Blunt Smith of Mute Work в начале весны 5 года.",
        ),
        (
            'Ruÿava Mawada Dipane, "Ruÿava  Bean   <gent> Skunks", сила',
            'Ruÿava Mawada Dipane, "Ruÿava  Bean of Skunks", сила',
        ),
        (
            "В начале осени  <gent> 14, Factional Confederacy держать  соревнование с участием",
            "В начале осени 14 года Factional Confederacy держать  соревнование с участием",
        ),
        ("В <loct> 1, Ezif поселился в Tiresky.", "В 1 году Ezif поселился в Tiresky."),
        ("В <loct> 1, Lusnub поселился в Hill <gent> Perishing.", "В 1 году Lusnub поселился в Hill of Perishing."),
        (
            "Couple  <gent> Glimmers  в Oakgrasping как часть <gent>  Festival <gent> Driving.",
            "Couple of Glimmers  в Oakgrasping как часть Festival of Driving.",
        ),
        ("В 2, Ezif стал <ablt> поэт в <loct> Tiresky.", "В 2, Ezif стал поэтом в Tiresky."),
        # TODO:
        # (
        #     "смертельного плевка! Oakpacks  был связан с <ablt>  вода, растения, природа,",
        #     "смертельного плевка! Oakpacks  был связан с  водой, растениями, природой,",
        # ),
        # (
        #     "<ablt> деревья, реки, растения, природа и животные.",
        #     "деревьями, реками, растениями, природой и животными.",
        # ),
        # ("статуэтка из ясеня <gent> пауки-скакуны", "статуэтка пауков-скакунов из ясеня"),
        # ("был связан с <ablt> разврат и похоть.", "был связан с развратом и похотью."),
        # (
        #     "Plaited Hall. èshgor  чаще всего изображается в виде <gent>  женский дварф и",
        #     "Plaited Hall. èshgor  чаще всего изображается в виде женщины-дварфа и",
        # ),
        # (
        #     "В  <loct> конце  зимы <gent> 12,  Rotik приручил  <accs> гигантские  протеи",
        #     "В конце зимы 12 года  Rotik приручил гигантских протеев",
        # ),
        # (
        #     "всего изображается в  виде <gent> мужской дварф и был связан  с <ablt> днём,",
        #     "всего изображается в  виде мужчины-дварфа и был связан  с днём,",
        # ),
        # (
        #     "Текстовая часть состоит из <gent> 64 страница справочник озаглавлен",
        #     "Текстовая часть состоит из 64 страниц справочник озаглавлен",
        # ),
        # (
        #     "возможности он предпочитает употреблять<accs> турнепс, ячменное вино и мука из фонио. Он совершенно не",
        #     "возможности он предпочитает употреблять турнепс, ячменное вино и муку из фонио. Он совершенно не",
        # ),
    ],
)
def test_tags_general(init_change_text, text, expected):
    assert corr_tags(text) == expected
    assert change_text(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("<-", None),
        ("<1в", None),
        (" <> ", None),
        ("asdfa <aeger:etrhrt> ehsge", "asdfa etrhrt ehsge"),
        ("asdfa <aeger> ehsge", "asdfa ehsge"),
        ('Golololв <accs>, "Golololв <accs>", ', 'Golololin, "Golololin", '),
        (
            "летящий {+железный болт+} бьёт <accs> индюк в <accs> голова, разрывая <accs>",
            "летящий {+железный болт+} бьёт индюка в голову, разрывая",
        ),
        (
            "Она   гражданин   <gent>   <capitalize>    Ochre   Girders.   Она   член   <gent>",
            "Она   гражданин Ochre   Girders.   Она   член",
        ),
        (
            '"Я был размышляет о <loct> концепция <gent> драгоценности."',
            '"Я размышлял о концепции драгоценностей."',
        ),
    ],
)
def test_tags_with_exceptions(init_change_text, text, expected):
    assert change_text(text) == expected
