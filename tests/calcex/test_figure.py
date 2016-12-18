# -*- coding: utf-8 -*-
import pytest

from ioex.calcex import Figure


@pytest.mark.parametrize(('init_params', 'init_kwargs', 'expected_value', 'expected_unit'), [
    [[], {}, None, None],
    [[123.4], {}, 123.4, None],
    [[None, 'm/s²'], {}, None, 'm/s²'],
    [[123.4, 'm/s²'], {}, 123.4, 'm/s²'],
    [[1234, '米/s²'], {}, 1234, '米/s²'],
    [[], {'value': 123.4}, 123.4, None],
    [[], {'unit': 'm/s²'}, None, 'm/s²'],
    [[], {'value': 123.4, 'unit': 'm/s²'}, 123.4, 'm/s²'],
    [[], {'value': 1234, 'unit': '米/s²'}, 1234, '米/s²'],
    [[1234], {'unit': '米/s²'}, 1234, '米/s²'],
])
def test_init(init_params, init_kwargs, expected_value, expected_unit):
    f = Figure(*init_params, **init_kwargs)
    assert expected_value == f.value
    assert expected_unit == f.unit


@pytest.mark.parametrize(('init_params', 'init_kwargs'), [
    [[12.34], {'value': 123.4}],
    [[12, 'm/h'], {'unit': 'm/s²'}],
])
def test_init_multiple_values(init_params, init_kwargs):
    with pytest.raises(Exception):
        Figure(*init_params, **init_kwargs)


@pytest.mark.parametrize(('value'), [
    1234,
    123.4,
    '一千',
])
def test_set_value(value):
    f = Figure()
    assert None == f.value
    f.value = value
    assert value == f.value
    f.value = None
    assert None == f.value
    f.set_value(value)
    assert value == f.value


@pytest.mark.parametrize(('unit'), [
    'μg/l',
    '米/s²',
])
def test_set_unit(unit):
    f = Figure()
    assert None == f.unit
    f.unit = unit
    assert unit == f.unit
    f.unit = None
    assert None == f.unit
    f.set_unit(unit)
    assert unit == f.unit


@pytest.mark.parametrize(('figure', 'expected_string'), [
    [Figure(), '?'],
    [Figure(value=123.4), '123.4'],
    [Figure(unit='m/s²'), '? m/s²'],
    [Figure(value=123.4, unit='m/s²'), '123.4 m/s²'],
    [Figure(value=1234, unit='米/s²'), '1234 米/s²'],
])
def test_str(figure, expected_string):
    assert expected_string == str(figure)

@pytest.mark.parametrize(('a', 'b'), [
    [Figure(1, 'm'), Figure(1, 'm')],
])
def test_eq(a, b):
    assert a == b
    print(a == b, a != b)
    assert not (a != b)

@pytest.mark.parametrize(('a', 'b'), [
    [Figure(1, 'm'), Figure(2, 'g')],
    [Figure(1, 'm'), Figure(2, 'm')],
    [Figure(2, 'm'), Figure(2, 'g')],
])
def test_neq(a, b):
    assert a != b
    assert not (a == b)
