# -*- coding: utf-8 -*-
from __future__ import print_function
from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
from gi.repository import Pango,Gtk
from core import general
import os
import json
import khayyam
import imp
from umalqurra import hijri_date

class DateEvents(IPlugin):
    persian_events = {}
    gregorian_events = {}
    hijri_events = {}

    def __init__(self):
        super(DateEvents, self).__init__()
        self.manager = PluginManagerSingleton.get()
        self.app = self.manager.app


    def activate(self):
        super(DateEvents, self).activate()
        self.path = os.path.join(general.PLUGIN_PATH, 'events')
        self.ui_config_path = os.path.join(self.path, 'config_dialog.ui')
        self.config_path = os.path.join(general.USER_CONFIG_PATH, 'events_plugin.ini')
        self.config_man = general.ConfigMan(self.config_path)


        #--- Load persian/jalali events
        try:
            self.jalali_events = imp.load_source("JALALI_EVENTS",os.path.join(self.path, 'jalaliEvents.py'))
            self.jalali_events = self.jalali_events.JALALI_EVENTS
        except:
            print("ERROR: CANNOT LOADING PERSIAN EVENTS")


        #--- Load gregorian events
        try:
            self.gregorian_events = imp.load_source("GREGORIAN_EVENTS",os.path.join(self.path, 'gregorianEvents.py'))
            self.gregorian_events = self.gregorian_events.GREGORIAN_EVENTS
        except:
            print("ERROR: CANNOT LOADING GREGORIAN EVENTS")


        #--- Load hijri events
        try:
            self.hijri_events = imp.load_source("HIJRI_EVENTS",os.path.join(self.path, 'hijriEvents.py'))
            self.hijri_events = self.hijri_events.HIJRI_EVENTS
        except:
            print("ERROR: CANNOT LOADING HIJRI EVENTS")

        self.app.on_refresh_date()
        self.builder = Gtk.Builder()


    def deactivate(self):
        super(DateEvents, self).deactivate()
        for i in range(1,43):
            obj = self.app.calendar.builder.get_object('bt'+str(i)+'lbl2')
            objbtn = self.app.calendar.builder.get_object('btn'+str(i))
            date = self.app.calendar.get_grid_date_by_pos(i-1)
            obj.set_text("")
            objbtn.set_tooltip_text("")
            objbtn.get_style_context().remove_class("day-has-event")
            self.gregorian_events = {}
            self.jalali_events = {}
            self.jalali_holidays = {}
            self.hijri_events = {}
            self.hijri_holidays = {}


    def set_on_calendar_grid(self):
        self.refresh_config()
        if self.is_activated:
            for i in range(1,43):
                objbtn = self.app.calendar.builder.get_object('btn'+str(i))
                obj = self.app.calendar.builder.get_object('bt'+str(i)+'lbl2')
                date = self.app.calendar.get_grid_date_by_pos(i-1)
                #--- Reset days info
                obj.set_text("")
                objbtn.set_tooltip_markup("")
                strEvent = ""
                objbtn.get_style_context().remove_class("day-has-event")


                if date != False:
                    GFIND = str(date.month).zfill(2)+"/"+str(date.day).zfill(2)

                    JDATE = khayyam.JalaliDate.from_date(date)
                    JFIND = str(JDATE.month).zfill(2)+"/"+str(JDATE.day).zfill(2)

                    HDATE = hijri_date.HijriDate(date.year, date.month, date.day, True)
                    HFIND = str(int(HDATE.month)).zfill(2)+"/"+str(int(HDATE.day)).zfill(2)


                    if JFIND.zfill(1) in self.jalali_events:
                        strEvent = self.jalali_events[JFIND][0]
                        objbtn.get_style_context().add_class("day-has-event")
                        if self.jalali_events[JFIND][1] == True:
                            objbtn.get_style_context().add_class("is-holiday")




                    if GFIND.zfill(1) in self.gregorian_events:
                        if strEvent != "": strEvent = strEvent+' - '
                        strEvent = strEvent+ self.gregorian_events[GFIND]
                        if objbtn.get_style_context().has_class("day-has-event") is False:
                            objbtn.get_style_context().add_class("day-has-event")


                    if HFIND.zfill(1) in self.hijri_events:
                        if strEvent != "": strEvent = strEvent + ' - '
                        strEvent = strEvent + self.hijri_events[HFIND][0] + "%s/%s/%s" % (int(HDATE.year),int(HDATE.month),int(HDATE.day))
                        if objbtn.get_style_context().has_class("day-has-event") is False:
                            objbtn.get_style_context().add_class("day-has-event")
                        if self.hijri_events[HFIND][1] == True:
                            objbtn.get_style_context().add_class("is-holiday")

                    if self.show_event_marker is False:
                        objbtn.get_style_context().remove_class("day-has-event")

                    obj.set_line_wrap(True)
                    obj.set_width_chars(5)
                    obj.set_lines(2)
                    obj.set_ellipsize(1)
                    obj.modify_font(Pango.FontDescription.from_string("tahoma 8px"))

                    if self.show_on_grid : obj.set_markup(strEvent)

                    strEvent = strEvent.replace('-', "\n")
                    strEvent = strEvent.replace(u'–', "\n")
                    objbtn.set_tooltip_markup(strEvent)


    def on_zoom_in(self):
        if self.is_activated:
            for i in range(1,43):
                obj = self.app.calendar.builder.get_object('bt'+str(i)+'lbl2')
                size = obj.get_style().font_desc.get_size()
                size = str((size/Pango.SCALE)+0.25)
                obj.modify_font(Pango.FontDescription.from_string(size))


    def on_zoom_out(self):
        if self.is_activated:
            for i in range(1,43):
                obj = self.app.calendar.builder.get_object('bt'+str(i)+'lbl2')
                size = obj.get_style().font_desc.get_size()
                size = str((size/Pango.SCALE)-0.25)
                obj.modify_font(Pango.FontDescription.from_string(size))


    def on_refresh_date(self):
        self.set_on_calendar_grid()


    def on_configure(self):
        if self.is_activated:
            self.builder.set_translation_domain(general.APP_NAME)
            self.builder.add_from_file(self.ui_config_path)
            self.builder.connect_signals(self)
            self.config_dialog = self.builder.get_object('config_dialog')
            self.builder.get_object('checkbutton_events_marker').props.active = self.show_event_marker
            self.builder.get_object('checkbutton_events_show').props.active = self.show_on_grid
            self.config_dialog.show_all()


    def on_btnclose_clicked(self, *args):
        self.config_dialog.close()


    def on_events_marker_toggled(self, obj):
        if obj.props.active:
            self.config_man.parser.set("general", "show_event_marker", "True")
        else:
            self.config_man.parser.set("general", "show_event_marker", "False")
        self.config_man.write_config()
        self.refresh_config()
        self.app.on_refresh_date()

    def on_events_show_toggled(self, obj):
        if obj.props.active:
            self.config_man.parser.set("general", "show_on_grid", "True")
        else:
            self.config_man.parser.set("general", "show_on_grid", "False")
        self.config_man.write_config()
        self.app.on_refresh_date()


    def refresh_config(self):
        try:
            self.show_on_grid = True if self.config_man.parser.get('general','show_on_grid')=="True" else False
        except:
            self.show_on_grid = True


        try:
            self.show_event_marker = True if self.config_man.parser.get('general','show_event_marker')=="True" else False
        except:
            self.show_event_marker = True