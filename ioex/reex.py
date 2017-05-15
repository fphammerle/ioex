import re


def rename_groups(pattern, name_repl):
    def pattern_repl(match):
        return '(?P<{}>'.format(name_repl(match.group(1)))
    return re.sub(
        r'\(\?P<(.*?)>',
        pattern_repl,
        pattern,
    )


def prefix_group_names(pattern, prefix):
    return rename_groups(
        pattern=pattern,
        name_repl=lambda group_name: prefix + group_name,
    )
