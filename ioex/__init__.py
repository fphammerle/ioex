import contextlib
import locale
import readline
import threading

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

def yaml_represent_unicode_as_str(dumper, unicode_string):
    return dumper.represent_scalar(u'tag:yaml.org,2002:str', unicode_string)

def register_yaml_unicode_as_str_representer(dumper):
    dumper.add_representer(unicode, yaml_represent_unicode_as_str)
