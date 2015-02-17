
from  gi.repository  import Gtk,Gio,Pango,Gdk,GdkPixbuf
import general
from translate import _
import BaseCalendar
import datetime

class PersianCalendarWidget:
    date_pos = []

    def __init__(self, app):
        self.app = app
        self.builder = Gtk.Builder()
        self.builder.set_translation_domain(general.APP_NAME)
        self.builder.add_from_file(general.UI_CALENDAR_PATH)
        self.builder.connect_signals(self.app)
        self.widget = self.builder.get_object("CalendarWidget")
        ### Remove supper labels
        for i in range(1, 43):
            obj = self.builder.get_object('bt'+str(i)+'lbl2')
            obj.set_text('')
            obj.set_name('bt'+str(i))


    def load_weekday(self):
        pCal = BaseCalendar.PersianCalendar().get_week_days()
        for i in range(1,8):
            obj = self.builder.get_object('WeekDay'+str(i))
            obj.set_text(pCal[i-1][0])



    def load_widget(self):
        pCal = BaseCalendar.PersianCalendar(datetime.date(self.app.DATE_POINTER[0],self.app.DATE_POINTER[1],self.app.DATE_POINTER[2]))
        pCal.gen_grid_mat()
        self.date_pos = []
        counter = 1
        for j, row in enumerate(pCal.grid_mat):
            for i, (date, day) in enumerate(row):

                obj1 = self.builder.get_object('bt'+str(counter)+'lbl1')
                obj2 = self.builder.get_object('btn'+str(counter))

                obj2.get_style_context().remove_class("day-this-month")
                obj2.get_style_context().remove_class("day-month")
                obj2.get_style_context().remove_class("day-highlight")

                if date.month == pCal.date.month:
                    obj2.get_style_context().add_class("day-this-month")

                    if date.day == pCal.date.day:
                        obj2.get_style_context().add_class("day-highlight")

                    else:
                        obj2.get_style_context().remove_class("day-highlight")

                else:
                    obj2.get_style_context().add_class("day-month")




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
        if counter<=36:
            for i in range(counter,43):
                obj = self.builder.get_object('btn'+str(i)+'')
                obj.destroy()
            obj = self.builder.get_object('DaysGrid').remove_row(6)


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




class Tooltip(Gtk.Window):
    is_show = False

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_border_width(1)
        self.set_default_size(10, 10)
        self.set_size_request(10, 10)
        self.set_type_hint(Gdk.WindowTypeHint.SPLASHSCREEN)

        self.label = Gtk.Label()
        self.add(self.label)

    def show(self):
        if self.is_show == False:
            self.connect("delete-event", self.close)
            self.show_all()
            #self.get_window().set_decorations(Gdk.WMDecoration.MENU)

            self.is_show = True

    def close(self):
        self.is_show = False
        self.hide()





