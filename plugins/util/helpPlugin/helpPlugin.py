from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
import string
import logging
# The python file's name must be the same as the .chatter file's module attribute
class helpPlugin(IPlugin):
    def user_changed_nick(self, old_nick, new_nick):
        logging.warning(old_nick + " > " + new_nick)
    def plugin_loaded(self):
        # Generate list of plugins and their tasks
        taskDict = {}
        manager = PluginManagerSingleton.get()
        for plugin in manager.getAllPlugins():
            pName = manager.app.get_plugin_short_path(plugin.name)
            helpData = manager.app.plugin_get_setting(pName, "help")
            for _name, _el in helpData.iteritems():
                taskDict[_name] = _el
                logging.debug("Found task " + _name + " with " + str(len(_el)) + " children.")
        manager.app.plugin_set_setting("helpPlugin", "tasks", taskDict)

    def botmsg(self, user, channel, task, args):
        manager = PluginManagerSingleton.get()
        user = user.split("!")[0]
        if manager.app.plugin_get_setting("helpPlugin", "pmOnly") == "yes":
            channel = user
        if task == "help":
            logging.info(user + " requested " + task + " " + string.join(args[0:]))
            if not args:
                # Provide list of available plugins
                # TODO: Don't spam everyone
                _settings = manager.app.plugin_get_setting("helpPlugin", "tasks")
                _data = " | "
                for _task in _settings:
                    _data = _data + str(_task) + " | "
                manager.app.msg(channel, _data)
            else:
                _settings = manager.app.plugin_get_setting("helpPlugin", "tasks")
                for _opt, _val in _settings[args[0]].iteritems():
                    manager.app.msg(channel, str(_opt) + " - " + str(_val))
            
