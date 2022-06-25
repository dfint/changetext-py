import pytest

import changetext
from changetext import change_text


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
        ("<-", None),
        ("<1в", None),
        (" <> ", None),
        ("asdfa <aeger:etrhrt> ehsge", "asdfa etrhrt ehsge"),
        ("asdfa <aeger> ehsge", "asdfa ehsge"),
        ("<capitalize>капитан ополчения встаёт.", "Капитан ополчения встаёт."),
        (
            "летящий {+железный болт+} бьёт <accs> индюк в <accs> голова, разрывая <accs>",
            "летящий {+железный болт+} бьёт индюка в голову, разрывая",
        ),
        (
            "летящий {+железный болт+} бьёт <accs> индюк в <accs> голова, разрывая <accs>",
            "летящий {+железный болт+} бьёт индюка в голову, разрывая",
        ),
        (
            "Lyrical Wisp. По  возможности она предпочитает употреблять<accs>  ячий сыр и",
            "Lyrical Wisp. По  возможности она предпочитает употреблять ячий сыр и",
        ),
        (
            "Она   гражданин   <gent>   <capitalize>    Ochre   Girders.   Она   член   <gent>",
            "Она   гражданин Ochre   Girders.   Она   член",
        ),
        (
            "Она  гражданин  <gent>  <capitalize>  Livid Dyes.  Она  член <gent>  <capitalize>",
            "Она  гражданин Livid Dyes.  Она  член",
        ),
    ],
)
def test_tags_general(init_change_text, text, expected):
    assert change_text(text) == expected
