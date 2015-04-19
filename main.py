#!/usr/bin/env python
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, ssl
import time, sys, logging, json, traceback
from yapsy.PluginManager import PluginManagerSingleton
class IRCBot(irc.IRCClient):
    nickname = "Bot123"     # Default values, something's *seriously* 
    password = ""           # wrong if these are ever used...
    def connectionMade(self):
        self.nickname = self.factory.nickname
        self.password = self.factory.password
        self.configuration = self.factory.config
        irc.IRCClient.connectionMade(self)
        logging.log(10, "Bot connected to server")
        manager = PluginManagerSingleton.get()
        manager.app = self
        manager.setPluginPlaces(["plugins"])   
        manager.collectPlugins()
        logging.log(10, "Plugins loaded.")        
        for p in manager.getAllPlugins():
            manager.activatePluginByName(p.name)
            if hasattr(p.plugin_object, "plugin_loaded"):
                try:
                    p.plugin_object.plugin_loaded()
                except StandardError as e:
                    tb = traceback.format_exc()
                    logging.log(40, "Unhandled exception! " + tb)
            else:
                logging.log(10, p.name + " does not have a plugin_loaded hook!")
 
    def connectionLost(self, reason):
        #connection fail
        pass
    def signedOn(self):
        for chan in self.factory.channels:
            self.join(str(chan))
 
    def joined(self, channel):
        manager = PluginManagerSingleton.get()
        for pluginInfo in manager.getAllPlugins():  
            if pluginInfo.is_activated and hasattr(pluginInfo.plugin_object, "joined"):  
                try: 
                    pluginInfo.plugin_object.joined(channel)
                except StandardError as e:
                    tb = traceback.format_exc()
                    logging.log(40, "Unhandled exception! " + tb)
            else:
                logging.log(10, pluginInfo.name + " not activated/no available function (joined)!")
    def privmsg(self, user, channel, msg):
        manager = PluginManagerSingleton.get()
        #TODO: Error checking/catching (not that important, Python saves us usually)
        for pluginInfo in manager.getAllPlugins():  
            if pluginInfo.is_activated and hasattr(pluginInfo.plugin_object, "privmsg"):   
                try:
                    pluginInfo.plugin_object.privmsg(user, channel, msg)
                except StandardError as e:
                    tb = traceback.format_exc()
                    logging.log(40, "Unhandled exception! " + tb)
            else:
                logging.log(10, pluginInfo.name + " not activated/no available function (privmsg)!")
        if msg.startswith("!"):
            for pluginInfo in manager.getAllPlugins():         
                if pluginInfo.is_activated and hasattr(pluginInfo.plugin_object, "botmsg"):       
                    args = msg.split(' ')
                    task = (args[0])[1:]    # Arguably nasty hack to select all characters after !
                    args = args[1:]         # Don't include the task in the args
                    try:
                        pluginInfo.plugin_object.botmsg(user, channel, task, args)
                    except StandardError as e:
                        tb = traceback.format_exc()
                        logging.log(40, "Unhandled exception! " + tb)
                else:
                    logging.log(10, pluginInfo.name + " not activated/no available function (botmsg)!")

    def action(self, user, channel, msg):
        #me
        pass

    def userJoined(self, user, channel):
        manager = PluginManagerSingleton.get()
        for pluginInfo in manager.getAllPlugins():  
            if pluginInfo.is_activated and hasattr(pluginInfo.plugin_object, "userJoined"):  
                try: 
                    pluginInfo.plugin_object.userJoined(user, channel)
                except StandardError as e:
                    tb = traceback.format_exc()
                    logging.log(40, "Unhandled exception! " + tb)
            else:
                logging.log(10, pluginInfo.name + " not activated/no available function (userJoined)!")
 
    def irc_NICK(self, prefix, params):
        # User changed their nick. We abstract this slightly.
        manager = PluginManagerSingleton.get()
        for pluginInfo in manager.getAllPlugins():  
            if pluginInfo.is_activated and hasattr(pluginInfo.plugin_object, "user_changed_nick"):  
                try: 
                    # Prefix is nick!user@host, we only want nick.
                    old_nick = prefix.split("!")[0]   
                    pluginInfo.plugin_object.user_changed_nick(old_nick, new_nick)
                except StandardError as e:
                    tb = traceback.format_exc()
                    logging.log(40, "Unhandled exception! " + tb)
            else:
                logging.log(10, pluginInfo.name + " not activated/no available function (userJoined)!")
    def alterCollidedNick(self, nickname):
        # Lines are very long, but still, blame Python's verbose ternary statements
        prefix = str(self.configuration["collision_prefix"]) if "collision_prefix" in self.configuration else ""
        suffix = str(self.configuration["collision_suffix"]) if "collision_suffix" in self.configuration else ""
        return  prefix + nickname + suffix

    def rehash_plugins(self):
        #Very hacky, but the singleton doesn't seem to have any other option...
        PluginManagerSingleton._PluginManagerSingleton__instance = None

        manager = PluginManagerSingleton.get()
        manager.app = self
        manager.quit = False
        manager.setPluginPlaces(["plugins"])   
        manager.collectPlugins()
        for p in manager.getAllPlugins():
            manager.activatePluginByName(p.name)
            if hasattr(p.plugin_object, "plugin_loaded"):
                p.plugin_object.plugin_loaded()
        logging.log(10, "Plugins reloaded.")
    
    def unload_plugin(self, plugin_name):
        manager.deactivatePluginByName(plugin_name)
    def load_plugin(self, plugin_name):
        manager.activatePluginByName(plugin_name)


class BotFactory(protocol.ClientFactory):
    protocol = IRCBot
 
    def __init__(self, channels, nickname, password, config):
        self.channels = channels
        self.nickname = nickname
        self.password = password
        self.config = config
        manager = PluginManagerSingleton.get()
        manager.quit = False
    def clientConnectionLost(self, connector, reason):
        #Reconnect if we weren't told to quit
        manager = PluginManagerSingleton.get()
        if manager.quit == False:        
            connector.connect()
 
    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()

def loadConfig(file):
    #Verification that the needed types are present *could* be done, but I don't really care.    
    f = open(file).read()
    json_data = json.loads(f)
    return json_data
if __name__ == '__main__':
    data = loadConfig("bot.conf")
    #todo: make configurable
    logging.basicConfig(filename=data["logFile"], format="[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)
    pwd = data["password"] if "password" in data else ""    #Assume no password if it isn't specified
    f = BotFactory(data["channels"], str(data["nickname"]), str(pwd), data)
    hostname = str(data["hostname"])
    port = int(data["port"])
    if "yes" in str(data["ssl"]): 
        reactor.connectSSL(hostname, port, f, ssl.ClientContextFactory())
    else:
        reactor.connectTCP(hostname, port, f)
    reactor.run() 
