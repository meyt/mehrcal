# -*- coding: utf-8 -*-
from __future__ import print_function
import core.general as general
import locale


try:
    lang = general.CONFIG_MAN.get('general', 'language')
except:
    lang = locale.getdefaultlocale()


def _(text):
    try: 
        locale.bindtextdomain(general.APP_NAME, general.LOCALE_PATH)
        locale.textdomain(general.APP_NAME)
        locale.setlocale(locale.LC_ALL, lang)
        return locale.dgettext(general.APP_NAME, text)
    except:
        print("locale cannot setting")

    return text

