from changetext.contextual_changes import corr_contextual
from changetext.final_changes import final_changes
from changetext.logging_tools import get_logger, log_exceptions
from changetext.preliminary_changes import preliminary_changes
from changetext.utf16_codec import utf16_codec


def change_text(text):
    text = preliminary_changes.incremental_changes(text)
    assert text is not None
    text = corr_contextual(text)
    assert text is not None
    text = final_changes.exclusive_changes(text)
    assert text is not None
    return text


@utf16_codec
@log_exceptions()
def outer_change_text(text):
    result = change_text(text)
    get_logger().write(f"{outer_change_text.__name__}({text!r}) -> {result!r}")
    return result
