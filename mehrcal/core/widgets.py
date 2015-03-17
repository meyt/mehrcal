##
# All widget's
##
from __future__ import print_function
from  gi.repository  import Gtk,Gio,Pango,Gdk,GdkPixbuf

import core.general as general
import core.BaseCalendar as BaseCalendar
import datetime


class PersianCalendarWidget:
    date_pos = []
    default_lbl1_font_size = "12"
    default_lbl2_font_size = "6"
    default_lbl3_font_size = "8"

    def __init__(self, app, wpos="left", calendar_horizontal_layout="rtl"):
        self.app = app
        self.builder = Gtk.Builder()
        self.builder.set_translation_domain(general.APP_NAME)
        self.RTL= False

        if calendar_horizontal_layout == "rtl":
            self.RTL= True

        if wpos == "top":
            self.mode = "horizontal"
            self.builder.add_from_file(general.UI_CALENDAR_TOP_PATH)


        elif wpos == "left":
            self.mode = "vertical"
            self.builder.add_from_file(general.UI_CALENDAR_LEFT_PATH)


        elif wpos == "right":
            self.mode = "vertical"
            self.builder.add_from_file(general.UI_CALENDAR_RIGHT_PATH)

        else:
            print("ERROR: INVALID WEEKDAY POSITION")

        self.builder.connect_signals(self.app)

        self.widget = self.builder.get_object("CalendarWidget")
        ### Remove supper labels
        for i in range(1, 43):
            obj1 = self.builder.get_object('bt'+str(i)+'lbl1')
            obj1.modify_font(Pango.FontDescription.from_string(self.default_lbl1_font_size))

            obj2 = self.builder.get_object('bt'+str(i)+'lbl2')
            obj2.modify_font(Pango.FontDescription.from_string(self.default_lbl2_font_size))

            obj3 = self.builder.get_object('bt'+str(i)+'lbl3')
            obj3.modify_font(Pango.FontDescription.from_string(self.default_lbl3_font_size))

            obj2.set_text('')
            obj2.set_name('bt'+str(i))

        if self.mode=='vertical': ## force RTL off when vertical mode
            self.RTL = False


    def load_weekday(self, abbr=False):
        pCal = BaseCalendar.PersianCalendar().get_week_days()
        for i in range(1,8):
            obj = self.builder.get_object('WeekDay'+str(i))
            num = i-1
            if self.RTL:
                num = 6-num
            if abbr:
                obj.set_text(pCal[num][0])
            else:
                obj.set_text(pCal[num][1])


    def load_widget(self):
        pCal = BaseCalendar.PersianCalendar(datetime.date(self.app.DATE_POINTER[0],self.app.DATE_POINTER[1],self.app.DATE_POINTER[2]))
        pCal.gen_grid_mat(self.RTL)

        self.date_pos = []
        counter = 1
        for j, row in enumerate(pCal.grid_mat):
            for i, (date, day) in enumerate(row):

                obj1 = self.builder.get_object('bt'+str(counter)+'lbl1')
                obj = self.builder.get_object('btn'+str(counter))
                obj.show()


                obj1.get_style_context().remove_class("day-lbl-main")
                obj.get_style_context().remove_class("day-this-month")
                obj.get_style_context().remove_class("day-month")
                obj.get_style_context().remove_class("day-highlight")
                obj.get_style_context().remove_class("is-holiday")


                obj1.get_style_context().add_class("day-lbl-main")
                if(i==0 and self.mode=='horizontal'):
                    obj.get_style_context().add_class("is-holiday")

                elif(i==6 and self.mode=='vertical'):
                    obj.get_style_context().add_class("is-holiday")

                if date.month == pCal.date.month:
                    obj.get_style_context().add_class("day-this-month")

                    if date.day == pCal.date.day:
                        obj.get_style_context().add_class("day-highlight")

                    else:
                        obj.get_style_context().remove_class("day-highlight")

                else:
                    obj.get_style_context().add_class("day-month")


                obj1.set_text(day)

                ### Highlight selected day
                text = obj1.get_text()

                ### Convert to gregorian date
                GDATE = BaseCalendar.khayyam.JalaliDate(date.year, date.month, date.day)
                GDATE = GDATE.todate()
                obj1 = self.builder.get_object('bt'+str(counter)+'lbl3')
                obj1.set_text(str(GDATE.day))

                self.date_pos.append(GDATE.strftime("%s"))
                counter += 1

        ### Remove empty row

        if counter <= 36:
            for i in range(counter,43):
                obj = self.builder.get_object('btn'+str(i))
                obj.hide()



    def get_grid_pos_by_date(self, year, month, day):
        time = datetime.date(year,month,day).strftime("%s")
        if time in self.date_pos:
            return self.date_pos.index(time)
        else:
            return False

    def get_grid_date_by_pos(self, pos):
        if pos < len(self.date_pos):
            return datetime.date.fromtimestamp(float(self.date_pos[pos]))
        else:
            return False












class AboutDialog():
    def __init__(self, app):
        self.app = app


    def show(self, *args):
        self.builder = Gtk.Builder()
        self.builder.set_translation_domain(general.APP_NAME)
        self.builder.add_from_file(general.UI_ABOUT_PATH)
        self.builder.connect_signals(self.app)
        self.widget = self.builder.get_object("AboutDialog")
        self.builder.connect_signals(self)
        self.widget.set_logo(GdkPixbuf.Pixbuf.new_from_file_at_size(general.APP_ICON, 150, 150))
        self.widget.show_all()


    def close(self, *args):
        self.widget.destroy()










class sidebar:
    def __init__(self, app):
        self.app = app
        self.widget = Gtk.ScrolledWindow()
        self.viewport = Gtk.Viewport()
        self.main_vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.viewport.add(self.main_vbox)
        self.empty_widget = Gtk.Box()
        self.widget.add(self.viewport)






empty_widget = Gtk.Box()