# -*- coding: utf-8 -*-
import pytest

import ioex.reex


@pytest.mark.parametrize(('source', 'repl', 'expected'), [
    ['(?P<a>a)', lambda n: n.upper(), '(?P<A>a)'],
    ['(?P<a>a(?P<a1>1))', lambda n: n.upper(), '(?P<A>a(?P<A1>1))'],
    ['(?P<a>a)(?P<b>b)', lambda n: n.upper(), '(?P<A>a)(?P<B>b)'],
])
def test_rename_groups(source, repl, expected):
    assert expected == ioex.reex.rename_groups(source, repl)
