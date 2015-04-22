from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
import string
import logging
# The python file's name must be the same as the .chatter file's module attribute
class configEditor(IPlugin):
    def botmsg(self, user, channel, task, args):
        manager = PluginManagerSingleton.get()
        user = user.split("!")[0]
        if user not in manager.app.plugin_get_setting("quitPlugin", "allowedUsers") and (task == "quit" or task == "reboot"):
            manager.app.msg(channel, "You're not authorised to do that!")
            return
        
        if task == "quit":
            manager.quit = True
            manager.app.quit("Quitting (" + user + ")")
        elif task == "reboot":
            manager.app.quit("Rebooting (" + user + ")")
            
