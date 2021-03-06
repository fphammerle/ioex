# -*- coding: utf-8 -*-
import pytest

import pytz
import ioex.datetimeex
import datetime


@pytest.mark.parametrize(('start', 'end'), [
    [datetime.datetime(2016, 7, 24, 12, 21),
     datetime.datetime(2016, 7, 24, 12, 22)],
    [None, datetime.datetime(2016, 7, 24, 12, 22)],
    [datetime.datetime(2016, 7, 24, 12, 21), None],
    [None, None],
])
def test_init_start_end(start, end):
    p = ioex.datetimeex.Period(start=start, end=end)
    assert p.start == start
    assert p.end == end


@pytest.mark.parametrize(('start', 'end'), [
    [';-)', datetime.datetime(2016, 7, 24, 12, 22)],
    [datetime.datetime(2016, 7, 24, 12, 22), ';-)'],
])
def test_init_start_end_fail(start, end):
    with pytest.raises(TypeError):
        ioex.datetimeex.Period(start=start, end=end)


@pytest.mark.parametrize(('start'), [
    datetime.datetime(2016, 7, 24, 12, 21),
    None,
])
def test_set_start(start):
    p = ioex.datetimeex.Period()
    assert p.start is None
    p.start = start
    assert p.start == start


@pytest.mark.parametrize(('start'), [
    ':-/',
])
def test_set_start_fail(start):
    p = ioex.datetimeex.Period()
    with pytest.raises(TypeError):
        p.start = start


@pytest.mark.parametrize(('end'), [
    datetime.datetime(2016, 7, 24, 12, 21),
    None,
])
def test_set_end(end):
    p = ioex.datetimeex.Period()
    assert p.end is None
    p.end = end
    assert p.end == end


@pytest.mark.parametrize(('end'), [
    ':-/',
])
def test_set_end_fail(end):
    p = ioex.datetimeex.Period()
    with pytest.raises(TypeError):
        p.end = end


@pytest.mark.parametrize(('start', 'end', 'iso'), [
    [
        datetime.datetime(2016, 7, 24, 12, 21, 0),
        datetime.datetime(2016, 7, 24, 12, 22, 13),
        '2016-07-24T12:21:00/2016-07-24T12:22:13',
    ],
    [
        datetime.datetime(2016, 7, 24, 12, 21, 0, tzinfo=pytz.utc),
        datetime.datetime(2016, 7, 24, 12, 22, 13, tzinfo=pytz.utc),
        '2016-07-24T12:21:00Z/2016-07-24T12:22:13Z',
    ],
    [
        datetime.datetime(2016, 7, 24, 12, 21, 0, tzinfo=pytz.utc),
        pytz.timezone('Europe/Vienna').localize(
            datetime.datetime(2016, 7, 24, 12, 22, 13)
        ),
        '2016-07-24T12:21:00Z/2016-07-24T12:22:13+02:00',
    ],
    [
        pytz.timezone('US/Pacific').localize(
            datetime.datetime(2016, 1, 12, 12, 22, 13)
        ),
        pytz.timezone('Europe/London').localize(
            datetime.datetime(2016, 1, 24, 12, 22, 13)
        ),
        '2016-01-12T12:22:13-08:00/2016-01-24T12:22:13Z',
    ],
    [
        datetime.datetime(2016, 7, 24, 12, 20, 0, microsecond=25500),
        datetime.datetime(
            2016, 7, 24, 12, 21, 0,
            microsecond=13,
            tzinfo=pytz.utc,
        ),
        '2016-07-24T12:20:00.025500/2016-07-24T12:21:00.000013Z',
    ],
])
def test_get_isoformat(start, end, iso):
    p = ioex.datetimeex.Period(start=start, end=end)
    assert p.isoformat == iso


@pytest.mark.parametrize(('start', 'end', 'source_iso'), [
    [
        datetime.datetime(2016, 7, 24, 12, 21, 0),
        datetime.datetime(2016, 7, 24, 12, 22, 13),
        '2016-07-24T12:21:00/2016-07-24T12:22:13',
    ],
    [
        datetime.datetime(2016, 7, 24, 12, 21, 0, tzinfo=pytz.utc),
        datetime.datetime(2016, 7, 24, 12, 22, 13, tzinfo=pytz.utc),
        '2016-07-24T12:21:00Z/2016-07-24T12:22:13Z',
    ],
    [
        datetime.datetime(2016, 7, 24, 12, 21, 0, tzinfo=pytz.utc),
        pytz.timezone('Europe/Vienna').localize(
            datetime.datetime(2016, 7, 24, 12, 22, 13)
        ),
        '2016-07-24T12:21:00Z/2016-07-24T12:22:13+02:00',
    ],
    [
        pytz.timezone('US/Pacific').localize(
            datetime.datetime(2016, 1, 12, 12, 22, 13)
        ),
        pytz.timezone('Europe/London').localize(
            datetime.datetime(2016, 1, 24, 12, 22, 13)
        ),
        '2016-01-12T12:22:13-08:00/2016-01-24T12:22:13Z',
    ],
    [
        datetime.datetime(2016, 7, 24, 12, 20, 0, microsecond=25500),
        datetime.datetime(
            2016, 7, 24, 12, 21, 0,
            microsecond=13,
            tzinfo=pytz.utc,
        ),
        '2016-07-24T12:20:00.025500/2016-07-24T12:21:00.000013Z',
    ],
    [
        datetime.datetime(2016, 7, 24, 12, 20, 0, microsecond=25500),
        datetime.datetime(
            2016, 7, 24, 12, 21, 0,
            microsecond=130000,
            tzinfo=pytz.utc,
        ),
        '2016-07-24T12:20:00.0255/2016-07-24T12:21:00.13Z',
    ],
])
def test_from_iso(start, end, source_iso):
    p = ioex.datetimeex.Period.from_iso(source_iso)
    assert p.start == start
    assert p.end == end


@pytest.mark.parametrize(('source_iso'), [
    '2016-07-24T12:20:0<INVALID>0.0255/2016-07-24T12:21:00.13Z',
])
def test_from_iso_fail(source_iso):
    with pytest.raises(ValueError):
        ioex.datetimeex.Period.from_iso(source_iso)


@pytest.mark.parametrize(('a', 'b'), [
    [
        ioex.datetimeex.Period(
            start=datetime.datetime(2016, 7, 24, 12, 21, 0),
            end=datetime.datetime(2016, 7, 24, 12, 22, 13),
        ),
        ioex.datetimeex.Period(
            start=datetime.datetime(2016, 7, 24, 12, 21, 0, 0),
            end=datetime.datetime(2016, 7, 24, 12, 22, 13, 0),
        ),
    ],
    [
        ioex.datetimeex.Period(
            start=pytz.timezone('Europe/Vienna').localize(
                datetime.datetime(2016, 7, 24, 12, 21, 0)
            ),
            end=datetime.datetime(2016, 7, 24, 12, 22, 13),
        ),
        ioex.datetimeex.Period(
            start=pytz.timezone('Europe/Vienna').localize(
                datetime.datetime(2016, 7, 24, 12, 21, 0)
            ),
            end=datetime.datetime(2016, 7, 24, 12, 22, 13),
        ),
    ],
    [
        ioex.datetimeex.Period(
            start=pytz.timezone('Europe/Vienna').localize(
                datetime.datetime(2016, 7, 24, 12, 21, 0)
            ),
            end=pytz.timezone('Europe/London').localize(
                datetime.datetime(2016, 7, 24, 12, 22, 13)
            ),
        ),
        ioex.datetimeex.Period(
            start=pytz.timezone('Europe/London').localize(
                datetime.datetime(2016, 7, 24, 11, 21, 0)
            ),
            end=pytz.timezone('Europe/Vienna').localize(
                datetime.datetime(2016, 7, 24, 13, 22, 13)
            ),
        ),
    ],
])
def test_eq(a, b):
    assert a == b
    assert b == a
