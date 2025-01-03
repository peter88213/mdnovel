"""Provide an abstract view component node class.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/apptk
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from abc import abstractmethod

from apptk.model.observable import Observable
from apptk.view.view_component_base import ViewComponentBase


class ViewComponentNode(Observable, ViewComponentBase):
    """A node in the view composite structure tree.
    
    Subordinate leaves can be registered and unregistered.
    
    Passes down the following commands to the leaves:
        - refresh
        - lock/unlock
        - emable/disable menu    
    """

    @abstractmethod
    def __init__(self, model, view, controller):
        Observable.__init__(self)
        ViewComponentBase.__init__(self, model, view, controller)

    def disable_menu(self):
        """Disable UI widgets, e.g. when no project is open."""
        for client in self._clients:
            client.disable_menu()

    def enable_menu(self):
        """Enable UI widgets, e.g. when a project is opened."""
        for client in self._clients:
            client.enable_menu()

    def lock(self):
        """Inhibit changes on the model."""
        for client in self._clients:
            client.lock()

    def refresh(self):
        """Refresh all view components."""
        self.refresh_clients()

    def unlock(self):
        """Enable changes on the model."""
        for client in self._clients:
            client.unlock()

