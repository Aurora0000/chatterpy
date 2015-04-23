from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
import string
import logging
# The python file's name must be the same as the .chatter file's module attribute
class notePlugin(IPlugin):
    
    def plugin_loaded(self):
        # Ensure notes setting is always available
        manager = PluginManagerSingleton.get()
        if not "notes" in manager.app.plugin_list_settings("notePlugin"):
            manager.app.plugin_set_setting("notePlugin", "notes", {})
            logging.debug("Created note database")
        else:
            logging.debug("Note database found.")

    def botmsg(self, user, channel, task, args):
        user = user.split("!")[0]
        if task == "note" and args[0] == "send":
            manager = PluginManagerSingleton.get()
            self.add_note(args[1], "\"" + string.join(args[2:]) + "\" (from " + user + ")")
            manager.app.msg(args[1], "You have a new note! Use !note read to read it.")
            manager.app.msg(user, "Your message has been sent.")
        elif task == "note" and args[0] == "read":
            manager = PluginManagerSingleton.get()     
            _notes = manager.app.plugin_get_setting("notePlugin", "notes")
            x = None
            try:
                x = _notes[user]
                if len(x) == 0:
                    raise KeyError("x")
            except KeyError:
                manager.app.msg(user, "You don't have any messages.")
                return
            manager.app.msg(user, str(x[0]))
            _notes[user].remove(x[0])
            manager.app.msg(user, "You now have " + str(len(x)) + " messages. Use !note read to read the next one.")
            if len(x) == 0:
                _notes.pop(user, None)
            manager.app.plugin_set_setting("notePlugin", "notes", _notes)
        elif task == "note" and args[0] == "purge":
            manager = PluginManagerSingleton.get()  
            if not user in manager.app.plugin_get_setting("notePlugin", "allowedUsers"):
                return
            manager.app.plugin_set_setting("notePlugin", "notes", {})
            manager.app.msg(user, "Notes purged.")

    def user_joined(self, user, channel):
        user = user.split("!")[0]
        manager = PluginManagerSingleton.get()
        _notes = manager.app.plugin_get_setting("notePlugin", "notes")
        if user in _notes:
            if len(_notes[user]) > 0:
                manager.app.msg(user, "You have " + str(len(_notes[iser])) + " new messages. Use !note read to read each one.")
    def add_note(self, target, msg):
        manager = PluginManagerSingleton.get()
        _notes = manager.app.plugin_get_setting("notePlugin", "notes")
        x = None
        try:
            x = _notes[target]                
        except KeyError:
            _notes[target] = []
            x = _notes[target]
        x.append(msg)
        _notes[target] = x
        manager.app.plugin_set_setting("notePlugin", "notes", _notes)
