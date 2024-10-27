"""Provide a plugin collection class.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/apptk
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""


class PluginCollection(list):

    PLUGINS = []

    def __init__(self, model, view, controller):
        """Instantiate the plugin objects and put them on the list."""
        super().__init__()
        for plugin in self.PLUGINS:
            self.append(plugin(model, view, controller))

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        for plugin in self:
            try:
                plugin.disable_menu()
            except:
                pass

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        for plugin in self:
            try:
                plugin.enable_menu()
            except:
                pass

    def on_quit(self):
        """Perform actions before the application is closed."""
        for plugin in self:
            try:
                plugin.on_quit()
            except:
                pass

    def on_close(self):
        """Perform actions before a project is closed."""
        for plugin in self:
            try:
                plugin.on_close()
            except:
                pass

