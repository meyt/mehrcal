


from gi.repository import Gtk, Gdk, Gio


class CalendarWidget(Gtk.Box):
    def __init__(self):
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.weekdays_box = Gtk.box()