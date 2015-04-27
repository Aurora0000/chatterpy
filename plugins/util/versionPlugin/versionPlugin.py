from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
# The python file's name must be the same as the .chatter file's module attribute
class versionPlugin(IPlugin):
    def botmsg(self, user, channel, task, args):
        if task == "version":
            manager = PluginManagerSingleton.get()
            if channel == manager.app.nickname:
                channel = user
            maj = str(manager.app.versionMajor)
            _min = str(manager.app.versionMinor)
            patch = str(manager.app.versionPatch)
            manager.app.msg(channel, "This bot is using ChatterPy v" + maj + "." + _min + "." + patch)
        
