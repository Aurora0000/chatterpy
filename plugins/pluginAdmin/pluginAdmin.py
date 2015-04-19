from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
# The python file's name must be the same as the .chatter file's module attribute
class examplePlugin(IPlugin):
    def botmsg(self, user, channel, task, args):
        if task == "plugin":
            if args[0] == "rehash":
                manager = PluginManagerSingleton.get()
                manager.app.rehash_plugins()
                manager.app.msg(channel, "Plugins rehashed!")
            elif args[0] == "load":
                manager = PluginManagerSingleton.get()
                manager.app.load_plugin(string.join(args[1:]))
                manager.app.msg(channel, "Plugin" + string.join(args[1:]) + " has been loaded.")
            elif args[0] == "unload":
                manager = PluginManagerSingleton.get()
                manager.app.unload_plugin(string.join(args[1:]))
                manager.app.msg(channel, "Plugin" + string.join(args[1:]) + " has been unloaded.")
