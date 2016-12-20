# -*- coding: utf-8 -*-
import pytest

from ioex.calcex import Figure, UnitMismatchError


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


def test_set_value_persistent():
    v = [1, 2]
    f = Figure(value=v)
    assert Figure([1, 2]) == f
    v[0] = 3
    v.append(4)
    assert Figure([1, 2]) == f


def test_set_value_persistent_deep():
    v = [{'x': 1}, {'x': 2}]
    f = Figure(value=v)
    assert Figure([{'x': 1}, {'x': 2}]) == f
    v[0]['x'] = 3
    assert Figure([{'x': 1}, {'x': 2}]) == f


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


def test_set_unit_persistent():
    u = [1, 2]
    f = Figure(0, u)
    assert Figure(0, [1, 2]) == f
    u.append(3)
    assert Figure(0, [1, 2]) == f


def test_set_unit_persistent_deep():
    u = (['N', 'm'], ['l'])
    f = Figure(0, u)
    assert Figure(0, (['N', 'm'], ['l'])) == f
    u[0].append('g')
    assert Figure(0, (['N', 'm'], ['l'])) == f


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
    assert not (a != b)


@pytest.mark.parametrize(('a', 'b'), [
    [Figure(1, 'm'), Figure(2, 'g')],
    [Figure(1, 'm'), Figure(2, 'm')],
    [Figure(2, 'm'), Figure(2, 'g')],
])
def test_neq(a, b):
    assert a != b
    assert not (a == b)


@pytest.mark.parametrize(('a', 'b', 'expected_sum'), [
    [Figure(1, 'm'), Figure(2, 'm'), Figure(3, 'm')],
    [Figure(-2, 'l'), Figure(-4, 'l'), Figure(-6, 'l')],
    [Figure(-1), Figure(3), Figure(2, None)],
])
def test_add(a, b, expected_sum):
    assert expected_sum == a + b


@pytest.mark.parametrize(('a', 'b'), [
    [Figure(1, 'm'), Figure(2, 'l')],
    [Figure(-2, 'l'), Figure(-4, None)],
])
def test_add_unit_mismatch(a, b):
    with pytest.raises(UnitMismatchError):
        a + b


def test_add_persistent():
    a = Figure([1], ['m'])
    b = Figure([2], ['m'])
    s = a + b
    assert Figure([1, 2], ['m']) == s
    a.value[0] = 3
    a.unit[0] = 'g'
    b.value[0] = 4
    b.unit[0] = 'l'
    assert Figure([1, 2], ['m']) == s


@pytest.mark.parametrize(('a', 'b', 'expected_sum'), [
    [Figure(1, 'm'), Figure(2, 'm'), Figure(-1, 'm')],
    [Figure(-2, 'l'), Figure(-4, 'l'), Figure(2, 'l')],
    [Figure(-1), Figure(3), Figure(-4, None)],
])
def test_sub(a, b, expected_sum):
    assert expected_sum == a - b


@pytest.mark.parametrize(('a', 'b'), [
    [Figure(1, 'm'), Figure(2, 'l')],
    [Figure(-2, 'l'), Figure(-4, None)],
])
def test_sub_unit_mismatch(a, b):
    with pytest.raises(UnitMismatchError):
        a - b


def test_sub_persistent():
    a = Figure(1, ['m'])
    b = Figure(2, ['m'])
    d = a - b
    assert Figure(-1, ['m']) == d
    a.value = 3
    a.unit[0] = 'g'
    b.value = 4
    b.unit[0] = 'l'
    assert Figure(-1, ['m']) == d
