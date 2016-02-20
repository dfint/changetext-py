import pytest

from changetext import ChangeText


def test_tag_wrap():
    assert ChangeText('whatever <gent>') == 'whatever '
    assert ChangeText('голова') == 'головы'
