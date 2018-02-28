# -*- coding: utf-8 -*-
import pytest

from ioex.datetimeex import Duration
import datetime
import pytz


@pytest.mark.parametrize(('init_kwargs'), [
    {'years': 0},
    {'years': 13},
    {'days': 0},
    {'days': 13},
    {'minutes': 7},
    {'years': 1, 'days': 3},
    {'years': 1, 'days': 3, 'minutes': 5},
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
    assert 0 == d.minutes


@pytest.mark.parametrize(('init_kwargs', 'exception_type'), [
    [{'years': -2}, ValueError],
    [{'years': '1'}, TypeError],
    [{'days': -2}, ValueError],
    [{'days': '1'}, TypeError],
    [{'minutes': -2}, ValueError],
    [{'minutes': '1'}, TypeError],
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


@pytest.mark.parametrize(('minutes'), [
    0,
    13,
])
def test_set_minutes(minutes):
    d = Duration()
    d.minutes = minutes
    assert d.minutes == minutes


@pytest.mark.parametrize(('minutes', 'exception_type'), [
    [-2, ValueError],
    ['1', TypeError],
])
def test_set_minutes_fail(minutes, exception_type):
    d = Duration()
    with pytest.raises(exception_type):
        d.minutes = minutes


@pytest.mark.parametrize(('init_params', 'iso'), [
    [{'years': 0}, 'P0Y'],
    [{'years': 30}, 'P30Y'],
    [{'years': 3}, 'P3Y'],
    [{'days': 30}, 'P30D'],
    [{'days': 3}, 'P3D'],
    [{'minutes': 3}, 'PT3M'],
    [{'years': 10, 'days': 30}, 'P10Y30D'],
    [{'days': 30, 'minutes': 50}, 'P30DT50M'],
    [{'years': 10, 'days': 30, 'minutes': 50}, 'P10Y30DT50M'],
])
def test_get_isoformat(init_params, iso):
    d = Duration(**init_params)
    assert d.isoformat == iso


@pytest.mark.parametrize(('expected', 'source_iso'), [
    [Duration(years=0), 'P0Y'],
    [Duration(years=30), 'P30Y'],
    [Duration(years=3), 'P3Y'],
    [Duration(days=30), 'P30D'],
    [Duration(days=3), 'P3D'],
    [Duration(minutes=3), 'PT3M'],
    [Duration(years=10, days=30), 'P10Y30D'],
    [Duration(days=30, minutes=50), 'P30DT50M'],
    [Duration(years=10, days=30, minutes=50), 'P10Y30DT50M'],
])
def test_from_iso(expected, source_iso):
    d = Duration.from_iso(source_iso)
    assert expected == d


@pytest.mark.parametrize(('source_iso'), [
    'Q0Y',
    'P10M20M',
    '2017-05-19T20:02:22+02:00',
])
def test_from_iso_fail(source_iso):
    with pytest.raises(ValueError):
        Duration.from_iso(source_iso)


@pytest.mark.parametrize(('a', 'b'), [
    [Duration(), Duration(years=0, days=0)],
    [Duration(years=0), Duration(years=0)],
    [Duration(years=3), Duration(years=3)],
    [Duration(days=0), Duration(days=0)],
    [Duration(days=3), Duration(days=3)],
    [Duration(minutes=3), Duration(minutes=3)],
    [Duration(years=1, days=3), Duration(years=1, days=3)],
    [Duration(years=1, days=3, minutes=5),
     Duration(years=1, days=3, minutes=5)],
])
def test_eq(a, b):
    assert a == b
    assert b == a


@pytest.mark.parametrize(('src_dt', 'duration', 'expected_sum'), [
    [
        datetime.datetime(2017, 5, 19, 21, 7, 1),
        Duration(years=3),
        datetime.datetime(2020, 5, 19, 21, 7, 1),
    ],
    [
        datetime.datetime(2016, 2, 29, 21, 7, 1),
        Duration(years=1),
        datetime.datetime(2017, 2, 28, 21, 7, 1),
    ],
    [
        datetime.datetime(2016, 2, 29, 21, 7, 1),
        Duration(years=1, days=6),
        datetime.datetime(2017, 3, 6, 21, 7, 1),
    ],
    [
        datetime.datetime(2016, 2, 29, 21, 7, 1),
        Duration(years=1, days=6, minutes=18),
        datetime.datetime(2017, 3, 6, 21, 25, 1),
    ],
    [
        pytz.timezone('Europe/Vienna').localize(
            datetime.datetime(2016, 2, 29, 21, 7, 1),
        ),
        Duration(years=1, days=6),
        pytz.timezone('Europe/Vienna').localize(
            datetime.datetime(2017, 3, 6, 21, 7, 1),
        ),
    ],
])
def test_radd_datetime(src_dt, duration, expected_sum):
    assert expected_sum == src_dt + duration
