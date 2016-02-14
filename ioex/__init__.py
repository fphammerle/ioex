import os
import sys
import locale

def curses_tty_wrapper(function, *args, **kwargs):
    stdin_fd = os.dup(sys.stdin.fileno())
    stdout_fd = os.dup(sys.stdout.fileno())
    # set stdin to tty
    tty_in = open('/dev/tty', 'r')
    os.dup2(tty_in.fileno(), sys.stdin.fileno())
    # set stdout to tty
    tty_out = open('/dev/tty', 'w')
    os.dup2(tty_out.fileno(), sys.stdout.fileno())
    # os.system('ls -l /proc/self/fd/')
    locale.setlocale(locale.LC_ALL, '')
    import curses
    result = curses.wrapper(function, *args, **kwargs)
    # reset stdin and stdout
    os.dup2(stdin_fd, sys.stdin.fileno())
    os.dup2(stdout_fd, sys.stdout.fileno())
    return result

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
