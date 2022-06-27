from changetext.corrector import get_corrector
from changetext.logging_tools import get_logger, log_exceptions
from changetext.utf16_codec import utf16_codec


def change_text(text):
    return get_corrector().change_text(text)


@utf16_codec
@log_exceptions
def outer_change_text(text):
    result = change_text(text)
    get_logger().write(text, result)
    return result
