import datetime
import dateutil.parser
import dateutil.tz.tz
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
            loaded_dt = loaded_dt.replace(tzinfo = dateutil.tz.tz.tzutc())
            timezone_attr = timezone_match.groupdict()
            if timezone_attr['h']:
                timezone = dateutil.tz.tz.tzoffset(
                        name = timezone_match.group(0),
                        offset = (int(timezone_attr['h']) * 60 + int(timezone_attr['m'])) * 60
                            * (-1 if timezone_attr['sign'] == '-' else 1),
                        )
                loaded_dt = loaded_dt.astimezone(timezone)
    return loaded_dt

def register_yaml_timestamp_constructor(loader, tag = u'tag:yaml.org,2002:timestamp'):
    loader.add_constructor(tag, construct_yaml_timestamp)

class Duration(object):

    yaml_tag = u'!duration'

    def __init__(self, years = 0):
        self.years = years

    @property
    def years(self):
        return self._years

    @years.setter
    def years(self, years):
        if not type(years) is int:
            raise TypeError('expected int, %r given' % years)
        elif years < 0:
            raise ValueError('number of years must be >= 0, %r given' % years)
        else:
            self._years = years

    @property
    def isoformat(self):
        return 'P%dY' % self.years

    def __eq__(self, other):
        return (type(self) == type(other)
                and self.years == other.years)

    @classmethod
    def from_yaml(cls, loader, node):
        return cls(**loader.construct_mapping(node))

    @classmethod
    def register_yaml_constructor(cls, loader, tag = yaml_tag):
        loader.add_constructor(tag, cls.from_yaml)

    @classmethod
    def to_yaml(cls, dumper, duration, tag = yaml_tag):
        return dumper.represent_mapping(
            tag = tag,
            mapping = {k: v for k, v in {
                'years': duration.years,
                }.items() if v != 0},
            )

    @classmethod
    def register_yaml_representer(cls, dumper):
        dumper.add_representer(cls, cls.to_yaml)

class Period(object):

    yaml_tag = u'!period'

    _timestamp_iso_format = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(.\d+)?(Z|[-\+]\d{2}:\d{2})?'
    _timeperiod_iso_format = r'(?P<start>%(t)s)\/(?P<end>%(t)s)' % {'t': _timestamp_iso_format}

    def __init__(self, start = None, end = None, isoformat = None):
        self._start = None
        self._end = None
        if (start or end) and isoformat:
            raise AttributeError('when providing isoformat no other parameters may be specified')
        elif isoformat:
            self.isoformat = isoformat
        else:
            self.start = start
            self.end = end

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        if not (start is None or type(start) is datetime.datetime):
            raise TypeError()
        self._start = start

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        if not (end is None or type(end) is datetime.datetime):
            raise TypeError()
        self._end = end

    @property
    def isoformat(self):
        if self.start is None or self.end is None:
            raise ValueError('both start and end must be set')
        return '%s/%s' % (
                self.start.isoformat().replace('+00:00', 'Z'),
                self.end.isoformat().replace('+00:00', 'Z'),
                )

    @isoformat.setter
    def isoformat(self, text):
        match = re.search('^%s$' % self.__class__._timeperiod_iso_format, text)
        if not match:
            raise ValueError(
                    "given string '%s' does not match the supported pattern '%s'"
                     % (text, self.__class__._timeperiod_iso_format)
                     )
        attr = match.groupdict()
        self.start = dateutil.parser.parse(attr['start'])
        self.end = dateutil.parser.parse(attr['end'])

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
            tag = cls.yaml_tag,
            mapping = {
                'start': period.start,
                'end': period.end,
                },
            # represent datetime objects with !timestamp tag
            flow_style = False,
            )

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, ', '.join([
            'start = %r' % self.start,
            'end = %r' % self.end,
            ]))

    @classmethod
    def register_yaml_constructor(cls, loader, tag = yaml_tag):
        register_yaml_timestamp_constructor(loader)
        loader.add_constructor(tag, cls.from_yaml)

    @classmethod
    def register_yaml_representer(cls, dumper):
        dumper.add_representer(cls, cls.to_yaml)
