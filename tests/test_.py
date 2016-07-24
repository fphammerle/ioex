# -*- coding: utf-8 -*-
import pytest

import pytz
import ioex
import locale
import datetime

@pytest.mark.parametrize(('locale_code'), [
    'unknown_??.utf8',
    ])
def test_setlocale_unsupported(locale_code):
    with pytest.raises(ioex.UnsupportedLocaleSettingError):
        with ioex.setlocale(locale_code):
            pass

def test_setlocale_unsupported_inheritance():
    assert issubclass(ioex.UnsupportedLocaleSettingError, locale.Error)

@pytest.mark.parametrize(('dt', 'dt_format', 'locale_code', 'expected_string'), [
    [datetime.datetime(2016, 07, 23, 1, 7, 12), '%x', 'de_DE.utf8', u'23.07.2016'],
    [datetime.datetime(2016, 07, 23, 1, 7, 12), '%X', 'de_DE.utf8', u'01:07:12'],
    [datetime.datetime(2016, 07, 23, 1, 7, 12), '%x', 'en_US.utf8', u'07/23/2016'],
    [datetime.datetime(2016, 07, 23, 1, 7, 12), '%X', 'en_US.utf8', u'01:07:12 AM'],
    [datetime.datetime(2016, 07, 23, 1, 7, 12), '%x', 'it_IT.utf8', u'23/07/2016'],
    [datetime.datetime(2016, 07, 23, 1, 7, 12), '%X', 'it_IT.utf8', u'01:07:12'],
    [datetime.datetime(2016, 07, 23, 1, 7, 12), '%x', 'zh_CN.utf8', u'2016年07月23日'],
    [datetime.datetime(2016, 07, 23, 1, 7, 12), '%X', 'zh_CN.utf8', u'01时07分12秒'],
    ])
def test_setlocale_strtime(dt, dt_format, locale_code, expected_string):
    try:
        with ioex.setlocale(locale_code):
            assert dt.strftime(dt_format).decode('utf-8') == expected_string
    except ioex.UnsupportedLocaleSettingError, ex:
        pytest.skip('locale %s unsupported' % locale_code)

@pytest.mark.parametrize(('start', 'end'), [
    [datetime.datetime(2016, 7, 24, 12, 21), datetime.datetime(2016, 7, 24, 12, 22)],
    [None, datetime.datetime(2016, 7, 24, 12, 22)],
    [datetime.datetime(2016, 7, 24, 12, 21), None],
    [None, None],
    ])
def test_dateperiod_init(start, end):
    p = ioex.DatePeriod(start = start, end = end)
    assert p.start == start
    assert p.end == end

@pytest.mark.parametrize(('start', 'end'), [
    [';-)', datetime.datetime(2016, 7, 24, 12, 22)],
    [datetime.datetime(2016, 7, 24, 12, 22), ';-)'],
    ])
def test_dateperiod_init_fail(start, end):
    with pytest.raises(TypeError):
        ioex.DatePeriod(start = start, end = end)

@pytest.mark.parametrize(('start'), [
    datetime.datetime(2016, 7, 24, 12, 21),
    None,
    ])
def test_dateperiod_set_start(start):
    p = ioex.DatePeriod()
    assert p.start is None
    p.start = start
    assert p.start == start

@pytest.mark.parametrize(('start'), [
    ':-/',
    ])
def test_dateperiod_set_start_fail(start):
    p = ioex.DatePeriod()
    with pytest.raises(TypeError):
        p.start = start

@pytest.mark.parametrize(('end'), [
    datetime.datetime(2016, 7, 24, 12, 21),
    None,
    ])
def test_dateperiod_set_end(end):
    p = ioex.DatePeriod()
    assert p.end is None
    p.end = end
    assert p.end == end

@pytest.mark.parametrize(('end'), [
    ':-/',
    ])
def test_dateperiod_set_end_fail(end):
    p = ioex.DatePeriod()
    with pytest.raises(TypeError):
        p.end = end

@pytest.mark.parametrize(('start', 'end', 'iso'), [
    [
        datetime.datetime(2016, 7, 24, 12, 21, 0),
        datetime.datetime(2016, 7, 24, 12, 22, 13),
        '2016-07-24T12:21:00/2016-07-24T12:22:13',
        ],
    [
        datetime.datetime(2016, 7, 24, 12, 21, 0, tzinfo = pytz.utc),
        datetime.datetime(2016, 7, 24, 12, 22, 13, tzinfo = pytz.utc),
        '2016-07-24T12:21:00Z/2016-07-24T12:22:13Z',
        ],
    [
        datetime.datetime(2016, 7, 24, 12, 21, 0, tzinfo = pytz.utc),
        pytz.timezone('Europe/Vienna').localize(datetime.datetime(2016, 7, 24, 12, 22, 13)),
        '2016-07-24T12:21:00Z/2016-07-24T12:22:13+02:00',
        ],
    [
        pytz.timezone('US/Pacific').localize(datetime.datetime(2016, 1, 12, 12, 22, 13)),
        pytz.timezone('Europe/London').localize(datetime.datetime(2016, 1, 24, 12, 22, 13)),
        '2016-01-12T12:22:13-08:00/2016-01-24T12:22:13Z',
        ],
    [
        datetime.datetime(2016, 7, 24, 12, 20, 0, microsecond = 25500),
        datetime.datetime(2016, 7, 24, 12, 21, 0, microsecond = 13, tzinfo = pytz.utc),
        '2016-07-24T12:20:00.025500/2016-07-24T12:21:00.000013Z',
        ],
    ])
def test_dateperiod_get_isoformat(start, end, iso):
    p = ioex.DatePeriod(start = start, end = end)
    assert p.isoformat == iso
