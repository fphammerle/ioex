# -*- coding: utf-8 -*-
import pytest

from ioex.classex import AttributeDescriptor


class Foo(object):

    desc = AttributeDescriptor('attr')

    def __init__(self, default):
        self.attr = default


def test_set_get_attribute():
    obj = Foo(1)
    assert 1 == obj.attr
    assert 1 == obj.desc
    obj.attr = 2
    assert 2 == obj.attr
    assert 2 == obj.desc
    obj.desc = 3
    assert 3 == obj.attr
    assert 3 == obj.desc


def test_multiple_instances():
    a = Foo('a')
    b = Foo('b')
    assert 'a' == a.desc
    assert 'b' == b.desc
    a.desc = a.desc.upper()
    b.desc = b.desc.upper()
    assert 'A' == a.desc
    assert 'B' == b.desc


class Bar(object):

    a = AttributeDescriptor('_a')
    A = AttributeDescriptor('_a')
    b = AttributeDescriptor('_b')


def test_multiple_attributes():
    obj = Bar()
    obj._a = 'a'
    obj._b = 'b'
    assert 'a' == obj.a
    assert 'a' == obj.A
    assert 'b' == obj.b
    obj.A = 'A'
    obj.b = 'B'
    assert 'A' == obj.a
    assert 'A' == obj.A
    assert 'B' == obj.b


class IntAttr(AttributeDescriptor):

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError()
        else:
            super(IntAttr, self).__set__(instance, value)

class Qux(object):

    desc = IntAttr('attr')

def test_subclass():
    obj = Qux()
    obj.attr = 'first'
    assert 'first' == obj.attr
    assert 'first' == obj.desc
    obj.desc = 42
    assert 42 == obj.attr
    assert 42 == obj.desc
    with pytest.raises(TypeError):
        obj.desc = 3.14
