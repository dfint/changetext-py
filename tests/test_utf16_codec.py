from changetext import utf16_codec


def test_none():
    text = "text"
    assert utf16_codec(lambda s: None)(text) is None


def test_str():
    text = "text"
    assert utf16_codec(lambda s: s)(text) == text


def test_utf16():
    text = "text"
    encoded = text.encode("utf-16-le")
    assert utf16_codec(lambda s: s)(encoded) == encoded + b"\0\0"
