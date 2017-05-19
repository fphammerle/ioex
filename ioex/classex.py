# -*- coding: utf-8 -*-


class AttributeDescriptor(object):

    def __init__(self, name, types=None, always_accept_none=False, min=None):
        self._name = name
        self._types = types
        self._always_accept_none = always_accept_none
        self._min = min

    def __get__(self, instance, owner):
        return getattr(instance, self._name)

    def __set__(self, instance, value):
        if self._always_accept_none and value is None:
            setattr(instance, self._name, None)
        elif self._types and not any([isinstance(value, t) for t in self._types]):
            raise TypeError('expected type ϵ {{{}}}, {} ({!r}) given'.format(
                ', '.join([t.__name__ for t in self._types]),
                type(value).__name__,
                value,
            ))
        elif self._min is not None and not self._min <= value:
            raise ValueError('expected value >= {!r}, {!r} given'.format(
                self._min,
                value,
            ))
        else:
            setattr(instance, self._name, value)
