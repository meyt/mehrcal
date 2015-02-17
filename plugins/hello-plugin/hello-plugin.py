from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton

class HelloPlugin(IPlugin):

    def __init__(self):
        super(HelloPlugin, self).__init__()
        #print 'Hello plugin :)'
        manager = PluginManagerSingleton.get()
        self.app = manager.app

        #self.app.window.gtkWindow.set_title('HELLO :)')



    def activate(self):
        # Make sure to call `activate()` on the parent class to ensure that the
        # `is_activated` property gets set.
        super(HelloPlugin, self).activate()
        
        # Connect to the "delete-event" and store the handler_id so that the
        # signal handler can be disconnected when the plugin is deactivated.
        # If your plugin connects to multiple signals on multiple objects then
        # you'll want to store the object and the handler_id of each of those.
        #print 'Hello plugin :)'


    
    def deactivate(self):
        # Make sure to call `deactivate()` on the parent class to ensure that 
        # the `is_activated` property gets set.
        super(HelloPlugin, self).deactivate()
        
        # Need to disconnect the signal handler when the plugin is deactivated.
        #print 'Bye plugin :('
    
