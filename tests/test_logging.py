import io
import contextlib

from changetext import get_logger, log_exceptions_and_result


def test_cache():
    file = io.StringIO()
    assert get_logger(file) is get_logger(file)


def test_double_write():
    text = "text"
    result = "result"
    file = io.StringIO()

    get_logger(file).write(text, result)
    assert file.getvalue() == "{!r} --> {!r}\n".format(text, result)

    # Try to write the same again
    get_logger(file).write(text, result)
    assert file.getvalue() == "{!r} --> {!r}\n".format(text, result)


def test_exception_logging():
    stderr = io.StringIO()
    with contextlib.redirect_stderr(stderr):
        @log_exceptions_and_result
        def foo(_):
            raise ValueError

        foo('text')

    stderr_text = stderr.getvalue().splitlines(keepends=False)
    assert stderr_text[0] == "An error occurred."
