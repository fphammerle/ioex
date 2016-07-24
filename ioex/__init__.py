import os
import sys
import locale
import datetime
import threading
import contextlib

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

class DatePeriod(object):

    def __init__(self, start = None, end = None):
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
