import pytest

from changetext import ChangeText


def test_tag_wrap():
    ChangeText('whatever <gent>')
    assert ChangeText('голова') == 'головы'
