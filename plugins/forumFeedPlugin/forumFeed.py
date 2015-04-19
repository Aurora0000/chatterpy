from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
import string
import feedparser
class forumFeed(IPlugin):
    def botmsg(self, user, channel, task, args):
        manager = PluginManagerSingleton.get()
        if task == manager.app.plugin_get_setting("forumFeed", "respondTo") and args[0] == "latest":
            feed = feedparser.parse(manager.app.plugin_get_setting("forumFeed", "feedUrl"))
            user = user.split("!")[0]   # Remove the user and host
            manager.app.msg(channel, user + ": The latest message is \"" + str(feed.entries[0].title) + "\" at " + str(feed.entries[0].link))
