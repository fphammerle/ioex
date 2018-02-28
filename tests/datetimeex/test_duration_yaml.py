# -*- coding: utf-8 -*-
import pytest

from ioex.datetimeex import Duration
yaml = pytest.importorskip('yaml')


@pytest.mark.parametrize(('loader'), [yaml.Loader, yaml.SafeLoader])
@pytest.mark.parametrize(('expected_duration', 'yaml_string'), [
    [Duration(years=0),  '!duration\nyears: 0'],
    [Duration(years=32), '!duration\nyears: 32'],
    [Duration(years=0),  '!duration\n{}'],
    [Duration(years=0),  '!duration {}'],
    [Duration(days=32), '!duration\ndays: 32'],
    [Duration(minutes=0), '!duration\nminutes: 0'],
    [Duration(minutes=32), '!duration\nminutes: 32'],
    [Duration(years=1, days=3), '!duration\nyears: 1\ndays: 3'],
    [Duration(years=1, days=3, minutes=5),
     '!duration\nyears: 1\ndays: 3\nminutes: 5'],
])
def test_from_yaml(expected_duration, yaml_string, loader):
    class TestLoader(loader):
        pass
    Duration.register_yaml_constructor(TestLoader)
    loaded_duration = yaml.load(yaml_string, Loader=TestLoader)
    assert expected_duration == loaded_duration


@pytest.mark.parametrize(('loader'), [yaml.Loader, yaml.SafeLoader])
@pytest.mark.parametrize(('expected_duration', 'yaml_string', 'tag'), [
    [Duration(years=2),  '!dur\nyears: 2', '!dur'],
    [Duration(years=0), '!duration_tag {}', '!duration_tag'],
])
def test_from_yaml_tag(expected_duration, yaml_string, tag, loader):
    class TestLoader(loader):
        pass
    Duration.register_yaml_constructor(TestLoader, tag=tag)
    loaded_duration = yaml.load(yaml_string, Loader=TestLoader)
    assert expected_duration == loaded_duration


@pytest.mark.parametrize(('dumper'), [yaml.Dumper, yaml.SafeDumper])
@pytest.mark.parametrize(('duration', 'yaml_string'), [
    [Duration(years=0),  '!duration {}\n'],
    [Duration(years=32), '!duration\nyears: 32\n'],
    [Duration(days=32), '!duration\ndays: 32\n'],
    [Duration(minutes=32), '!duration\nminutes: 32\n'],
    [Duration(years=1, days=2), '!duration\ndays: 2\nyears: 1\n'],
    [Duration(days=2, minutes=0), '!duration\ndays: 2\n'],
    [Duration(days=2, minutes=5), '!duration\ndays: 2\nminutes: 5\n'],
    [Duration(years=1, days=2, minutes=5),
     '!duration\ndays: 2\nminutes: 5\nyears: 1\n'],
])
def test_to_yaml(duration, yaml_string, dumper):
    class TestDumper(dumper):
        pass
    Duration.register_yaml_representer(TestDumper)
    assert yaml_string == yaml.dump(
        duration,
        Dumper=TestDumper,
        default_flow_style=False,
    )
