import pytest

from changetext import ChangeText


def test_not_tags():
    # проверка ложных срабатываний:
    assert ChangeText("<-") == None
    assert ChangeText("<1в") == None
    assert ChangeText(" <> ") == None


def test_invalid_tags():
    assert ChangeText('asdfa <aeger:etrhrt> ehsge') == 'asdfa etrhrt ehsge'
    assert ChangeText('asdfa <aeger> ehsge') == 'asdfa ehsge'


def test_tag_wrap():
    ChangeText('whatever <gent>')
    assert ChangeText('голова') == 'головы'


def test_capitalize_tag():
    assert ChangeText("<capitalize>капитан ополчения встаёт.") == "Капитан ополчения встаёт."


def test_corr_color_of_color():
    assert ChangeText("цвет серебристого цвета") == "серебристый цвет"
    assert ChangeText("цвет цвета морской волны") == "цвет морской волны"


def test_corr_contextual():
    ChangeText('  Dwarf Fortress  ')  # switch to the 'main' context
    assert ChangeText('Повар') in {'Повар', None}
    assert ChangeText('Рыба') in {'Рыба', None}
    
    ChangeText('Овощи/фрукты/листья')  # switch to the 'kitchen' context
    assert ChangeText('Повар') == 'Готовить'
    
    ChangeText('Граждане (10)')  # switch to the 'units' context
    assert ChangeText('Рыба') == 'Рыбачить'
