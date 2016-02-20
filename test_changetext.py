import pytest

from changetext import ChangeText


def test_not_tags():
    # проверка ложных срабатываний:
    assert ChangeText("<-") == None
    assert ChangeText("<1в") == None
    assert ChangeText(" <> ") == None


def test_tag_wrap():
    ChangeText('whatever <gent>')
    assert ChangeText('голова') == 'головы'
