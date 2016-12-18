import contextlib
import difflib
import ioex.shell
import locale
import readline
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
            except locale.Error as ex:
                if str(ex) == 'unsupported locale setting':
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
    try:
        dumper.add_representer(unicode, yaml_represent_unicode_as_str)
    except NameError: # python3
        pass

def yaml_construct_str_as_unicode(loader, node):
    string = loader.construct_scalar(node)
    try:
        return string if type(string) is unicode else string.decode('utf-8')
    except NameError: # python3
        return string

def register_yaml_str_as_unicode_constructor(loader):
    loader.add_constructor(u'tag:yaml.org,2002:str', yaml_construct_str_as_unicode)

yaml_diff_colors = {
    ' ': ioex.shell.TextColor.default,
    '+': ioex.shell.TextColor.green,
    '-': ioex.shell.TextColor.red,
    '?': ioex.shell.TextColor.yellow,
    }

def yaml_diff(a, b, dumper = None, colors = False):
    if dumper is None:
        class DiffDumper(yaml.Dumper):
            pass
        register_yaml_unicode_as_str_representer(DiffDumper)
        dumper = DiffDumper
    def to_yaml(data):
        return yaml.dump(
                data,
                Dumper = dumper,
                default_flow_style = False,
                allow_unicode = True,
                )
    diff_lines = difflib.ndiff(
        to_yaml(a).splitlines(True),
        to_yaml(b).splitlines(True),
        )
    if colors:
        diff_lines = [u'%s%s%s' % (yaml_diff_colors[l[0]], l, ioex.shell.TextColor.default) for l in diff_lines]
    return u''.join(diff_lines)
