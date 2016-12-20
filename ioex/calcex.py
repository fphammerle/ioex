import copy
try:
    import yaml
except ImportError:
    yaml = None


class UnitMismatchError(ValueError):
    pass


class Figure(object):

    yaml_tag = u"!figure"

    def __init__(self, value=None, unit=None):
        self.value = value
        self.unit = unit

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = copy.deepcopy(value)

    """ use property() instead of decorator to enable overriding """
    value = property(get_value, set_value)

    def get_unit(self):
        return self._unit

    def set_unit(self, unit):
        self._unit = copy.deepcopy(unit)

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

    @classmethod
    def from_yaml(cls, loader, node):
        return cls(**loader.construct_mapping(node, deep=True))

    @classmethod
    def register_yaml_constructor(cls, loader, tag=yaml_tag):
        loader.add_constructor(tag, cls.from_yaml)

    @classmethod
    def to_yaml(cls, dumper, figure, tag=yaml_tag):
        return dumper.represent_mapping(
            tag=tag,
            mapping={'value': figure.value, 'unit': figure.unit},
        )

    @classmethod
    def register_yaml_representer(cls, dumper):
        dumper.add_representer(cls, cls.to_yaml)

    def __eq__(self, other):
        return isinstance(self, type(other)) and vars(self) == vars(other)

    def __ne__(self, other):
        return not (self == other)

    def __add__(self, other):
        assert isinstance(self, type(other))
        assert not self.value is None
        assert not other.value is None
        if self.unit != other.unit:
            raise UnitMismatchError('{} + {}'.format(self, other))
        else:
            return type(self)(value=self.value + other.value, unit=self.unit)

    def __sub__(self, other):
        assert isinstance(self, type(other))
        assert not self.value is None
        assert not other.value is None
        if self.unit != other.unit:
            raise UnitMismatchError('{} - {}'.format(self, other))
        else:
            return type(self)(value=self.value - other.value, unit=self.unit)

    def __mul__(self, factor):
        if isinstance(factor, Figure):
            assert not self.value is None
            assert not factor.value is None
            assert factor.unit is None
            return type(self)(value=self.value * factor.value, unit=self.unit)
        else:
            return self * Figure(value=factor, unit=None)

    def __div__(self, divisor):
        if isinstance(divisor, Figure):
            assert not self.value is None
            assert not divisor.value is None
            assert divisor.unit is None
            return type(self)(value=self.value / divisor.value, unit=self.unit)
        else:
            return self / Figure(value=divisor, unit=None)
