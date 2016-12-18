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

@pytest.mark.parametrize('yaml_loader', [yaml.Loader, yaml.SafeLoader])
@pytest.mark.parametrize('expected_object,yaml_string', [
    [datetime.datetime(2016, 7, 14, 13, 50, 4, 0), '2016-07-14 13:50:04'],
    [pytz.timezone('Europe/Vienna').localize(datetime.datetime(2016, 7, 14, 13, 50, 4, 0)), '2016-07-14 13:50:04+02:00'],
    [pytz.utc.localize(datetime.datetime(2016, 7, 14, 13, 50, 4, 0)), '2016-07-14 13:50:04+00:00'],
    [pytz.utc.localize(datetime.datetime(2016, 7, 14, 13, 50, 4, 0)), '2016-07-14 13:50:04Z'],
    ])
def test_from_yaml(expected_object, yaml_string, yaml_loader):
    loaded_object = yaml.load(yaml_string, Loader = yaml_loader)
    try:
        assert expected_object == loaded_object
    except (TypeError, AssertionError) as ex:
        # python 2.7 -> TypeError
        # python 3 -> AssertionError
        if (isinstance(expected_object, datetime.datetime)
                and not expected_object.tzinfo is None
                and loaded_object.tzinfo is None):
            pytest.xfail('pyyaml\'s loaders do not set datetime.tzinfo')
        else:
            raise ex
