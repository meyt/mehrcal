import general
from ConfigParser import SafeConfigParser
import locale

try:
    lang = general.CONFIG_MAN.get('general', 'language')
except:
    lang = locale.getdefaultlocale()


def _(text):
    locale.bindtextdomain(general.APP_NAME, general.LOCALE_PATH)
    locale.textdomain(general.APP_NAME)
    locale.setlocale(locale.LC_ALL, lang)
    return locale.dgettext(general.APP_NAME, text)

