# -*- coding: utf-8 -*-


class AttributeDescriptor(object):

    def __init__(self, name, types=None):
        self._name = name
        self._types = types

    def __get__(self, instance, owner):
        return getattr(instance, self._name)

    def __set__(self, instance, value):
        if self._types and not any([isinstance(value, t) for t in self._types]):
            raise TypeError('expected type ϵ {{{}}}, {} ({!r}) given'.format(
                ', '.join([t.__name__ for t in self._types]),
                type(value).__name__,
                value,
            ))
        setattr(instance, self._name, value)
