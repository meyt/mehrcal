###
# General definition
##
from __future__ import print_function
import os

try:
  import configparser
except ImportError:
  import ConfigParser
  configparser = ConfigParser
  

DEBUG = False
DEBUG_ACT = False


HOME_DIR = os.path.expanduser("~")
USER_CONFIG_PATH = os.path.join(HOME_DIR, '.config')
USER_CONFIG_PATH = os.path.join(USER_CONFIG_PATH, 'mehrcal')

APP_NAME = 'mehrcal'
APP_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
APP_ICON = os.path.join(APP_PATH, 'data/mehrcal.svg')
APP_STYLE = os.path.join(APP_PATH, 'data/style.css')


LOCALE_PATH = os.path.join(APP_PATH, 'locale')
PLUGIN_PATH = os.path.join(APP_PATH, 'plugins')
CONFIG_FILE = os.path.join(USER_CONFIG_PATH, 'app.conf')


UI_CALENDAR_TOP_PATH = os.path.join(APP_PATH, 'data/calendar-widget-wtop.ui')
UI_CALENDAR_LEFT_PATH = os.path.join(APP_PATH, 'data/calendar-widget-wleft.ui')
UI_CALENDAR_RIGHT_PATH = os.path.join(APP_PATH, 'data/calendar-widget-wright.ui')

UI_ABOUT_PATH = os.path.join(APP_PATH, 'data/about.ui')
UI_SETTINGS_PATH = os.path.join(APP_PATH, 'data/settings.ui')

#--- Create config directory if not exists
try:
    os.makedirs(USER_CONFIG_PATH)
except:
    pass



#--- Return all number's exists on string
def get_num_from_string(r):
    return int(''.join(x for x in r if x.isdigit()))



class ConfigMan:
    def __init__(self, config_path):
        self.config_path = config_path
        #--- Create sample config file if not exits
        if os.path.isfile(self.config_path) is False:
            open(self.config_path, 'a').close()

        #--- Try to load parser / py2|3
        try:
            self.parser = configparser.ConfigParser(allow_no_value=True)
        except:
            self.parser = configparser.SafeConfigParser(allow_no_value=True)

        #--- Read file from parser
        self.parser.read(self.config_path)

        if self.parser.has_section("general") is False:
            self.parser.add_section("general")

    def write_config(self):
        f = open(self.config_path, "w")
        self.parser.write(f)
        f.close()




