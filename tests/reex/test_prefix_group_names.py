# -*- coding: utf-8 -*-
import pytest

import ioex.reex


@pytest.mark.parametrize(('source', 'prefix', 'expected'), [
    ['(?P<a>a)', 'pre_', '(?P<pre_a>a)'],
    ['(?P<a>a(?P<a1>1))', 'pre_', '(?P<pre_a>a(?P<pre_a1>1))'],
    ['(?P<a>a)(?P<b>b)', 'pre_', '(?P<pre_a>a)(?P<pre_b>b)'],
])
def test_prefix_group_names(source, prefix, expected):
    assert expected == ioex.reex.prefix_group_names(source, prefix)
