# -*- coding: utf-8 -*-
import pytest

from ioex import AutoDict

def test_assign():
    d = AutoDict()
    assert d == {}
    d['A'] = 1
    assert d == {'A': 1}
    d['B'][2] = 'b'
    assert d == {'A': 1, 'B': {2: 'b'}}
    del d['A']
    assert d == {'B': {2: 'b'}}
    d['C'][3]['c'] = ('Γ', 'γ')
    assert d == {'B': {2: 'b'}, 'C': {3: {'c': ('Γ', 'γ')}}}
