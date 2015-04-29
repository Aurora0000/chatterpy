#!/usr/bin/env python
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, ssl
from yapsy.PluginManager import PluginManagerSingleton
from pkgutil import iter_modules
import time
import sys
import logging
import logging.handlers
import json
import traceback
import os
import os.path

class ExceptionEventHandler(logging.StreamHandler):
    def emit(self, record):
        if record.levelno > 20:
            manager = PluginManagerSingleton.get()
            for pluginInfo in manager.getAllPlugins():  
                if pluginInfo.is_activated and hasattr(pluginInfo.plugin_object, "on_except"):  
                    try: 
                        pluginInfo.plugin_object.on_except(record)
                    except StandardError as e:
                        tb = traceback.format_exc()
                        logging.log(10, "[CRITICAL (MASKED)] Unhandled exception! " + tb)
                else:
                    logging.log(10, "\"" + pluginInfo.name + "\" not activated/no available function (on_except)!")
            logging.log(10, "All plugins notified of exception.")

class PluginConfigurationManager:
    configs = {}
    def __init__(self, folder):
        self.folder = folder
        self.collect_settings()
    
    def collect_settings(self):
        for dirpath, dirnames, filenames in os.walk(self.folder):
            for fn in [f for f in filenames if f.endswith(".chatterconf")]:
                self.configs[(fn.split(".")[0])] = os.path.join(dirpath, fn)
    def get_setting(self, setting, domain):
        # No error checking, if there's a problem, the caller needs to catch it
        f = open(self.configs[domain])
        json_data = json.loads(f.read())
        f.close()
        return json_data[setting]
    def set_setting(self, setting, domain, value):
        f = open(self.configs[domain], "r+")
        json_data = json.loads(f.read())
        json_data[setting] = value
        f.seek(0)
        f.write(json.dumps(json_data, indent=4))
        f.truncate()
        f.close()
    def get_json_data(self, domain):
        f = open(self.configs[domain])
        json_data = json.loads(f.read())
        f.close()
        return json_data



class IRCBot(irc.IRCClient):
    nickname = "Bot123"     # Default values, something's *seriously* 
    password = ""           # wrong if these are ever used...

    versionMajor = 0        # TODO: Update on release!
    versionMinor = 3
    versionPatch = 0
    
    def init_plugins(self):
        manager = PluginManagerSingleton.get()
        manager.app = self
        manager.quit = False
        manager.setPluginPlaces(["plugins"])   
        manager.collectPlugins()
        logging.log(10, "Plugins loaded.")    
        logging.log(10, "Checking plugin compatibility...")    
        for p in manager.getAllPlugins():
            try:
                pPath = p.path.split("/")[-1]
                if self.plugin_configs.get_setting("activated", pPath) == "true":
                    if self.are_modules_available(self.plugin_configs.get_setting("depends", pPath)):
                        versionString = str(self.versionMajor) + "." + str(self.versionMinor) + "." + str(self.versionPatch)
                        requireVersion = True if self.configuration["enforceVersion"] == "yes" else False
                        if self.plugin_configs.get_setting("version", pPath) == versionString and requireVersion:
                            manager.activatePluginByName(p.name)
                        else:
                            manager.deactivatePluginByName(p.name)
                            logging.log(30, "Plugin \"" + p.name + "\" is not for the correct version of ChatterPy!")
                    else:
                       manager.deactivatePluginByName(p.name)
                       logging.log(30, "Plugin \"" + p.name + "\" does not have all dependencies available!") 
                else:
                    manager.deactivatePluginByName(p.name)
            except LookupError as e:
                logging.log(30, "Plugin \"" + p.name + "\" has no valid .chatterconf file! The configuration may be invalid or inaccessible.")
                manager.deactivatePluginByName(p.name)
            if hasattr(p.plugin_object, "plugin_loaded"):
               try:
                   p.plugin_object.plugin_loaded()
               except StandardError as e:
                   tb = traceback.format_exc()
                   logging.log(40, "Unhandled exception! " + tb)
            else:
                logging.log(10, "\"" + p.name + "\" does not have a plugin_loaded hook!")
    def connectionMade(self):
        self.nickname = self.factory.nickname
        self.password = self.factory.password
        self.configuration = self.factory.config
        self.plugin_configs = PluginConfigurationManager("./plugins")
        irc.IRCClient.connectionMade(self)
        logging.log(10, "Bot connected to server")
        manager = PluginManagerSingleton.get()
        self.init_plugins()
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
                logging.log(10, "\"" + pluginInfo.name + "\" not activated/no available function (joined)!")

    def privmsg(self, user, channel, msg):
        manager = PluginManagerSingleton.get()
        for pluginInfo in manager.getAllPlugins():  
            if pluginInfo.is_activated and hasattr(pluginInfo.plugin_object, "privmsg"):   
                try:
                    pluginInfo.plugin_object.privmsg(user, channel, msg)
                except StandardError as e:
                    tb = traceback.format_exc()
                    logging.log(40, "Unhandled exception! " + tb)
            else:
                logging.log(10, "\"" + pluginInfo.name + "\" not activated/no available function (privmsg)!")
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
                    logging.log(10, "\"" + pluginInfo.name + "\" not activated/no available function (botmsg)!")

    def action(self, user, channel, msg):
        manager = PluginManagerSingleton.get()
        for pluginInfo in manager.getAllPlugins():  
            if pluginInfo.is_activated and hasattr(pluginInfo.plugin_object, "action"):  
                try: 
                    pluginInfo.plugin_object.action(user, channel, msg)
                except StandardError as e:
                    tb = traceback.format_exc()
                    logging.log(40, "Unhandled exception! " + tb)
            else:
                logging.log(10, "\"" + pluginInfo.name + "\" not activated/no available function (action)!")

    def userJoined(self, user, channel):
        manager = PluginManagerSingleton.get()
        for pluginInfo in manager.getAllPlugins():  
            if pluginInfo.is_activated and hasattr(pluginInfo.plugin_object, "user_joined"):  
                try: 
                    pluginInfo.plugin_object.user_joined(user, channel)
                except StandardError as e:
                    tb = traceback.format_exc()
                    logging.log(40, "Unhandled exception! " + tb)
            else:
                logging.log(10, "\"" + pluginInfo.name + "\" not activated/no available function (user_joined)!")
 
    def irc_NICK(self, prefix, params):
        # User changed their nick. We abstract this slightly.
        manager = PluginManagerSingleton.get()
        for pluginInfo in manager.getAllPlugins():  
            if pluginInfo.is_activated and hasattr(pluginInfo.plugin_object, "user_changed_nick"):  
                try: 
                    # Prefix is nick!user@host, we only want nick.
                    old_nick = prefix   
                    suff = prefix.split("!")[1]
                    new_nick = params[0] + "!" + suff
                    pluginInfo.plugin_object.user_changed_nick(old_nick, new_nick)
                except StandardError as e:
                    tb = traceback.format_exc()
                    logging.log(40, "Unhandled exception! " + tb)
            else:
                logging.log(10, "\"" + pluginInfo.name + "\" not activated/no available function (user_changed_nick)!")
    def alterCollidedNick(self, nickname):
        preSetting = str(self.configuration["collision_prefix"])
        prefix = preSetting if "collision_prefix" in self.configuration else ""
        sufSetting = str(self.configuration["collision_suffix"])
        suffix = sufSetting if "collision_suffix" in self.configuration else ""
        return  prefix + nickname + suffix

    def rehash_plugins(self):
        # Very hacky, but the singleton doesn't seem to have any other option...
        PluginManagerSingleton._PluginManagerSingleton__instance = None

        self.init_plugins()
    
    def unload_plugin(self, plugin_name):
        manager = PluginManagerSingleton.get()
        p = self.get_plugin_short_path(plugin_name)
        self.plugin_configs.set_setting("activated", p, "false")
        manager.deactivatePluginByName(plugin_name)
    
    def load_plugin(self, plugin_name):
        manager = PluginManagerSingleton.get()
        p = self.get_plugin_short_path(plugin_name)
        self.plugin_configs.set_setting("activated", p, "true")
        manager.activatePluginByName(plugin_name)

    def get_plugin_short_path(self, name):
        manager = PluginManagerSingleton.get()
        return manager.getPluginByName(name).path.split("/")[-1]

    def plugin_get_setting(self, name, setting):
        return self.plugin_configs.get_setting(setting, name)

    def plugin_set_setting(self, name, setting, value):
        self.plugin_configs.set_setting(setting, name, value)

    def plugin_list_settings(self, name):
        settings = []
        for s in self.plugin_configs.get_json_data(name):
            settings.append(s)
        return settings

    def is_module_available(self, module):
        try:
            __import__(module)
        except ImportError:
            return False
        else:
            return True
   
    def are_modules_available(self, modules):
        for m in modules:
            if not self.is_module_available(m):
                return False
        return True
    
class BotFactory(protocol.ClientFactory):
    protocol = IRCBot
 
    def __init__(self, channels, nickname, password, config):
        self.channels = channels
        self.nickname = nickname
        self.password = password
        self.config = config
    def clientConnectionLost(self, connector, reason):
        #Reconnect if we weren't told to quit
        manager = PluginManagerSingleton.get()
        if manager.quit == False:        
            connector.connect()
 
    def clientConnectionFailed(self, connector, reason):
        print ("Connection failed:" + reason)
        reactor.stop()

def loadConfig(file):
    # Verification that the needed types are present *could* be done, but I don't really care.    
    f = open(file).read()
    json_data = json.loads(f)
    return json_data

if __name__ == '__main__':
    # Load the JSON configuration file
    data = loadConfig("bot.conf")
    log_lvl = logging.INFO
    if data["logLevel"] == "DEBUG":
        log_lvl = logging.DEBUG
    elif data["logLevel"] == "INFO":
        log_lvl = logging.INFO
    elif data["logLevel"] == "WARNING":
        log_lvl = logging.WARNING
    elif data["logLevel"] == "ERROR":
        log_lvl = logging.ERROR
    # Set up formatters and logger
    _format = "[%(asctime)s] %(levelname)s: %(message)s"
    _datefmt = "%Y-%m-%d %H:%M:%S"
    logger = logging.getLogger()
    logger.setLevel(log_lvl)
    # Store maximum of 500kb of logs, make this configurable in future
    handler = logging.handlers.RotatingFileHandler(data["logFile"], maxBytes=(1024*100), backupCount=3)
    formatter = logging.Formatter(_format, datefmt=_datefmt)
    handler.setFormatter(formatter)
    logger.addHandler(ExceptionEventHandler())
    logger.addHandler(handler)

    pwd = data["password"] if "password" in data else ""    #Assume no password if it isn't specified
    f = BotFactory(data["channels"], str(data["nickname"]), str(pwd), data)
    hostname = str(data["hostname"])
    port = int(data["port"])
    pconf = PluginConfigurationManager("./plugins")

    if "yes" in str(data["ssl"]): 
        reactor.connectSSL(hostname, port, f, ssl.ClientContextFactory())
    else:
        reactor.connectTCP(hostname, port, f)
    reactor.run() 
