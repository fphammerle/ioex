import copy
try:
    import yaml
    import yaml.nodes
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
        if isinstance(node, yaml.nodes.ScalarNode):
            seg = loader.construct_scalar(node).split(' ')
            if seg[0] == '?':
                value = None
            else:
                try:
                    value = int(seg[0])
                except ValueError:
                    value = float(seg[0])
            return cls(
                value=value,
                unit=' '.join(seg[1:]) if len(seg) > 1 else None,
            )
        else:
            return cls(**loader.construct_mapping(node, deep=True))

    @classmethod
    def register_yaml_constructor(cls, loader, tag=None):
        loader.add_constructor(
            cls.yaml_tag if tag is None else tag,
            cls.from_yaml,
        )

    @classmethod
    def to_yaml(cls, dumper, figure, tag=yaml_tag):
        if figure.value is None or type(figure.value) in [int, float]:
            if figure.value is None:
                value_text = u'?'
            else:
                value_text = u'{}'.format(figure.value)
            if figure.unit is None:
                figure_text = value_text
            else:
                figure_text = u'{} {}'.format(value_text, figure.unit)
            return dumper.represent_scalar(tag=tag, value=figure_text)
        else:
            return dumper.represent_mapping(
                tag=tag,
                mapping={'value': figure.value, 'unit': figure.unit},
            )

    @classmethod
    def register_yaml_representer(cls, dumper, tag=yaml_tag):
        dumper.add_representer(cls, lambda d, f: cls.to_yaml(d, f, tag=tag))

    def __eq__(self, other):
        return isinstance(self, type(other)) and vars(self) == vars(other)

    def __ne__(self, other):
        return not (self == other)

    def __add__(self, other):
        if not isinstance(self, type(other)):
            raise NotImplementedError('{!r} + {!r}'.format(self, other))
        assert not self.value is None
        assert not other.value is None
        if self.unit != other.unit:
            raise UnitMismatchError('{} + {}'.format(self, other))
        else:
            return type(self)(value=self.value + other.value, unit=self.unit)

    def __radd__(self, other):
        """ enables use of sum() """
        if isinstance(other, int) and other == 0:
            return copy.deepcopy(self)
        else:
            raise NotImplementedError('{!r} + {!r}'.format(other, self))

    def __sub__(self, other):
        if not isinstance(self, type(other)):
            raise NotImplementedError('{!r} - {!r}'.format(self, other))
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

    """
    $ python2
    >>> 3/2
    1
    $ python3
    >>> 3/2
    1.5
    >>> 4/2
    2.0
    """

    def __truediv__(self, divisor):
        if isinstance(divisor, Figure):
            assert not self.value is None
            assert not divisor.value is None
            if isinstance(self.value, int):
                value = float(self.value) / divisor.value
            else:
                value = self.value / divisor.value
            if self.unit == divisor.unit:
                return Figure(value=value, unit=None)
            elif divisor.unit is None:
                return type(self)(value=value, unit=self.unit)
            else:
                raise NotImplementedError('{!r} / {!r}'.format(self, divisor))
        else:
            return self / Figure(value=divisor, unit=None)

    def __div__(self, divisor):
        return self.__truediv__(divisor)
