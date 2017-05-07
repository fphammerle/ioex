# -*- coding: utf-8 -*-
import pytest

from ioex import dict_collapse


@pytest.mark.parametrize(('src', 'key_repl', 'expected'), [
    [{'a': 'a'}, lambda k: k.upper(), {'A': 'a'}],
    [{'a1': 'a', 'a2': None}, lambda k: k[0], {'a': 'a'}],
    [{'a1': None, 'a2': 'a'}, lambda k: k[0], {'a': 'a'}],
    [{'a1': None, 'a2': False}, lambda k: k[0], {'a': False}],
    [{'a1': None, 'a2': (None,)}, lambda k: k[0], {'a': (None,)}],
    [{'1': 'a', 1.0: 'b'}, lambda k: k, {'1': 'a', 1.0: 'b'}],
    [{'1': None, 1.0: 'b'}, lambda k: int(k), {1: 'b'}],
])
def test_collapse(src, key_repl, expected):
    assert expected == dict_collapse(src, key_repl)


@pytest.mark.parametrize(('src', 'key_repl'), [
    [{'a1': 1, 'a2': 2}, lambda k: k[0]],
    [{'a1': None, 'a2': 2, 'a3': 3}, lambda k: k[0]],
    [{'a1': True, 'a2': False}, lambda k: k[0]],
    [{'a1': True, 'a2': (None,)}, lambda k: k[0]],
    [{'a1': True, 'a2': []}, lambda k: k[0]],
    [{'1': 'a', 1.0: 'b'}, lambda k: int(k)],
])
def test_collapse_fail(src, key_repl):
    with pytest.raises(ValueError):
        dict_collapse(src, key_repl)
