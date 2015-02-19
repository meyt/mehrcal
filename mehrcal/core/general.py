###
# General definition
##
import configparser

import os

DEBUG = True

APP_NAME = 'mehrcal'
APP_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
APP_ICON = os.path.join(APP_PATH, 'data/mehrcal.svg')
APP_STYLE = os.path.join(APP_PATH, 'data/style.css')

LOCALE_PATH = os.path.join(APP_PATH, 'locale')
PLUGIN_PATH = os.path.join(APP_PATH, 'plugins')
CONFIG_FILE = os.path.join(APP_PATH, 'app.conf')

UI_CALENDAR_PATH = os.path.join(APP_PATH, 'data/calendar-widget.ui')
UI_ABOUT_PATH = os.path.join(APP_PATH, 'data/about.ui')
UI_SETTINGS_PATH = os.path.join(APP_PATH, 'data/settings.ui')

RTL = False
CONFIG_MAN =  configparser.ConfigParser()
try:
    CONFIG_MAN = configparser.ConfigParser()
except:
    CONFIG_MAN = configparser.SafeConfigParser()


CONFIG_MAN.read(CONFIG_FILE)





#--- Return all number's exists on string
def get_num_from_string(r):
    return int(''.join(x for x in r if x.isdigit()))