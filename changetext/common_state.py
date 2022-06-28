import functools


class ChangeTextState:
    def __init__(self, object_id):
        self.object_id = object_id
        self.prev_tail = ""
        self.context = None

    def reset(self):
        self.prev_tail = ""
        self.context = None


def init():
    pass


@functools.lru_cache()
def get_state(object_id=None):
    return ChangeTextState(object_id)
