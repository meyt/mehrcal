'''
    Prepare window element's
'''
from gi.repository import Gtk, GLib, Gio, Gdk
import general


from translate import _



class Window(Gtk.Window):

    def __init__(self, app):
        self.app = app
        Gtk.Window.__init__(self)
        self.set_border_width(5)
        self.set_default_size(350, 200)
        self.set_size_request(350, 200)
        self.set_type_hint(Gdk.WindowTypeHint.NORMAL)
        self.set_icon_from_file(general.APP_ICON)


        #--- Set headerbar gtk+ 3.x
        self.HeaderBar = Gtk.HeaderBar()
        self.HeaderBar.set_show_close_button(True)
        self.set_titlebar(self.HeaderBar)


        #--- Set settings button
        button = Gtk.MenuButton()
        icon = Gio.ThemedIcon(name="document-properties")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        #button.connect("clicked", self.app.on_show_settings)

        #--- Create main menu


        mitem1 = Gtk.MenuItem(_("Zoom in"))
        mitem1.connect("button-release-event", self.app.on_zoom_in)

        mitem2 = Gtk.MenuItem(_("Zoom out"))
        mitem2.connect("button-release-event", self.app.on_zoom_out)

        mitem3 = Gtk.MenuItem(_("Settings"))
        mitem3.connect("button-release-event", self.app.on_show_settings)

        mitem4 = Gtk.MenuItem(_("About"))
        mitem4.connect("button-release-event", self.app.on_show_about)

        menu = Gtk.Menu()
        menu.append(mitem1)
        menu.append(mitem2)
        menu.append(mitem3)
        menu.append(mitem4)
        menu.show_all()
        button.set_popup(menu)


        self.HeaderBar.pack_end(button)





        #--- Set date navigation buttons
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        box.add(button)
        button.connect("clicked", self.app.on_nav_prev)


        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        box.add(button)
        button.connect("clicked", self.app.on_nav_next)


        #--- Packing HeaderBar navigation
        self.HeaderBar.pack_start(box)

        #--- Window content layout
        self.MainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.MainBox.set_name('MainBox')
        self.add(self.MainBox)

        self.SecondBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.MainBox.pack_start(self.SecondBox, True, True, 0)
        self.MainPanned = Gtk.Paned()
        self.SecondBox.pack_end(self.MainPanned, True, True, 0)

        screen = Gdk.Screen.get_default()
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(general.APP_STYLE)

        context = Gtk.StyleContext()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)





    def show(self):
        self.connect("delete-event", self.close)
        self.connect("key-press-event", self.bind_keys)
        self.connect("motion-notify-event", self.app.on_mouse_move)
        self.SecondBox.connect('motion-notify-event',self.app.on_exit)
        self.show_all()
        #self.get_window().set_decorations(Gdk.WMDecoration.BORDER)
        #self.get_window().set_decorations(1)


        #myStatusIcon = Gtk.StatusIcon()
        #myStatusIcon.set_from_file(general.APP_ICON)
        #myStatusIcon.set_visible(True)


        Gtk.main()





    def close(self, *args):
        Gtk.main_quit()
        self.app.on_exit()


    def bind_keys(self, widget, event):

        #--- ControlKey bind
        if Gdk.ModifierType.CONTROL_MASK & event.state:
            if general.DEBUG: print "Control mask"


        #--- PlusKey
        if event.keyval == Gdk.KEY_plus or event.keyval==Gdk.KEY_KP_Add :
            self.app.on_zoom_in()

        #--- MinusKey
        if event.keyval == Gdk.KEY_minus or event.keyval==Gdk.KEY_KP_Subtract :
            self.app.on_zoom_out()


        #--- Debug::
        if general.DEBUG: print "KeyPressed: "+str(event.keyval)

