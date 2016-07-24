import contextlib
import datetime
import dateutil.parser
import locale
import os
import re
import sys
import threading
try:
    import yaml
except ImportError:
    yaml = None

class UnsupportedLocaleSettingError(locale.Error):
    pass

locale_lock = threading.Lock()

@contextlib.contextmanager
def setlocale(temporary_locale):
    with locale_lock:
        primary_locale = locale.setlocale(locale.LC_ALL)
        try:
            try:
                yield locale.setlocale(locale.LC_ALL, temporary_locale)
            except locale.Error, ex:
                if ex.message == 'unsupported locale setting':
                    raise UnsupportedLocaleSettingError(temporary_locale)
                else:
                    raise ex
        finally:
            locale.setlocale(locale.LC_ALL, primary_locale)

def raw_input_with_default(prompt, default):
    import readline
    def pre_input_hook():
        readline.insert_text(default)
        readline.redisplay()
    readline.set_pre_input_hook(pre_input_hook)
    try:
        return raw_input(prompt)
    finally:
        readline.set_pre_input_hook(None)

def int_input_with_default(prompt, default):
    if default:
        default = str(default)
    else:
        default = ''
    s = raw_input_with_default(prompt, default).strip()
    if s:
        return int(s)
    else:
        return None

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

if yaml:
    yaml.add_representer(Period, Period.to_yaml)
    yaml.SafeDumper.add_representer(Period, Period.to_yaml)
    yaml.add_constructor(u'!period', Period.from_yaml)
    yaml.SafeLoader.add_constructor(u'!period', Period.from_yaml)
