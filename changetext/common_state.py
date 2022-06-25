class ChangeTextState:
    def __init__(self):
        self.prev_tail = ""
        self.context = None


_change_text_state = None


def init():
    global _change_text_state
    _change_text_state = ChangeTextState()


init()


def get_state() -> ChangeTextState:
    global _change_text_state
    if _change_text_state is None:
        _change_text_state = ChangeTextState()
    return _change_text_state
