#!/usr/bin/env python
from yapsy.PluginManager import PluginManagerSingleton
from ChatterUtils import PluginConfigurationManager
from itertools import chain
import subprocess

class ChatterCleaner:
    def __init__(self):
        self.plugin_configs = PluginConfigurationManager("./plugins")
        manager = PluginManagerSingleton.get()        
        manager.app = self
        manager.setPluginPlaces(["plugins"])   
        manager.collectPlugins()

    def clean(self):
        manager = PluginManagerSingleton.get()
        for plugin in manager.getAllPlugins():
            if hasattr(plugin.plugin_object, "cleanup"):
                try:
                    plugin.plugin_object.cleanup()
                except StandardError as e:
                    print(e)
                    return

    def plugin_get_setting(self, name, setting):
        return self.plugin_configs.get_setting(setting, name)

    def plugin_set_setting(self, name, setting, value):
        self.plugin_configs.set_setting(setting, name, value)

if __name__ == "__main__":
    cleaner = ChatterCleaner()
    cleaner.clean()
    print("Cleaned!")
    
