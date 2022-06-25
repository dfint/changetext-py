from changetext import change_text


def test_corr_color_of_color():
    assert change_text("цвет серебристого цвета") == "серебристый цвет"
    assert change_text("цвет цвета морской волны") == "цвет морской волны"


def test_corr_contextual():
    change_text("  Dwarf Fortress  ")  # switch to the 'main' context
    assert change_text("Повар") in {"Повар", None}
    assert change_text("Рыба") in {"Рыба", None}

    change_text("Овощи/фрукты/листья")  # switch to the 'kitchen' context
    assert change_text("Повар") == "Готовить"

    change_text("Граждане (10)")  # switch to the 'units' context
    assert change_text("Рыба") == "Рыбачить"


def test_corr_has_verb():
    # Test 'has' + verb fix
    assert change_text(" имеет создал ") == " создал "
    assert change_text(" был создать ") == " создал "
    assert change_text(" имеет пришёл ") == " пришёл "
    assert change_text(" имеет упал ") == " упал "
    assert change_text(" имеет стрямкал ") == " стрямкал "
