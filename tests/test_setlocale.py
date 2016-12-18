# -*- coding: utf-8 -*-
import pytest

import ioex
import locale
import datetime

@pytest.mark.parametrize(('locale_code'), [
    'unknown_??.utf8',
    ])
def test_setlocale_unsupported(locale_code):
    with pytest.raises(ioex.UnsupportedLocaleSettingError):
        with ioex.setlocale(locale_code):
            pass

def test_setlocale_unsupported_inheritance():
    assert issubclass(ioex.UnsupportedLocaleSettingError, locale.Error)

@pytest.mark.parametrize(('dt', 'dt_format', 'locale_code', 'expected_string'), [
    [datetime.datetime(2016, 7, 23, 1, 7, 12), '%x', 'de_DE.utf8', '23.07.2016'],
    [datetime.datetime(2016, 7, 23, 1, 7, 12), '%X', 'de_DE.utf8', '01:07:12'],
    [datetime.datetime(2016, 7, 23, 1, 7, 12), '%x', 'en_US.utf8', '07/23/2016'],
    [datetime.datetime(2016, 7, 23, 1, 7, 12), '%X', 'en_US.utf8', '01:07:12 AM'],
    [datetime.datetime(2016, 7, 23, 1, 7, 12), '%x', 'it_IT.utf8', '23/07/2016'],
    [datetime.datetime(2016, 7, 23, 1, 7, 12), '%X', 'it_IT.utf8', '01:07:12'],
    [datetime.datetime(2016, 7, 23, 1, 7, 12), '%x', 'zh_CN.utf8', '2016年07月23日'],
    [datetime.datetime(2016, 7, 23, 1, 7, 12), '%X', 'zh_CN.utf8', '01时07分12秒'],
    ])
def test_setlocale_strtime(dt, dt_format, locale_code, expected_string):
    try:
        with ioex.setlocale(locale_code):
            assert dt.strftime(dt_format) == expected_string
    except ioex.UnsupportedLocaleSettingError as ex:
        pytest.skip('locale %s unsupported' % locale_code)
