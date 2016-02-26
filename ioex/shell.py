# http://misc.flogisoft.com/bash/tip_colors_and_formatting

class Formatting:
    bold = '\033[1m'
    dim = '\033[2m'
    reset_bold = '\033[21m'
    reset_dim = '\033[22m'
    reset = ''.join([reset_bold, reset_dim])

class TextColor:
    default = '\033[39m'
    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    blue = '\033[34m'
    magenta = '\033[35m'
