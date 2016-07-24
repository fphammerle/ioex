# -*- coding: utf-8 -*-
import pytest

yaml = pytest.importorskip('yaml')
import copy
import datetime
import dateutil.tz.tz
import ioex.datetimeex
import pytz

@pytest.mark.parametrize(('loader'), [yaml.Loader, yaml.SafeLoader])
@pytest.mark.parametrize(('yaml_string', 'expected_timestamp'), [
    ['2016-07-14 13:50:04', datetime.datetime(2016, 7, 14, 13, 50, 4, 0)],
    ['2016-07-14 13:50:04Z', pytz.utc.localize(datetime.datetime(2016, 7, 14, 13, 50, 4, 0))],
    ['2016-07-14 13:50:04Z', datetime.datetime(2016, 7, 14, 13, 50, 4, 0, tzinfo = dateutil.tz.tz.tzutc())],
    ['2016-01-14 13:50:04+01:00', pytz.timezone('Europe/Vienna').localize(datetime.datetime(2016, 1, 14, 13, 50, 4, 0))],
    ['2016-07-14 13:50:04+02:00', pytz.timezone('Europe/Vienna').localize(datetime.datetime(2016, 7, 14, 13, 50, 4, 0))],
    ['2016-07-14 13:50:04+02:00', datetime.datetime(2016, 7, 14, 13, 50, 4, 0, tzinfo = dateutil.tz.tz.tzoffset('Vienna', 2 * 60 * 60))],
    ['2016-07-14 13:50:04-07:00', pytz.timezone('US/Pacific').localize(datetime.datetime(2016, 7, 14, 13, 50, 4, 0))],
    ])
def test_from_yaml(yaml_string, expected_timestamp, loader):
    loader_copy = copy.deepcopy(loader)
    ioex.datetimeex.register_yaml_timestamp_constructor(loader_copy)
    loaded_timestamp = yaml.load(yaml_string, Loader = loader_copy)
    assert loaded_timestamp == expected_timestamp
    assert loaded_timestamp.utcoffset() == expected_timestamp.utcoffset()

@pytest.mark.parametrize(('yaml_string', 'tag', 'expected_timestamp'), [
    ['!without_timezone 2016-07-14 13:50:04', '!without_timezone', datetime.datetime(2016, 7, 14, 13, 50, 4, 0)],
    ['!datetime 2016-07-14 13:50:04Z', '!datetime', pytz.utc.localize(datetime.datetime(2016, 7, 14, 13, 50, 4, 0))],
    ])
def test_from_yaml_tag(yaml_string, tag, expected_timestamp):
    loader = copy.deepcopy(yaml.SafeLoader)
    ioex.datetimeex.register_yaml_timestamp_constructor(loader, tag = tag)
    assert yaml.load(yaml_string, Loader = loader) == expected_timestamp

@pytest.mark.parametrize(('yaml_string', 'expected_timestamp'), [
    ['2016-07-14 13:50:04', datetime.datetime(2016, 7, 14, 13, 50, 4, 0)],
    ['2016-07-14 13:50:04Z', pytz.utc.localize(datetime.datetime(2016, 7, 14, 13, 50, 4, 0))],
    ])
def test_from_yaml_repeat(yaml_string, expected_timestamp):
    loader = copy.deepcopy(yaml.SafeLoader)
    ioex.datetimeex.register_yaml_timestamp_constructor(loader)
    assert yaml.load(yaml_string, Loader = loader) == expected_timestamp
    ioex.datetimeex.register_yaml_timestamp_constructor(loader)
    assert yaml.load(yaml_string, Loader = loader) == expected_timestamp
