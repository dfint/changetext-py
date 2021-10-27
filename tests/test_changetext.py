from changetext import ChangeText


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
