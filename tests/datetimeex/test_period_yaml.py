# -*- coding: utf-8 -*-
import pytest

import copy
import datetime
import ioex.datetimeex
import pytz
yaml = pytest.importorskip('yaml')

@pytest.mark.parametrize(('loader'), [yaml.Loader, yaml.SafeLoader])
@pytest.mark.parametrize(('expected_period', 'yaml_string'), [
    [
        ioex.datetimeex.Period(
            start = datetime.datetime(2016, 7, 24, 12, 21, 0),
            end = datetime.datetime(2016, 7, 24, 12, 22, 13),
            ),
        '!period\nstart: 2016-07-24T12:21:00\nend: 2016-07-24T12:22:13',
        ],
    [
        ioex.datetimeex.Period(
            start = datetime.datetime(2016, 7, 24, 12, 21, 0),
            end = datetime.datetime(2016, 7, 24, 12, 22, 13),
            ),
        '!period\nstart: 2016-07-24 12:21:00\nend: 2016-07-24 12:22:13',
        ],
    [
        ioex.datetimeex.Period(
            start = datetime.datetime(2016, 7, 24, 12, 20, 0, microsecond = 25500),
            end = datetime.datetime(2016, 7, 24, 12, 21, 0, microsecond = 13),
            ),
        '!period\nstart: 2016-07-24T12:20:00.025500\nend: 2016-07-24T12:21:00.000013',
        ],
    [
        ioex.datetimeex.Period(
            start = datetime.datetime(2016, 7, 24, 12, 20, 0, microsecond = 25500),
            end = pytz.utc.localize(datetime.datetime(2016, 7, 24, 12, 21, 0, microsecond = 13)),
            ),
        '!period\nstart: 2016-07-24T12:20:00.025500\nend: 2016-07-24T12:21:00.000013Z',
        ],
    [
        ioex.datetimeex.Period(
            start = pytz.timezone('Europe/London').localize(datetime.datetime(2016, 1, 24, 12, 20, 0, microsecond = 25500)),
            end = pytz.timezone('Europe/London').localize(datetime.datetime(2016, 7, 24, 12, 21, 0, microsecond = 13)),
            ),
        '!period\nstart: 2016-01-24T12:20:00.025500Z\nend: 2016-07-24T12:21:00.000013+01:00',
        ],
    ])
def test_from_yaml(expected_period, yaml_string, loader):
    loader_copy = copy.deepcopy(loader)
    loaded_period = yaml.load(yaml_string, Loader = loader_copy)
    assert expected_period == loaded_period
    assert expected_period.start.utcoffset() == loaded_period.start.utcoffset()
    assert expected_period.end.utcoffset() == loaded_period.end.utcoffset()

@pytest.mark.parametrize(('period', 'yaml_string'), [
    [
        ioex.datetimeex.Period(
            start = datetime.datetime(2016, 7, 24, 12, 21, 0),
            end = datetime.datetime(2016, 7, 24, 12, 22, 13),
            ),
        '!period\nend: 2016-07-24 12:22:13\nstart: 2016-07-24 12:21:00\n',
        ],
    [
        ioex.datetimeex.Period(
            start = datetime.datetime(2016, 7, 24, 12, 20, 0, microsecond = 25500),
            end = datetime.datetime(2016, 7, 24, 12, 21, 0, microsecond = 13),
            ),
        '!period\nend: 2016-07-24 12:21:00.000013\nstart: 2016-07-24 12:20:00.025500\n',
        ],
    [
        ioex.datetimeex.Period(
            start = pytz.timezone('Europe/London').localize(datetime.datetime(2016, 7, 24, 12, 20, 0)),
            end = pytz.utc.localize(datetime.datetime(2016, 7, 24, 12, 21, 0, microsecond = 13)),
            ),
        '!period\nend: 2016-07-24 12:21:00.000013+00:00\nstart: 2016-07-24 12:20:00+01:00\n',
        ],
    ])
def test_to_yaml(period, yaml_string):
    assert yaml.dump(period) == yaml_string
    assert yaml.safe_dump(period) == yaml_string
