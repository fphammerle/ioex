# -*- coding: utf-8 -*-
import pytest

import pytz
import ioex
import datetime
yaml = pytest.importorskip('yaml')

@pytest.mark.parametrize(('period', 'yaml_string'), [
    [
        ioex.DatePeriod(
            start = datetime.datetime(2016, 7, 24, 12, 21, 0),
            end = datetime.datetime(2016, 7, 24, 12, 22, 13),
            ),
        '!period\nstart: 2016-07-24T12:21:00\nend: 2016-07-24T12:22:13',
        ],
    [
        ioex.DatePeriod(
            start = datetime.datetime(2016, 7, 24, 12, 21, 0),
            end = datetime.datetime(2016, 7, 24, 12, 22, 13),
            ),
        '!period\nstart: 2016-07-24 12:21:00\nend: 2016-07-24 12:22:13',
        ],
    [
        ioex.DatePeriod(
            start = datetime.datetime(2016, 7, 24, 12, 20, 0, microsecond = 25500),
            end = datetime.datetime(2016, 7, 24, 12, 21, 0, microsecond = 13),
            ),
        '!period\nstart: 2016-07-24T12:20:00.025500\nend: 2016-07-24T12:21:00.000013',
        ],
    [
        ioex.DatePeriod(
            start = datetime.datetime(2016, 7, 24, 12, 20, 0, microsecond = 25500),
            end = datetime.datetime(2016, 7, 24, 12, 21, 0, microsecond = 13, tzinfo = pytz.utc),
            ),
        '!period\nstart: 2016-07-24T12:20:00.025500\nend: 2016-07-24T12:21:00.000013Z',
        ],
    ])
def test_dateperiod_from_yaml(period, yaml_string):
    if period.start.tzinfo or period.end.tzinfo: 
        pytest.xfail('pyyaml ignores timezones when loading timestamps')
    assert period == yaml.load(yaml_string)
    assert period == yaml.safe_load(yaml_string)

@pytest.mark.parametrize(('period', 'yaml_string'), [
    [
        ioex.DatePeriod(
            start = datetime.datetime(2016, 7, 24, 12, 21, 0),
            end = datetime.datetime(2016, 7, 24, 12, 22, 13),
            ),
        '!period\nend: 2016-07-24 12:22:13\nstart: 2016-07-24 12:21:00\n',
        ],
    [
        ioex.DatePeriod(
            start = datetime.datetime(2016, 7, 24, 12, 20, 0, microsecond = 25500),
            end = datetime.datetime(2016, 7, 24, 12, 21, 0, microsecond = 13),
            ),
        '!period\nend: 2016-07-24 12:21:00.000013\nstart: 2016-07-24 12:20:00.025500\n',
        ],
    [
        ioex.DatePeriod(
            start = pytz.timezone('Europe/London').localize(datetime.datetime(2016, 7, 24, 12, 20, 0)),
            end = pytz.utc.localize(datetime.datetime(2016, 7, 24, 12, 21, 0, microsecond = 13)),
            ),
        '!period\nend: 2016-07-24 12:21:00.000013+00:00\nstart: 2016-07-24 12:20:00+01:00\n',
        ],
    ])
def test_dateperiod_to_yaml(period, yaml_string):
    assert yaml.dump(period) == yaml_string
    assert yaml.safe_dump(period) == yaml_string
