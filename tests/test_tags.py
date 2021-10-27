import changetext
from changetext import ChangeText


def test_not_tags():
    # проверка ложных срабатываний:
    assert ChangeText("<-") is None
    assert ChangeText("<1в") is None
    assert ChangeText(" <> ") is None


def test_invalid_tags():
    assert ChangeText('asdfa <aeger:etrhrt> ehsge') == 'asdfa etrhrt ehsge'
    assert ChangeText('asdfa <aeger> ehsge') == 'asdfa ehsge'


def test_tag_wrap():
    ChangeText('whatever <gent>')
    assert ChangeText('голова') == 'головы'


def test_capitalize_tag():
    assert ChangeText("<capitalize>капитан ополчения встаёт.") == "Капитан ополчения встаёт."


def test_consecutive_tags():
    assert (ChangeText('Она   гражданин   <gent>   <capitalize>    Ochre   Girders.   Она   член   <gent>')
            == 'Она   гражданин Ochre   Girders.   Она   член')
    changetext.init()
    assert (ChangeText('Она  гражданин  <gent>  <capitalize>  Livid Dyes.  Она  член <gent>  <capitalize>')
            == 'Она  гражданин Livid Dyes.  Она  член')


def test_tag_spaces():
    changetext.init()
    assert (ChangeText('Lyrical Wisp. По  возможности она предпочитает употреблять<accs>  ячий сыр и')
            == 'Lyrical Wisp. По  возможности она предпочитает употреблять ячий сыр и')
    assert (ChangeText('вино из плодов восковницы. Она совершенно не выносит<accs> комары.')
            == 'вино из плодов восковницы. Она совершенно не выносит комаров.')
    assert ChangeText('Anurnir, " <capitalize> Wondrous Land"') == 'Anurnir, "Wondrous Land"'


def test_commas():
    assert (ChangeText('летящий {+железный болт+} бьёт <accs> индюк в <accs> голова, разрывая <accs>')
            == 'летящий {+железный болт+} бьёт индюка в голову, разрывая')
