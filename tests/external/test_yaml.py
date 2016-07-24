# -*- coding: utf-8 -*-
import pytest

yaml = pytest.importorskip('yaml')
import datetime
import pytz

@pytest.mark.parametrize('source_object,yaml_string', [
    [datetime.datetime(2016, 7, 14, 13, 50, 4, 0), '2016-07-14 13:50:04\n...\n'],
    [pytz.timezone('Europe/Vienna').localize(datetime.datetime(2016, 7, 14, 13, 50, 4, 0)), '2016-07-14 13:50:04+02:00\n...\n'],
    [pytz.utc.localize(datetime.datetime(2016, 7, 14, 13, 50, 4, 0)), '2016-07-14 13:50:04+00:00\n...\n'],
    ])
def test_to_yaml(source_object, yaml_string):
    assert yaml.dump(source_object) == yaml_string
    assert yaml.safe_dump(source_object) == yaml_string

@pytest.mark.parametrize('expected_object,yaml_string', [
    [datetime.datetime(2016, 7, 14, 13, 50, 4, 0), '2016-07-14 13:50:04'],
    [pytz.timezone('Europe/Vienna').localize(datetime.datetime(2016, 7, 14, 13, 50, 4, 0)), '2016-07-14 13:50:04+02:00'],
    [pytz.utc.localize(datetime.datetime(2016, 7, 14, 13, 50, 4, 0)), '2016-07-14 13:50:04+00:00'],
    [pytz.utc.localize(datetime.datetime(2016, 7, 14, 13, 50, 4, 0)), '2016-07-14 13:50:04Z'],
    ])
def test_from_yaml(expected_object, yaml_string):
    try:
        assert expected_object == yaml.load(yaml_string)
        assert expected_object == yaml.safe_load(yaml_string)
    except TypeError, ex:
        if (isinstance(expected_object, datetime.datetime) 
                and not expected_object.tzinfo is None
                and "can't compare offset-naive and offset-aware datetimes" in ex.message):
            pytest.xfail('pyyaml\'s loaders do not set datetime.tzinfo')
        else:
            raise ex
