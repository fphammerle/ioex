# -*- coding: utf-8 -*-
import pytest

from ioex.datetimeex import Duration

@pytest.mark.parametrize(('years'), [
    0,
    13,
    ])
def test_init(years):
    d = Duration(years = years)
    assert d.years == years

def test_init_default():
    d = Duration()
    assert d.years == 0
    None,

@pytest.mark.parametrize(('years', 'exception_type'), [
    [-2, ValueError],
    ['1', TypeError],
    ])
def test_init_fail(years, exception_type):
    with pytest.raises(exception_type):
        Duration(years = years)

@pytest.mark.parametrize(('years'), [
    0,
    13,
    ])
def test_set_years(years):
    d = Duration()
    d.years = years
    assert d.years == years

@pytest.mark.parametrize(('years', 'exception_type'), [
    [-2, ValueError],
    ['1', TypeError],
    ])
def test_set_years_fail(years, exception_type):
    d = Duration()
    with pytest.raises(exception_type):
        d.years = years

@pytest.mark.parametrize(('init_params', 'iso'), [
    [{'years': 0}, 'P0Y'],
    [{'years': 3}, 'P3Y'],
    ])
def test_get_isoformat(init_params, iso):
    d = Duration(**init_params)
    assert d.isoformat == iso

@pytest.mark.parametrize(('a', 'b'), [
    [Duration(), Duration(years = 0)],
    [Duration(years = 0), Duration(years = 0)],
    [Duration(years = 3), Duration(years = 3)],
    ])
def test_eq(a, b):
    assert a == b
    assert b == a
