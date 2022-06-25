import pytest

from changetext.utils import open_brackets


@pytest.mark.parametrize(
    "text, expected",
    [
        ("()", "()"),
        ("!(*+-[{«р☼XxTEST", "!(*+-[{«≡☼XxTEST"),
        ("!(*+-[{«р☼XxTESTxX☼р»}]-+*)!", "!(*+-[{«≡☼XxTESTxX☼≡»}]-+*)!"),
        ("(", "("),
        ("рTр", "≡T≡"),
        ("!(*+-[{«р☼XxT", "!(*+-[{«≡☼XxT"),
        ("ррамбутановая брага бочка (и", "≡рамбутановая брага бочка (и"),
        ("*рамбутановая брага бочка (и", "*рамбутановая брага бочка (и"),
        ("-рамбутановая брага бочка (и", "-рамбутановая брага бочка (и"),
    ]
)
def test_open_brackets(text, expected):
    assert open_brackets(lambda x: x)(text) == expected
