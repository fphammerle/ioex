import os
import sys
import locale
import threading
import contextlib

locale_lock = threading.Lock()

@contextlib.contextmanager
def setlocale(temporary_locale):
    with locale_lock:
        primary_locale = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, temporary_locale)
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
