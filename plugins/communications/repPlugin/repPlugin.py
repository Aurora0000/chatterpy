from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
# The python file's name must be the same as the .chatter file's module attribute
class repPlugin(IPlugin):
    
    def privmsg(self, user, channel, msg):
        if "+1" in msg:
            manager = PluginManagerSingleton.get()
            user = user.split("!")[0]
            manager.app.msg(channel, user + ": You can give rep to that user with !rep give [user]")

    def botmsg(self, user, channel, task, args):
        if task == "rep":
            user = user.split("!")[0]
            if args[0] == "give":
                manager = PluginManagerSingleton.get()
                if args[1] == user:
                    manager.app.msg(channel, "You cannot give yourself rep.")
                    return
                lastRep = manager.app.plugin_get_setting("repPlugin", "lastRep")
                if user + ":" + args[1] == str(lastRep):
                    manager.app.msg(channel, "You've already given this person rep!")
                    return
                self.give_rep(args[1])
                manager.app.plugin_set_setting("repPlugin", "lastRep", user + ":" + args[1])
                manager.app.msg(channel, args[1] + " has received 1 rep from " + user)
            elif args[0] == "check":
                manager = PluginManagerSingleton.get()
                manager.app.msg(channel, args[1] + " has " + str(self.get_rep(args[1])) + " rep!")
            elif args[0] == "purge":
                manager = PluginManagerSingleton.get()
                manager.app.plugin_set_setting("repPlugin", "repData", {})
                manager.app.plugin_set_setting("repPlugin", "lastRep", "")
                manager.app.msg(channel, "Rep data purged.")
    
    def get_rep(self, user):
        manager = PluginManagerSingleton.get()
        repData = manager.app.plugin_get_setting("repPlugin", "repData")
        repAmount = 0
        try:
            repAmount = repData[user]
        except KeyError:
            pass
        return repAmount

    def give_rep(self, user):
        manager = PluginManagerSingleton.get()
        repData = manager.app.plugin_get_setting("repPlugin", "repData")
        try:
            repData[user] = repData[user] + 1
        except KeyError:
            repData[user] = 1
        manager.app.plugin_set_setting("repPlugin", "repData", repData)
