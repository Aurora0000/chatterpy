from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
import string
import logging
from bs4 import BeautifulSoup
import re
import urllib2

class manPlugin(IPlugin):

    def botmsg(self, user, channel, task, args):
        if not args:
            return  # All of our commands require arguments.
        if task == "man":
            manager = PluginManagerSingleton.get()
            user = user.split("!")[0]
            if user in manager.app.plugin_get_setting("manPlugin", "blacklist"):
                manager.app.msg(channel, "You're blacklisted!")
                return
            elif channel == manager.app.nickname:
                channel = user

            if args[0] == "get":
                topic = args[1]
                url = "http://man.he.net/?topic=" + topic + "&section=all"
                pg = urllib2.urlopen(url).read()
                logging.debug(url)
                soup = BeautifulSoup(pg)
                pre = soup.find("pre")
                text = string.join(pre.findAll(text=True)).decode("utf8").encode("ascii", "ignore")
                manager.app.msg(channel, text[:250] + "...")
                manager.app.msg(channel, "More information at " + str(url))
