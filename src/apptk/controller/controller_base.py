"""Provide a controller base class for a MVC framework.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/apptk
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""

from abc import ABC, abstractmethod


class ControllerBase(ABC):

    @abstractmethod
    def __init__(self, title):
        # self._mdl = ModelBase()
        # self._mdl.register_client(self)
        # self._ui = ViewBase(self._mdl, self, title)
        # self.plugins = PluginCollection(self._mdl, self._ui, self)
        pass

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        self._ui.disable_menu()
        self.plugins.disable_menu()

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        self._ui.enable_menu()
        self.plugins.enable_menu()

    def get_view(self):
        """Return a reference to the application's main view object."""
        return self._ui

    def on_quit(self):
        self.plugins.on_quit()
        self._ui.on_quit()

    def refresh(self):
        """Callback function to report model element modifications."""
        pass
