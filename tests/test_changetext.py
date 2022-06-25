import pytest

from changetext import change_text


@pytest.mark.parametrize(
    "text, expected",
    [
        ("цвет серебристого цвета", "серебристый цвет"),
        ("цвет цвета морской волны", "цвет морской волны"),
    ]
)
def test_corr_color_of_color(text, expected):
    assert change_text(text) == expected


def test_corr_contextual():
    change_text("  Dwarf Fortress  ")  # switch to the 'main' context
    assert change_text("Повар") in {"Повар", None}
    assert change_text("Рыба") in {"Рыба", None}

    change_text("Овощи/фрукты/листья")  # switch to the 'kitchen' context
    assert change_text("Повар") == "Готовить"

    change_text("Граждане (10)")  # switch to the 'units' context
    assert change_text("Рыба") == "Рыбачить"


@pytest.mark.parametrize(
    "text, expected",
    [
        (" имеет создал ", " создал "),
        (" был создать ", " создал "),
        (" имеет пришёл ", " пришёл "),
        (" имеет упал ", " упал "),
        (" имеет стрямкал ", " стрямкал "),
    ]
)
def test_corr_has_verb(text, expected):
    # Test 'has' + verb fix
    assert change_text(text) == expected
