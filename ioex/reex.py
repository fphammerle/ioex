import re


def rename_groups(pattern, name_repl):
    def pattern_repl(match):
        return '(?P<{}>'.format(name_repl(match.group(1)))
    return re.sub(
        r'\(\?P<(.*?)>',
        pattern_repl,
        pattern,
    )
