import re

from changetext.common_state import get_state

contexts = {
    "  Dwarf Fortress  ": "main",
    "Овощи/фрукты/листья": "kitchen",
    re.compile(r"Граждане \(\d+\)"): "units",
    "Создано:": "status",
}

contextual_replace = dict(
    kitchen={"Повар": "Готовить"},
    units={"Рыба": "Рыбачить"},
)


def corr_contextual(text):
    state = get_state()
    if text in contexts:
        state.context = contexts[text]
    else:
        for pattern in contexts:
            if not isinstance(pattern, str) and pattern.search(text):
                state.context = contexts[pattern]
                break

    if state.context and state.context in contextual_replace:
        return contextual_replace[state.context].get(text, None)
