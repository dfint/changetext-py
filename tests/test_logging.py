import contextlib
import io

from changetext.logging_tools import get_logger, log_exceptions


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
    stdout = io.StringIO()

    with contextlib.redirect_stdout(stdout):
        @log_exceptions
        def foo(_):
            raise ValueError

        foo('text')

    stderr_text = stdout.getvalue().splitlines(keepends=False)
    assert stderr_text[0] == "An exception occurred. Initial string: 'text'"
