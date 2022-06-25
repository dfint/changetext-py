import changetext
from changetext import change_text


def test_not_tags():
    # проверка ложных срабатываний:
    assert change_text("<-") is None
    assert change_text("<1в") is None
    assert change_text(" <> ") is None


def test_invalid_tags():
    assert change_text("asdfa <aeger:etrhrt> ehsge") == "asdfa etrhrt ehsge"


def test_skip_unknown_tags():
    assert change_text("asdfa <aeger> ehsge") == "asdfa ehsge"


def test_tag_wrap():
    change_text("whatever <gent>")
    assert change_text("голова") == "головы"


def test_capitalize_tag():
    assert change_text("<capitalize>капитан ополчения встаёт.") == "Капитан ополчения встаёт."


def test_consecutive_tags():
    assert (
        change_text("Она   гражданин   <gent>   <capitalize>    Ochre   Girders.   Она   член   <gent>")
        == "Она   гражданин Ochre   Girders.   Она   член"
    )
    changetext.init()
    assert (
        change_text("Она  гражданин  <gent>  <capitalize>  Livid Dyes.  Она  член <gent>  <capitalize>")
        == "Она  гражданин Livid Dyes.  Она  член"
    )


def test_tag_spaces():
    changetext.init()
    assert (
        change_text("Lyrical Wisp. По  возможности она предпочитает употреблять<accs>  ячий сыр и")
        == "Lyrical Wisp. По  возможности она предпочитает употреблять ячий сыр и"
    )
    assert (
        change_text("вино из плодов восковницы. Она совершенно не выносит<accs> комары.")
        == "вино из плодов восковницы. Она совершенно не выносит комаров."
    )
    assert change_text('Anurnir, " <capitalize> Wondrous Land"') == 'Anurnir, "Wondrous Land"'


def test_commas():
    assert (
        change_text("летящий {+железный болт+} бьёт <accs> индюк в <accs> голова, разрывая <accs>")
        == "летящий {+железный болт+} бьёт индюка в голову, разрывая"
    )
