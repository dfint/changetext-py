import io

from changetext import get_logger


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
