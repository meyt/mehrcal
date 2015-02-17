# -*- coding: utf-8 -*-
import logging
import datetime
import BaseCalendar
import widgets
import general
import window
import settings
from yapsy.ConfigurablePluginManager import ConfigurablePluginManager
from yapsy.VersionedPluginManager import VersionedPluginManager
from yapsy.PluginManager import PluginManagerSingleton
from translate import _
from  gi.repository  import Gtk, Gio, Pango, Gdk



class App():
    PLUGIN_MAN = None
    CONFIG_MAN = None
    DATE_POINTER = [2015, 01, 01]

    def __init__(self):
        self.window = window.Window(self)
        self.settings = settings.Settings(self)
        self.about_dialog = widgets.AboutDialog(self)
        self.calendar = widgets.PersianCalendarWidget(self)
        self.calendar.load_weekday()
        self.calendar.load_widget()
        self.SECOND_DATE = 'jalali'
        self.tooltip = widgets.Tooltip()

        ### set config
        self.CONFIG_MAN = general.CONFIG_MAN
        if general.DEBUG:
            logging.debug("Reading configuration file: %s" % general.CONFIG_FILE)
        PluginManagerSingleton.setBehaviour([ConfigurablePluginManager,VersionedPluginManager])
        self.PLUGIN_MAN = PluginManagerSingleton.get()
        self.PLUGIN_MAN.app = self
        self.PLUGIN_MAN.setConfigParser(self.CONFIG_MAN, self.write_config)
        self.PLUGIN_MAN.setPluginInfoExtension("plugin")
        self.PLUGIN_MAN.setPluginPlaces([general.PLUGIN_PATH])
        self.PLUGIN_MAN.collectPlugins()

        ### Set today date to pinter
        tmp = datetime.date.today()
        self.DATE_POINTER = [tmp.year, tmp.month, tmp.day]



    def write_config(self):
        if general.DEBUG:
            logging.debug(_("Writing configuration file: %s") % general.CONFIG_FILE)
        f = open(general.CONFIG_FILE, "w")
        self.CONFIG_MAN.write(f)
        f.close()



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
        if general.DEBUG: print 'on_nav_prev'
        cdate = datetime.date(self.DATE_POINTER[0], self.DATE_POINTER[1], self.DATE_POINTER[2])
        jdate = BaseCalendar.PersianCalendar(cdate).subtract_one_month()
        gdate = jdate.todate()
        #print jdate.todate()
        self.DATE_POINTER = [gdate.year, gdate.month, gdate.day]
        self.on_refresh_date()


    def on_nav_next(self, event):
        if general.DEBUG: print 'on_nav_next'
        cdate = datetime.date(self.DATE_POINTER[0], self.DATE_POINTER[1], self.DATE_POINTER[2])
        jdate = BaseCalendar.PersianCalendar(cdate).add_one_month()
        gdate = jdate.todate()
        #print jdate.todate()
        self.DATE_POINTER = [gdate.year, gdate.month, gdate.day]
        self.on_refresh_date()


    def on_zoom_in(self, *args):
        if general.DEBUG: print "on_zoom_in"
        for plugin in self.PLUGIN_MAN.getAllPlugins():
            if(hasattr(plugin.plugin_object, 'on_zoom_in')):
                plugin.plugin_object.on_zoom_in()

        for i in range(1,43):
            obj = self.calendar.builder.get_object('bt'+str(i)+'lbl1')
            size = obj.get_style().font_desc.get_size()
            size = str((size/Pango.SCALE)+1)
            obj.modify_font(Pango.FontDescription.from_string(size))

            obj = self.calendar.builder.get_object('bt'+str(i)+'lbl3')
            size = obj.get_style().font_desc.get_size()
            size = str((size/Pango.SCALE)+1)
            obj.modify_font(Pango.FontDescription.from_string(size))


    def on_zoom_out(self, *args):
        if general.DEBUG: print 'on_zoom_out'

        for plugin in self.PLUGIN_MAN.getAllPlugins():
            if(hasattr(plugin.plugin_object, 'on_zoom_out')):
                plugin.plugin_object.on_zoom_out()

        for i in range(1, 43):
            obj = self.calendar.builder.get_object('bt'+str(i)+'lbl1')
            size = obj.get_style().font_desc.get_size()
            size = str((size/Pango.SCALE)-1)
            obj.modify_font(Pango.FontDescription.from_string(size))

            obj = self.calendar.builder.get_object('bt'+str(i)+'lbl3')
            size = obj.get_style().font_desc.get_size()
            size = str((size/Pango.SCALE)-1)
            obj.modify_font(Pango.FontDescription.from_string(size))
        self.window.resize(100, 100)


    def on_select_day(self, obj):
        if general.DEBUG: print 'on_select_day'
        btn_num = general.get_num_from_string(obj.get_name())
        date = self.calendar.get_grid_date_by_pos(btn_num-1)
        self.DATE_POINTER = [date.year, date.month, date.day]
        self.on_refresh_date()


    def on_mouse_enter_day(self, obj, *args):
        if general.DEBUG: print 'on_mouse_enter_day'
        #btn_num = general.get_num_from_string(obj.get_name())
        #date = self.calendar.get_grid_date_by_pos(btn_num-1)
        #self.tooltip.label.set_text(str(date))
        #self.tooltip.show()


    def on_mouse_leave_day(self, obj, *args):
        if general.DEBUG: print 'on_mouse_leave_day'
        #self.tooltip.close()


    def on_mouse_move(self, *args):
        window_pos = self.window.get_position()
        pointer_pos = self.window.get_pointer()
        tooltip_height = self.tooltip.get_allocated_height()
        pos = [
            window_pos[0]  + pointer_pos[0]  + 15 ,
            window_pos[1]  + pointer_pos[1]  + 15
        ]
        self.tooltip.move(pos[0], pos[1])


    def run(self):
        if general.DEBUG: print 'run()'
        self.window.MainPanned.pack1(self.calendar.widget, False, False)
        self.window.set_title(_('MehrCalendar'))
        self.on_refresh_date()
        self.window.show()
        self.on_refresh_date()