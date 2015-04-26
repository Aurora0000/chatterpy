from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
import string
import feedparser
class forumFeed(IPlugin):
    def botmsg(self, user, channel, task, args):
        if not args:
            return  # All of our commands require arguments.
        manager = PluginManagerSingleton.get()
        if channel == manager.app.nickname:
            channel = user  # Crafty hack to allow bot to PM users if message
                            # isn't in a channel.
        if task == "feed" and args[0] == "latest":
            feed = feedparser.parse(manager.app.plugin_get_setting("forumFeed", "feedUrl"))
            user = user.split("!")[0]   # Remove the user and host
            title = str(feed.entries[0].title)
            link = str(feed.entries[0].link)
            manager.app.msg(channel, user + ": The latest message is \"" + title + "\" at " + link)
