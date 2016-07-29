# -*- coding: utf-8 -*-
import pytest

import copy
import ioex.datetimeex
yaml = pytest.importorskip('yaml')

@pytest.mark.parametrize(('loader'), [yaml.Loader, yaml.SafeLoader])
@pytest.mark.parametrize(('yaml_string', 'expected_object'), [
    # ascii strings
    #
    # nota bene:
    # >>> yaml.dump('it\xc3\xa4m', allow_unicode = False) == '!!python/str "it\\xE4m"\n'
    # True
    # >>> yaml.dump('it\xc3\xa4m', allow_unicode = True) == "!!python/str 'it\xc3\xa4m'\n"
    # True
    ['item', u'item'],
    ['itäm', u'itäm'],
    ['it\xc3\xa4m', u'itäm'],
    ['"it\xc3\xa4m"', u'itäm'],
    [r'it\xE4m', ur'it\xE4m'],
    ['"itäm"', u'itäm'],
    [r'"it\xc3\xa4m"', u'it\xc3\xa4m'], # see comment above
    # unicode strings
    [r'"it\xE4m"', u'it\xE4m'],
    [r'"it\xE4m"', u'itäm'],
    [u'item', u'item'],
    [u'itäm', u'itäm'],
    ['{kĕyĭ: 可以}\n', {u'kĕyĭ': u'可以'}],
    ['{⚕: ☤}\n', {u'⚕': u'☤'}],
    # lists
    ['[item]', [u'item']],
    ['[itäm]', [u'itäm']],
    # dicts
    ['{key: value}', {u'key': u'value'}],
    ['{kï: valü}', {u'kï': u'valü'}],
    ])
def test_to_yaml(yaml_string, expected_object, loader):
    loader_copy = copy.deepcopy(loader)
    ioex.register_yaml_str_as_unicode_constructor(loader_copy)
    generated_object = yaml.load(yaml_string, Loader = loader_copy)
    assert type(expected_object) == type(generated_object)
    assert expected_object == generated_object
    if type(expected_object) is list:
        assert [type(i) for i in expected_object] == [type(i) for i in generated_object]
    elif type(expected_object) is dict:
        assert [type(k) for k in expected_object.keys()] == [type(k) for k in generated_object.keys()]
        assert [type(v) for v in expected_object.values()] == [type(v) for v in generated_object.values()]
