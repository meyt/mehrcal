from gi.repository import Gtk, GLib, Gio
import core.general as general
from core.translate import _


class Settings:
    exists = False

    def __init__(self, app):
        self.app = app
        self.builder = Gtk.Builder()
        self.builder.set_translation_domain(general.APP_NAME)




    def show(self):
        if self.exists==False:
            self.builder.add_from_file(general.UI_SETTINGS_PATH)
            self.builder.connect_signals(self)
            self.settings_window = self.builder.get_object('settings_window')
            self.settings_window.show_all()
            self.settings_window.set_title(_('Settings'))
            self.plugin_store =  self.builder.get_object('liststore_plugins')
            self.load_plugin_tree_view()
            self.exists = True



    def close(self, *args):
        self.settings_window.destroy()
        self.exists = False




    def load_plugin_tree_view(self):
        self.plugin_store.clear()
        for info in self.app.PLUGIN_MAN.getAllPlugins():
            plugin = info.plugin_object
            self.plugin_store.append((info.name,  str(info.version), plugin.is_activated, info))



    def on_plugin_info(self, treeviewobj):
        treeselect = treeviewobj.get_selection() ## return TreeSelection
        store = treeselect.get_selected_rows() ## return ListStore
        pos = store[1][0] ## get selected row position
        iter = self.plugin_store.get_iter(pos)

        ### get plugin information's
        plugin_name = self.plugin_store[iter][3].name
        plugin_author = self.plugin_store[iter][3].author
        plugin_version = self.plugin_store[iter][3].version
        plugin_website = self.plugin_store[iter][3].website
        plugin_description = self.plugin_store[iter][3].description
        message = _("%s %s \n author: %s \n %s \n %s") % (plugin_name,plugin_version,plugin_author,plugin_description,plugin_website)

        dialog = Gtk.MessageDialog(self.app.window, Gtk.DialogFlags.MODAL |
                                           Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                           Gtk.MessageType.INFO,
                                           Gtk.ButtonsType.CLOSE,
                                           message)
        dialog.set_title(_("about plugin %s") % plugin_name)
        dialog.run()
        dialog.destroy()


    def on_plugin_config(self, treeviewobj):
        treeselect = treeviewobj.get_selection() ## return TreeSelection
        store = treeselect.get_selected_rows() ## return ListStore
        pos = store[1][0] ## get selected row position
        iter = self.plugin_store.get_iter(pos)
        plugin_name = self.plugin_store[iter][3].name
        plugin = self.app.PLUGIN_MAN.getPluginByName(plugin_name)
        if(hasattr(plugin.plugin_object,'on_configure')):
                plugin.plugin_object.on_configure()



    def on_toggle_plugin(self, cell, path, data=None):
        ### Toggle the activation checkbox
        iter = self.plugin_store.get_iter(path)
        self.plugin_store[iter][2] = not self.plugin_store[iter][2]
        ### Activate or deactivate the plugin
        if self.plugin_store[iter][2]:
            self.app.PLUGIN_MAN.activatePluginByName(self.plugin_store[iter][3].name)
        else:
            self.app.PLUGIN_MAN.deactivatePluginByName(self.plugin_store[iter][3].name)

