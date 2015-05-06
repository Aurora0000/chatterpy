from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
import string
import time
# The python file's name must be the same as the .chatter file's module attribute
class awayPlugin(IPlugin):

    def botmsg(self, user, channel, task, args):
        user = user.split("!")[0] 
        if task == "away":
            manager = PluginManagerSingleton.get()
            if manager.app.plugin_get_setting("awayPlugin", "pmOnly") == "yes":
                channel = user
            elif channel == manager.app.nickname:
                channel = user

            if args[0] == "reason":
                reason = self.get_reason_for_away(args[1])
                manager.app.msg(channel, args[1] + " is away for the following reason: " + str(reason))
            elif args[0] == "set":
                reason = string.join(args[1:])
                self.add_user_as_away(user, reason)
                manager.app.msg(channel, "Your away reason has been set.")
            elif args[0] == "unset":
                self.remove_user_as_away(user)
                manager.app.msg(channel, "Your away reason has been removed.")
            elif args[0] == "purge":
                if user not in manager.app.plugin_get_setting("awayPlugin", "allowedUsers"):
                    manager.app.msg(channel, "You're not permitted to do that!")
                    return
                manager.app.plugin_set_setting("awayPlugin", "awayReasons", {})

    def add_user_as_away(self, user, reason):
        manager = PluginManagerSingleton.get()
        _cur = manager.app.plugin_get_setting("awayPlugin", "awayReasons")
        _cur[user] = reason + " (set at " + time.strftime("%c") + ")"
        manager.app.plugin_set_setting("awayPlugin", "awayReasons", _cur)

    def remove_user_as_away(self, user):
        manager = PluginManagerSingleton.get()
        _cur = manager.app.plugin_get_setting("awayPlugin", "awayReasons")
        _cur.pop(user, None)
        manager.app.plugin_set_setting("awayPlugin", "awayReasons", _cur)

    def get_reason_for_away(self, user):
        manager = PluginManagerSingleton.get()
        _cur = manager.app.plugin_get_setting("awayPlugin", "awayReasons")
        try:
            return _cur[user]
        except KeyError:
            return "User is not away!"

    def cleanup(self):
        manager = PluginManagerSingleton.get()
        manager.app.plugin_set_setting("awayPlugin", "awayReasons", {})
