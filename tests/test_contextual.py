from changetext.changetext import change_text
from changetext.contextual import corr_contextual


def test_corr_contextual():
    change_text("  Dwarf Fortress  ")  # switch to the 'main' context
    assert corr_contextual("Повар") in {"Повар", None}
    assert change_text("Повар") in {"Повар", None}

    assert corr_contextual("Рыба") in {"Рыба", None}
    assert change_text("Рыба") in {"Рыба", None}

    change_text("Овощи/фрукты/листья")  # switch to the 'kitchen' context
    assert corr_contextual("Повар") == "Готовить"
    assert change_text("Повар") == "Готовить"

    change_text("Граждане (10)")  # switch to the 'units' context
    assert corr_contextual("Рыба") == "Рыбачить"
    assert change_text("Рыба") == "Рыбачить"
