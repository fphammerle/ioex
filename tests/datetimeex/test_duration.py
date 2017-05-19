# -*- coding: utf-8 -*-
import pytest

from ioex.datetimeex import Duration


@pytest.mark.parametrize(('init_kwargs'), [
    {'years': 0},
    {'years': 13},
    {'days': 0},
    {'days': 13},
    {'years': 1, 'days': 3},
])
def test_init(init_kwargs):
    d = Duration(**init_kwargs)
    for attr in ['years', 'days']:
        if attr in init_kwargs:
            assert init_kwargs[attr] == getattr(d, attr)
        else:
            assert 0 == getattr(d, attr)


def test_init_default():
    d = Duration()
    assert 0 == d.years
    assert 0 == d.days


@pytest.mark.parametrize(('init_kwargs', 'exception_type'), [
    [{'years': -2}, ValueError],
    [{'years': '1'}, TypeError],
    [{'days': -2}, ValueError],
    [{'days': '1'}, TypeError],
])
def test_init_fail(init_kwargs, exception_type):
    with pytest.raises(exception_type):
        Duration(**init_kwargs)


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


@pytest.mark.parametrize(('days'), [
    0,
    13,
])
def test_set_days(days):
    d = Duration()
    d.days = days
    assert d.days == days


@pytest.mark.parametrize(('days', 'exception_type'), [
    [-2, ValueError],
    ['1', TypeError],
])
def test_set_days_fail(days, exception_type):
    d = Duration()
    with pytest.raises(exception_type):
        d.days = days


@pytest.mark.parametrize(('init_params', 'iso'), [
    [{'years': 0}, 'P0Y'],
    [{'years': 30}, 'P30Y'],
    [{'years': 3}, 'P3Y'],
    [{'days': 30}, 'P30D'],
    [{'days': 3}, 'P3D'],
    [{'years': 10, 'days': 30}, 'P10Y30D'],
])
def test_get_isoformat(init_params, iso):
    d = Duration(**init_params)
    assert d.isoformat == iso


@pytest.mark.parametrize(('a', 'b'), [
    [Duration(), Duration(years=0, days=0)],
    [Duration(years=0), Duration(years=0)],
    [Duration(years=3), Duration(years=3)],
    [Duration(days=0), Duration(days=0)],
    [Duration(days=3), Duration(days=3)],
    [Duration(years=1, days=3), Duration(years=1, days=3)],
])
def test_eq(a, b):
    assert a == b
    assert b == a
