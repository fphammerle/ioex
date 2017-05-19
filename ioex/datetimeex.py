import datetime
import dateutil.parser
import dateutil.tz.tz
import ioex.classex
import re


def construct_yaml_timestamp(loader, node):
    loaded_dt = loader.construct_yaml_timestamp(node)
    if type(loaded_dt) is datetime.datetime and loaded_dt.tzinfo is None:
        timezone_match = re.search(
            r'(Z|(?P<sign>[\+-])(?P<h>\d{2}):(?P<m>\d{2}))$',
            loader.construct_yaml_str(node),
        )
        if timezone_match:
            # loader.construct_yaml_timestamp converts to UTC
            loaded_dt = loaded_dt.replace(tzinfo=dateutil.tz.tz.tzutc())
            timezone_attr = timezone_match.groupdict()
            if timezone_attr['h']:
                timezone = dateutil.tz.tz.tzoffset(
                    name=timezone_match.group(0),
                    offset=(
                        int(timezone_attr['h']) * 60 + int(timezone_attr['m'])) * 60
                         * (-1 if timezone_attr['sign'] == '-' else 1),
                )
                loaded_dt = loaded_dt.astimezone(timezone)
    return loaded_dt


def register_yaml_timestamp_constructor(loader, tag=u'tag:yaml.org,2002:timestamp'):
    loader.add_constructor(tag, construct_yaml_timestamp)


class Duration(object):

    yaml_tag = u'!duration'

    iso_format = r'P((?P<y>\d+)Y)?((?P<d>\d+)D)?'

    years = ioex.classex.AttributeDescriptor('_years', types=(int,), min=0)
    days = ioex.classex.AttributeDescriptor('_days', types=(int,), min=0)

    def __init__(self, years=0, days=0):
        self.years = years
        self.days = days

    @property
    def isoformat(self):
        iso_str = re.sub(
            r'(?<!\d)0.',
            '',
            'P{}Y{}D'.format(self.years, self.days),
        )
        return 'P0Y' if iso_str == 'P' else iso_str

    @classmethod
    def from_iso(cls, iso):
        match = re.search(
            r'^{}$'.format(cls.iso_format),
            iso,
        )
        if not match:
            raise ValueError('unsupported string {!r}'.format(iso))
        else:
            attr = {k: int(v) if v is not None else 0
                    for k, v in match.groupdict().items()}
            return cls(
                years=attr['y'],
                days=attr['d'],
            )

    def __eq__(self, other):
        return (type(self) == type(other)
                and self.years == other.years
                and self.days == other.days)

    @classmethod
    def from_yaml(cls, loader, node):
        return cls(**loader.construct_mapping(node))

    @classmethod
    def register_yaml_constructor(cls, loader, tag=yaml_tag):
        loader.add_constructor(tag, cls.from_yaml)

    @classmethod
    def to_yaml(cls, dumper, duration, tag=yaml_tag):
        return dumper.represent_mapping(
            tag=tag,
            mapping={k: v for k, v in {
                'years': duration.years,
                'days': duration.days,
            }.items() if v != 0},
        )

    @classmethod
    def register_yaml_representer(cls, dumper):
        dumper.add_representer(cls, cls.to_yaml)


class Period(object):

    yaml_tag = u'!period'

    _timestamp_iso_format = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(.\d+)?(Z|[-\+]\d{2}:\d{2})?'
    _timeperiod_iso_format = r'(?P<start>{t})\/(?P<end>{t})'.format(
        t=_timestamp_iso_format,
    )

    start = ioex.classex.AttributeDescriptor(
        '_start',
        types=(datetime.datetime,),
        always_accept_none=True,
    )
    end = ioex.classex.AttributeDescriptor(
        '_end',
        types=(datetime.datetime,),
        always_accept_none=True,
    )

    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end

    @property
    def isoformat(self):
        if self.start is None or self.end is None:
            raise ValueError('both start and end must be set')
        return '%s/%s' % (
            self.start.isoformat().replace('+00:00', 'Z'),
            self.end.isoformat().replace('+00:00', 'Z'),
        )

    @classmethod
    def from_iso(cls, iso):
        match = re.search(
            '^{}$'.format(cls._timeperiod_iso_format),
            iso,
        )
        if not match:
            raise ValueError(
                "given string '%s' does not match the supported pattern '%s'"
                     % (iso, cls._timeperiod_iso_format)
            )
        else:
            attr = match.groupdict()
            return cls(
                start = dateutil.parser.parse(attr['start']),
                end = dateutil.parser.parse(attr['end']),
            )

    def __eq__(self, other):
        return (type(self) == type(other)
                and self.start == other.start
                and self.end == other.end)

    @classmethod
    def from_yaml(cls, loader, node):
        return cls(**loader.construct_mapping(node))

    @classmethod
    def to_yaml(cls, dumper, period):
        return dumper.represent_mapping(
            tag=cls.yaml_tag,
            mapping={
                'start': period.start,
                'end': period.end,
            },
            # represent datetime objects with !timestamp tag
            flow_style=False,
        )

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, ', '.join([
            'start = %r' % self.start,
            'end = %r' % self.end,
        ]))

    @classmethod
    def register_yaml_constructor(cls, loader, tag=yaml_tag):
        register_yaml_timestamp_constructor(loader)
        loader.add_constructor(tag, cls.from_yaml)

    @classmethod
    def register_yaml_representer(cls, dumper):
        dumper.add_representer(cls, cls.to_yaml)
