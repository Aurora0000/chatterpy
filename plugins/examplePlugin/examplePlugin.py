from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
# The python file's name must be the same as the .chatter file's module attribute
class examplePlugin(IPlugin):
    def privmsg(self, user, channel, msg):
        # The singleton allows us to access the bot's methods (such as msg)
        # via the manager.app class.
        manager = PluginManagerSingleton.get()

        # For the purposes of this example, we'll just say ping to any message.
        manager.app.msg(channel, "Ping.")
        
