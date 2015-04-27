from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
from bs4 import BeautifulSoup
import string
import logging
import urllib2

class wikipediaPlugin(IPlugin):

    def botmsg(self, user, channel, task, args):
        if not args:
            return  # All of our commands require arguments.
        if task == "wiki":
            manager = PluginManagerSingleton.get()
            user = user.split("!")[0]
            if user in manager.app.plugin_get_setting("wikipediaPlugin", "blacklist"):
                manager.app.msg(channel, "You're blacklisted for abuse (ha ha ha ha).")
                return
            if args[0] == "get":
                topic = string.join(args[1:])
                topic = topic.replace(" ", "_")
                url = "http://en.wikipedia.com/wiki/" + topic
                logging.debug("Checking url "+ url)
                pg = urllib2.urlopen(url)
                soup = BeautifulSoup(pg)
                mainText = soup.find("div", {"id": "mw-content-text"})
                firstParagraph = mainText.find("p")
                asciiParagraph = firstParagraph.text.encode("ascii", "ignore").decode("ascii")
                manager.app.msg(channel, str(asciiParagraph)[:250] + "...")
                manager.app.msg(channel, "More information at " + url)
        
