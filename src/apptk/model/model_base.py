"""Provide a model base class for a MVC framework.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/apptk
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from abc import ABC, abstractmethod


class ModelBase(ABC):

    @abstractmethod
    def __init__(self):
        self._clients = []
        # objects to be updated on model change
        self._internalModificationFlag = False

    @property
    def isModified(self):
        # Boolean -- True if there are unsaved changes.
        return self._internalModificationFlag

    @isModified.setter
    def isModified(self, setFlag):
        self._internalModificationFlag = setFlag
        for client in self._clients:
            client.refresh()

    def register_client(self, client):
        if not client in self._clients:
            self._clients.append(client)

    def unregister_client(self, client):
        if client in self._clients:
            self._clients.remove(client)

    def on_element_change(self):
        """Callback function to report model element modifications."""
        self.isModified = True

