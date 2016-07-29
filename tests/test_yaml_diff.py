# -*- coding: utf-8 -*-
import pytest

yaml = pytest.importorskip('yaml')
import datetime
import ioex.datetimeex
import ioex.debug
from ioex.shell import TextColor

@pytest.mark.parametrize(('a', 'b', 'expected_diff_lines'), [
    [
        [1, 2, 3],
        [1, 2, 3],
        [
            u'  - 1',
            u'  - 2',
            u'  - 3',
            ],
        ],
    [
        [1, 2, 3],
        [1, 3],
        [
            u'  - 1',
            u'- - 2',
            u'  - 3',
            ],
        ],
    [
        [1, 3],
        [1, 2, 3],
        [
            u'  - 1',
            u'+ - 2',
            u'  - 3',
            ],
        ],
    [
        u'abcdef',
        u'abdf',
        [
            u"- abcdef",
            u"?   - -",
            u"+ abdf",
            u"  ...",
            ],
        ],
    [
        u'äbcdef',
        u'äbcdÜf',
        [
            u"- äbcdef",
            u"?     ^",
            u"+ äbcdÜf",
            u"?     ^",
            u"  ...",
            ],
        ],
    [
        ioex.datetimeex.Duration(years = 2),
        ioex.datetimeex.Duration(years = 2),
        [
            u'  !duration',
            u'  years: 2',
            ],
        ],
    [
        ioex.datetimeex.Duration(years = 1),
        ioex.datetimeex.Duration(years = 2),
        [
            u'  !duration',
            u'- years: 1',
            u'?        ^',
            u'+ years: 2',
            u'?        ^',
            ],
        ],
    [
        ioex.datetimeex.Period(
            start = datetime.datetime(2016, 7, 29, 21, 59, 13),
            end = datetime.datetime(2017, 8, 30, 22, 32, 12),
            ),
        ioex.datetimeex.Period(
            start = datetime.datetime(2016, 7, 29, 21, 59, 13),
            end = datetime.datetime(2017, 8, 30, 23, 32, 12),
            ),
        [
            u'  !period',
            u'- end: 2017-08-30 22:32:12',
            u'?                  ^',
            u'+ end: 2017-08-30 23:32:12',
            u'?                  ^',
            u'  start: 2016-07-29 21:59:13',
            ],
        ],
    ])
def test_yaml_diff(a, b, expected_diff_lines):
    class TestDumper(yaml.SafeDumper):
        pass
    ioex.datetimeex.Duration.register_yaml_representer(TestDumper)
    ioex.datetimeex.Period.register_yaml_representer(TestDumper)
    expected_diff = u'\n'.join(expected_diff_lines) + u'\n'
    generated_diff = ioex.yaml_diff(a, b, dumper = TestDumper)
    assert expected_diff == generated_diff, \
            '\ngenerated: %r\nexpected:  %r' % (generated_diff, expected_diff)

@pytest.mark.parametrize(('a', 'b', 'expected_diff_lines'), [
    [
        [1, 2, 3],
        [1, 3, 4],
        [
            TextColor.default + u'  - 1',
            TextColor.red     + u'- - 2',
            TextColor.default + u'  - 3',
            TextColor.green   + u'+ - 4',
            ],
        ],
    [
        'abcef',
        'abdef',
        [
            TextColor.red     + u'- abcef',
            TextColor.yellow  + u'?   ^',
            TextColor.green   + u'+ abdef',
            TextColor.yellow  + u'?   ^',
            TextColor.default + u'  ...',
            ],
        ],
    [
        {'a': True, 'b': 123, 'c': 'string', 'd': 1.23},
        {'a': True, 'b': 123, 'c': 'string', 'd': 1.23},
        [
            TextColor.default + u'  a: true',
            TextColor.default + u'  b: 123',
            TextColor.default + u'  c: string',
            TextColor.default + u'  d: 1.23',
            ],
        ],
    [
        {'a': True,  'b': 123, 'c': 'str',    'd': 1.23},
        {'a': False, 'b': 13,  'c': 'string', 'd': 12.3},
        [
            TextColor.red     + u'- a: true',
            TextColor.green   + u'+ a: false',
            TextColor.red     + u'- b: 123',
            TextColor.yellow  + u'?     -',
            TextColor.green   + u'+ b: 13',
            TextColor.red     + u'- c: str',
            TextColor.green   + u'+ c: string',
            TextColor.yellow  + u'?       +++',
            TextColor.red     + u'- d: 1.23',
            TextColor.yellow  + u'?      -',
            TextColor.green   + u'+ d: 12.3',
            TextColor.yellow  + u'?     +',
            ],
        ],
    ])
def test_yaml_diff(a, b, expected_diff_lines):
    expected_diff = (u'\n' + TextColor.default).join(expected_diff_lines) + u'\n' + TextColor.default
    generated_diff = ioex.yaml_diff(a, b, colors = True)
    assert expected_diff == generated_diff, \
            '\ngenerated: %r\nexpected:  %r' % (generated_diff, expected_diff)
