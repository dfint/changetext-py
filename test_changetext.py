import pytest

from changetext import ChangeText


class TestTags:
    def test_not_tags(self):
        # проверка ложных срабатываний:
        assert ChangeText("<-") == None
        assert ChangeText("<1в") == None
        assert ChangeText(" <> ") == None

    def test_invalid_tags(self):
        assert ChangeText('asdfa <aeger:etrhrt> ehsge') == 'asdfa etrhrt ehsge'
        assert ChangeText('asdfa <aeger> ehsge') == 'asdfa ehsge'

    def test_tag_wrap(self):
        ChangeText('whatever <gent>')
        assert ChangeText('голова') == 'головы'

    def test_capitalize_tag(self):
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


def test_corr_has_verb():
    # Test 'has' + verb fix
    assert ChangeText(' имеет создал ') == ' создал '
    assert ChangeText(' имеет пришёл ') == ' пришёл '
    assert ChangeText(' имеет упал ') == ' упал '
    assert ChangeText(' имеет стрямкал ') == ' стрямкал '
