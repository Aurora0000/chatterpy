from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
import string
import itertools
# The python file's name must be the same as the .chatter file's module attribute
class pluginAdmin(IPlugin):
    def botmsg(self, user, channel, task, args):
        manager = PluginManagerSingleton.get()
        if user.split("!")[0] not in manager.app.plugin_get_setting("pluginAdmin", "allowedUsers") and task == "plugin" :
            manager.app.msg(channel, "You're not authorised to do that!")
            return
        if task == "plugin":
            if args[0] == "rehash":
                manager.app.rehash_plugins()
                manager.app.msg(channel, "Plugins rehashed!")
            elif args[0] == "load":
                manager = PluginManagerSingleton.get()
                pname = string.join(args[1:])
                if pname in manager.app.plugin_get_setting("pluginAdmin", "disallowedPlugins"):
                    manager.app.msg(channel, "Plugin \"" + pname + "\" is protected!")      
                    return
                manager.app.load_plugin(pname)
                manager.app.msg(channel, "Plugin \"" + string.join(args[1:]) + "\" has been loaded.")
            elif args[0] == "list":
                manager = PluginManagerSingleton.get()
                plugins_list = manager.getAllPlugins()
                plugins_names = itertools.imap(lambda plugin: plugin.name, plugins_list)
                manager.app.msg(channel, ' | '.join(plugins_names))
            elif args[0] == "unload":
                manager = PluginManagerSingleton.get()
                pname = string.join(args[1:])
                if pname in manager.app.plugin_get_setting("pluginAdmin", "disallowedPlugins"):
                    manager.app.msg(channel, "Plugin \"" + pname + "\" is protected!")      
                    return
                manager.app.unload_plugin(string.join(args[1:]))
                manager.app.msg(channel, "Plugin \"" + string.join(args[1:]) + "\" has been unloaded.")