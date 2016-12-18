# try:
#     import yaml
# except ImportError:
#     yaml = None


class UnitMismatchError(ValueError):
    pass


class Figure(object):

    yaml_tag = u"!figure"

    def __init__(self, value=None, unit=None):
        self._value = value
        self._unit = unit

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    """ use property() instead of decorator to enable overriding """
    value = property(get_value, set_value)

    def get_unit(self):
        return self._unit

    def set_unit(self, unit):
        self._unit = unit

    """ use property() instead of decorator to enable overriding """
    unit = property(get_unit, set_unit)

    def __repr__(self):
        return '{}(value = {!r}, unit = {})'.format(type(self).__name__, self.value, self.unit)

    def __str__(self):
        if self.value is None and self.unit is None:
            return '?'
        elif self.unit is None:
            return '{}'.format(self.value)
        elif self.value is None:
            return '? {}'.format(self.unit)
        else:
            return '{} {}'.format(self.value, self.unit)

    def __eq__(self, other):
        return type(self) == type(other) and vars(self) == vars(other)

    def __ne__(self, other):
        return not (self == other)
