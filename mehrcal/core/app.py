# -*- coding: utf-8 -*-
##
# Application main
##
from __future__ import print_function
from yapsy.ConfigurablePluginManager import ConfigurablePluginManager
from yapsy.VersionedPluginManager import VersionedPluginManager
from yapsy.PluginManager import PluginManagerSingleton
from core.translate import _
import core.translate
from gi.repository  import Gtk, Gio, Pango, Gdk
import logging
import datetime
import core.BaseCalendar as BaseCalendar
import core.widgets as widgets
import core.general as general
import core.window as window
import core.settings as settings



class App():
    PLUGIN_MAN = None
    CONFIG_MAN = None
    DATE_POINTER = [2015, 1, 1]

    def __init__(self):
        self.CONFIG_MAN = general.ConfigMan(general.CONFIG_FILE)
        if self.CONFIG_MAN.parser.has_section('general') and self.CONFIG_MAN.parser.has_option('general', 'language'):
            core.translate.lang = self.CONFIG_MAN.parser.get("general", "language")

        self.window = window.Window(self)
        self.settings = settings.Settings(self)
        self.about_dialog = widgets.AboutDialog(self)

        self.refresh_calendar_config()
        self.load_calendar()

        self.SECOND_DATE = 'jalali'
        self.sidebar = widgets.sidebar(self)




        try:
            self.on_refresh_holiday_color(self.CONFIG_MAN.parser.get("general", "holiday-color"))
        except:
            self.on_refresh_holiday_color('green')

        ### set config
        if general.DEBUG:
            logging.debug(_("Reading configuration file: %s" % general.CONFIG_FILE))
        PluginManagerSingleton.setBehaviour([ConfigurablePluginManager,VersionedPluginManager])
        self.PLUGIN_MAN = PluginManagerSingleton.get()
        self.PLUGIN_MAN.app = self
        self.PLUGIN_MAN.setConfigParser(self.CONFIG_MAN.parser, self.CONFIG_MAN.write_config)
        self.PLUGIN_MAN.setPluginInfoExtension("plugin")
        self.PLUGIN_MAN.setPluginPlaces([general.PLUGIN_PATH])
        self.PLUGIN_MAN.collectPlugins()

        ### Set today date to pinter
        tmp = datetime.date.today()
        self.DATE_POINTER = [tmp.year, tmp.month, tmp.day]



    def on_refresh_date(self):
        self.calendar.load_weekday()
        self.calendar.load_widget()


        for plugin in self.PLUGIN_MAN.getAllPlugins():
            if(hasattr(plugin.plugin_object, 'on_refresh_date')):
                plugin.plugin_object.on_refresh_date()

        #--- Set HeaderBar title
        JDATE = BaseCalendar.khayyam.JalaliDate.from_date(datetime.date(self.DATE_POINTER[0], self.DATE_POINTER[1], self.DATE_POINTER[2]))
        month_name = BaseCalendar.khayyam.PERSIAN_MONTH_NAMES[int(JDATE.month)]
        self.window.HeaderBar.props.title = str(JDATE.year) + " " + month_name


    def on_exit(self, *args):
        for plugin in self.PLUGIN_MAN.getAllPlugins():
            if(hasattr(plugin.plugin_object, 'on_exit')):
                plugin.plugin_object.onExit()
        exit()


    def on_response_about(self, *args):
        self.about_dialog.close()


    def on_show_about(self, *args):
        self.about_dialog.show()


    def on_show_settings(self, *args):
        self.settings.show()


    def on_nav_prev(self, *args):
        if general.DEBUG: print('on_nav_prev')
        cdate = datetime.date(self.DATE_POINTER[0], self.DATE_POINTER[1], self.DATE_POINTER[2])
        jdate = BaseCalendar.PersianCalendar(cdate).subtract_one_month()
        gdate = jdate.todate()
        self.DATE_POINTER = [gdate.year, gdate.month, gdate.day]
        self.on_refresh_date()


    def on_nav_next(self, event):
        if general.DEBUG: print('on_nav_next')
        cdate = datetime.date(self.DATE_POINTER[0], self.DATE_POINTER[1], self.DATE_POINTER[2])
        jdate = BaseCalendar.PersianCalendar(cdate).add_one_month()
        gdate = jdate.todate()
        self.DATE_POINTER = [gdate.year, gdate.month, gdate.day]
        self.on_refresh_date()


    def on_zoom_in(self, *args):
        if general.DEBUG: print("on_zoom_in")
        for plugin in self.PLUGIN_MAN.getAllPlugins():
            if(hasattr(plugin.plugin_object, 'on_zoom_in')):
                plugin.plugin_object.on_zoom_in()

        for i in range(1,43):
            obj = self.calendar.builder.get_object('bt'+str(i)+'lbl1')
            size = obj.get_style().font_desc.get_size()
            size = str((size/Pango.SCALE)+2)
            obj.modify_font(Pango.FontDescription.from_string(size))

            obj = self.calendar.builder.get_object('bt'+str(i)+'lbl3')
            size = obj.get_style().font_desc.get_size()
            size = str((size/Pango.SCALE)+1)
            obj.modify_font(Pango.FontDescription.from_string(size))


    def on_zoom_out(self, *args):
        if general.DEBUG: print('on_zoom_out')

        for plugin in self.PLUGIN_MAN.getAllPlugins():
            if(hasattr(plugin.plugin_object, 'on_zoom_out')):
                plugin.plugin_object.on_zoom_out()

        for i in range(1, 43):
            obj = self.calendar.builder.get_object('bt'+str(i)+'lbl1')
            size = obj.get_style().font_desc.get_size()
            size = str((size/Pango.SCALE)-2)
            obj.modify_font(Pango.FontDescription.from_string(size))

            obj = self.calendar.builder.get_object('bt'+str(i)+'lbl3')
            size = obj.get_style().font_desc.get_size()
            size = str((size/Pango.SCALE)-1)
            obj.modify_font(Pango.FontDescription.from_string(size))
        self.window.resize(100, 100)


    def on_select_day(self, obj):
        if general.DEBUG: print('on_select_day')
        btn_num = general.get_num_from_string(obj.get_name())
        date = self.calendar.get_grid_date_by_pos(btn_num-1)
        self.DATE_POINTER = [date.year, date.month, date.day]
        self.on_refresh_date()


    def on_mouse_enter_day(self, obj, *args):
        if general.DEBUG_ACT: print('on_mouse_enter_day')
        #btn_num = general.get_num_from_string(obj.get_name())
        #date = self.calendar.get_grid_date_by_pos(btn_num-1)


    def on_mouse_leave_day(self, obj, *args):
        if general.DEBUG_ACT: print('on_mouse_leave_day')


    def on_mouse_move(self, *args):
        window_pos = self.window.get_position()
        pointer_pos = self.window.get_pointer()
        pos = [
            window_pos[0]  + pointer_pos[0]  + 15 ,
            window_pos[1]  + pointer_pos[1]  + 15
        ]


    def on_toggle_sidebar(self, obj):
        if obj.props.active:
            self.on_show_sidebar()
        else:
            self.on_hide_sidebar()
        self.on_refresh_date()


    def on_show_sidebar(self):
        self.window.MainPanned.remove(widgets.empty_widget)
        self.window.MainPanned.pack2(self.sidebar.widget, True, False)
        self.window.refresh()


    def on_hide_sidebar(self):
        self.window.MainPanned.remove(self.sidebar.widget)
        self.window.refresh()


    def refresh_calendar_config(self):
        #--- Get weekday position config
        try:
            self.calendar_wpos = self.CONFIG_MAN.parser.get("general", "weekday_position")
        except:
            self.calendar_wpos = "top"

        #--- Get weekday horizontal layout config
        try:
            self.calendar_horizontal_layout = self.CONFIG_MAN.parser.get("general", "weekday_horizontal_layout")
        except:
            self.calendar_horizontal_layout = "rtl"


    def load_calendar(self, mode=None, horizontal_layout=None ):
        if hasattr(self, 'calendar'):
            self.window.MainPanned.remove(self.calendar.widget)

        self.refresh_calendar_config()

        if mode==None:
            mode = self.calendar_wpos

        if horizontal_layout==None:
            horizontal_layout= self.calendar_horizontal_layout

        self.calendar = widgets.PersianCalendarWidget(self, mode, horizontal_layout)
        self.window.MainPanned.pack1(self.calendar.widget, False, False)
        self.window.refresh()
        self.calendar.load_weekday()
        self.calendar.load_widget()


    def on_refresh_holiday_color(self, color_hex):
        if color_hex != "":
            color_hex = """GtkWindow #MainBox .is-holiday .day-lbl-main{color: %s;}""" % str(color_hex)
            self.window.refresh_css(data=color_hex.encode())


    def on_window_show(self, *args):
        if self.window.get_property("visible"):
            if general.DEBUG: print('on_window_show')
            self.on_refresh_date()



    def run(self):
        if general.DEBUG: print('run()')

        self.window.set_title(_('MehrCalendar'))
        self.window.show()




