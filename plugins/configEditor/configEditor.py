from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
import string
import logging
# The python file's name must be the same as the .chatter file's module attribute
class configEditor(IPlugin):
    def botmsg(self, user, channel, task, args):
        # Quit before doing anything if we haven't got any arguments
        if not args and task == "config":
            logging.debug("[configEditor] No arguments!")
            return
        
        manager = PluginManagerSingleton.get()
        if user.split("!")[0] not in manager.app.plugin_get_setting("configEditor", "allowedUsers") and task == "config":
            manager.app.msg(channel, "You're not authorised to do that!")
            return
        
        # Check if we must always send PMs
        if manager.app.plugin_get_setting("configEditor", "pmOnly") == "yes":
            channel = user
        
        if task == "config" and args[0] == "list":
            _msg = ""
            pName = manager.app.get_plugin_short_path(string.join(args[1:]))
            settings = manager.app.plugin_list_settings(pName)
            for opt in settings:
                _msg = _msg + " | " + str(opt)
            _msg = _msg + " |"
            manager.app.msg(channel, "There are " + str(len(settings)) + " settings:")
            manager.app.msg(channel, _msg)
        elif task == "config" and args[0] == "get":
            pName = manager.app.get_plugin_short_path(string.join(args[2:]))
            v = manager.app.plugin_get_setting(pName, args[1])
            manager.app.msg(channel, args[1] + ": \"" + str(v) + "\"")
        elif task == "config" and args[0] == "getName":
            pName = manager.app.get_plugin_short_path(string.join(args[1:]))
            manager.app.msg(channel, "\"" + pName + "\"")
        elif task == "config" and args[0] == "set":
            pName = args[2]
            v = manager.app.plugin_set_setting(pName, args[1], string.join(args[3:]))
            manager.app.msg(channel, "Value set successfully.")           
