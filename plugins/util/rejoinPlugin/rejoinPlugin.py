from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
# The python file's name must be the same as the .chatter file's module attribute
class rejoinPlugin(IPlugin):
    def kicked(self, user, channel, kicker, message):
        manager = PluginManagerSingleton.get()
        if user == manager.app.nickname:
            manager.app.join(channel)
            manager.app.msg(channel, kicker + ": Don't kick me!")

