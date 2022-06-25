import pytest

from changetext import change_text


@pytest.mark.parametrize(
    "text, expected",
    [
        ("цвет серебристого цвета", "серебристый цвет"),
        ("цвет цвета морской волны", "цвет морской волны"),
    ],
)
def test_corr_color_of_color(text, expected):
    assert change_text(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        (" имеет создал ", " создал "),
        (" был создать ", " создал "),
        (" имеет пришёл ", " пришёл "),
        (" имеет упал ", " упал "),
        (" имеет стрямкал ", " стрямкал "),
    ],
)
def test_corr_has_verb(text, expected):
    # Test 'has' + verb fix
    assert change_text(text) == expected
