import io

from changetext.logging_tools import get_logger, log_exceptions


def test_cache():
    file = io.StringIO()
    assert get_logger(file) is get_logger(file)


def test_double_write():
    text = "text"
    result = "result"
    file = io.StringIO()

    text = f"{text!r} --> {result!r}"
    get_logger(file).write(text)
    assert file.getvalue().strip() == text

    # Try to write the same again
    get_logger(file).write(text)
    assert file.getvalue().strip() == text


def test_exception_logging():
    file = io.StringIO()

    @log_exceptions(file)
    def foo(_):
        raise ValueError

    arg = "text"
    foo("text")

    stderr_text = file.getvalue().splitlines(keepends=False)
    assert stderr_text[0] == f"An exception occurred. Initial string: {arg!r}"
