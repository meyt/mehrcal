# -*- coding: utf-8 -*-
from __future__ import print_function
import core.general as general
import locale

lang = locale.getdefaultlocale()
path = general.LOCALE_PATH

def _(text):

    try:
        locale.bindtextdomain(general.APP_NAME, path)
        locale.textdomain(general.APP_NAME)
        locale.setlocale(locale.LC_ALL, lang)
        return locale.dgettext(general.APP_NAME, text)
    except:
        print("locale cannot setting")

    return text



