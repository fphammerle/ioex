# -*- coding: utf-8 -*-
import pytest

import copy
from ioex.datetimeex import Duration
yaml = pytest.importorskip('yaml')

@pytest.mark.parametrize(('loader'), [yaml.Loader, yaml.SafeLoader])
@pytest.mark.parametrize(('expected_duration', 'yaml_string'), [
    [Duration(years = 0),  '!duration\nyears: 0'],
    [Duration(years = 32), '!duration\nyears: 32'],
    [Duration(years = 0),  '!duration\n{}'],
    [Duration(years = 0),  '!duration {}'],
    ])
def test_from_yaml(expected_duration, yaml_string, loader):
    loader_copy = copy.deepcopy(loader)
    Duration.register_yaml_constructor(loader_copy)
    loaded_duration = yaml.load(yaml_string, Loader = loader_copy)
    assert expected_duration == loaded_duration

@pytest.mark.parametrize(('loader'), [yaml.Loader, yaml.SafeLoader])
@pytest.mark.parametrize(('expected_duration', 'yaml_string', 'tag'), [
    [Duration(years = 2),  '!dur\nyears: 2', '!dur'],
    [Duration(years = 0), '!duration_tag {}', '!duration_tag'],
    ])
def test_from_yaml(expected_duration, yaml_string, tag, loader):
    loader_copy = copy.deepcopy(loader)
    Duration.register_yaml_constructor(loader_copy, tag = tag)
    loaded_duration = yaml.load(yaml_string, Loader = loader_copy)
    assert expected_duration == loaded_duration

@pytest.mark.parametrize(('dumper'), [yaml.Dumper, yaml.SafeDumper])
@pytest.mark.parametrize(('duration', 'yaml_string'), [
    [Duration(years = 0),  '!duration {}\n'],
    [Duration(years = 32), '!duration\nyears: 32\n'],
    ])
def test_to_yaml(duration, yaml_string, dumper):
    dumper_copy = copy.deepcopy(dumper)
    Duration.register_yaml_representer(dumper_copy)
    assert yaml.dump(duration, Dumper = dumper_copy, default_flow_style = False) == yaml_string
