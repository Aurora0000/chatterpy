from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
import logging
# The python file's name must be the same as the .chatter file's module attribute
class authPlugin(IPlugin):
    def plugin_loaded(self):
        try:
            manager = PluginManagerSingleton.get()
            f = open("./plugins/util/authPlugin/passwd.data").read()
            service = str(manager.app.plugin_get_setting("authPlugin", "serviceName"))
            manager.app.msg(service, "identify {}".format(str(f)))
        except IOError:
            logging.warning("Password data file not found. Cannot authenticate!")
