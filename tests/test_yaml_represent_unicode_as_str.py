# -*- coding: utf-8 -*-
import pytest

import ioex.datetimeex
yaml = pytest.importorskip('yaml')

@pytest.mark.parametrize(('dumper'), [yaml.Dumper, yaml.SafeDumper])
@pytest.mark.parametrize(('unicode_string', 'expected_yaml_string', 'dump_params'), [
    [[u'item'], '[item]\n', {}],
    [[u'itäm'], '["it\\xE4m"]\n', {'allow_unicode': False}],
    [[u'itäm'], '[itäm]\n', {'allow_unicode': True}],
    [{u'key': u'value'}, '{key: value}\n', {}],
    [{u'kï': u'valü'}, '{"k\\xEF": "val\\xFC"}\n', {'allow_unicode': False}],
    [{u'kï': u'valü'}, '{kï: valü}\n', {'allow_unicode': True}],
    [{u'kĕyĭ': u'可以'}, '{kĕyĭ: 可以}\n', {'allow_unicode': True}],
    [{u'⚕': u'☤'}, '{⚕: ☤}\n', {'allow_unicode': True}],
    ])
def test_to_yaml(unicode_string, expected_yaml_string, dump_params, dumper):
    # create subclass so call to class method does not interfere with other tests
    # see yaml.BaseRepresenter.add_representer()
    class TestDumper(dumper):
        pass
    ioex.register_yaml_unicode_as_str_representer(TestDumper)
    generated_yaml_string = yaml.dump(
            unicode_string,
            Dumper = TestDumper,
            default_flow_style = True,
            **dump_params
            )
    assert type(expected_yaml_string) == type(generated_yaml_string)
    assert expected_yaml_string == generated_yaml_string
