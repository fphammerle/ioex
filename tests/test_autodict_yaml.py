# -*- coding: utf-8 -*-
import pytest

from ioex import AutoDict
yaml = pytest.importorskip('yaml')


def test_to_yaml():
    d = AutoDict()
    d['A'] = 1.1
    d['B'][2] = 'b'
    d['C'][3]['c'] = [u'Γ', u'γ']

    class TestDumper(yaml.SafeDumper):
        pass
    TestDumper.add_representer(type(d), lambda d, c: type(c).to_yaml(d, c))
    generated_yaml = yaml.dump(
        d,
        Dumper=TestDumper,
     default_flow_style=False)

    loaded_dict = yaml.load(generated_yaml)
    assert isinstance(loaded_dict, dict)
    expected_dict = {
        'A': 1.1,
        'B': {2: 'b'},
        'C': {3: {'c': [u'Γ', u'γ']}},
    }
    assert expected_dict == loaded_dict


def test_register_yaml_representer():
    d = AutoDict()
    d['A'] = 1.1
    d['B'][2] = 'b'
    d['C'][3]['c'] = [u'Γ', u'γ']

    class TestDumper(yaml.SafeDumper):
        pass
    AutoDict.register_yaml_representer(TestDumper)
    generated_yaml = yaml.dump(
        d,
        Dumper=TestDumper,
     default_flow_style=False)

    loaded_dict = yaml.load(generated_yaml)
    assert isinstance(loaded_dict, dict)
    expected_dict = {
        'A': 1.1,
        'B': {2: 'b'},
        'C': {3: {'c': [u'Γ', u'γ']}},
    }
    assert expected_dict == loaded_dict
