from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
import string
import logging
import urllib
import urllib2
import feedparser
import re

class msdnPlugin(IPlugin):

    def botmsg(self, user, channel, task, args):
        if not args:
            return  # All of our commands require arguments.
        if task == "msdn":
            manager = PluginManagerSingleton.get()
            if args[0] == "get":
                topic = string.join(args[1:])
                params = urllib.urlencode({"query": topic + " site:msdn.microsoft.com", "format": "RSS"}) 
                url = "https://social.msdn.microsoft.com/search/en-US/feed?" + params
                searchRes = feedparser.parse(url)
                try:
                    url = searchRes.entries[0].link
                    asciiParagraph = str(searchRes.entries[0].description)
                    manager.app.msg(channel, str(asciiParagraph)[:250] + "...")
                    manager.app.msg(channel, "More information at " + str(url))
                except:
                    manager.app.msg(channel, "Search unsuccessful.")
