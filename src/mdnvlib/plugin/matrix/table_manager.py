"""Provide a tkinter widget for relationship table management.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from apptk.view.view_component_base import ViewComponentBase
from mdnvlib.novx_globals import _
from mdnvlib.plugin.matrix.relations_table import RelationsTable
from mdnvlib.plugin.matrix.table_frame import TableFrame
from mdnvlib.view.platform.platform_settings import KEYS
from mdnvlib.view.platform.platform_settings import MOUSE
from mdnvlib.view.platform.platform_settings import PLATFORM
import tkinter as tk


class TableManager(ViewComponentBase, tk.Toplevel):

    def __init__(self, model, view, controller, manager, **kwargs):
        ViewComponentBase.__init__(self, model, view, controller)
        tk.Toplevel.__init__(self)

        self._manager = manager
        self._kwargs = kwargs

        self._statusText = ''

        self.geometry(kwargs['window_geometry'])
        self.lift()
        self.focus()

        #--- Register this view component.
        self._ui.register_client(self)

        #--- Event bindings.
        if PLATFORM != 'win':
            self.bind(KEYS.QUIT_PROGRAM[0], self.on_quit)
        self.protocol("WM_DELETE_WINDOW", self.on_quit)

        #--- Main menu.
        self.mainMenu = tk.Menu(self)
        self.config(menu=self.mainMenu)

        #--- Main window and table frame.
        self.mainWindow = ttk.Frame(self)
        self.mainWindow.pack(fill='both', expand=True)
        self.tableFrame = TableFrame(self.mainWindow)

        #--- The Relations Table.
        if self._mdl.novel is not None:
            self._relationsTable = RelationsTable(self.tableFrame, self._mdl.novel, **self._kwargs)
            self._relationsTable.set_nodes()
        self.isOpen = True
        self.tableFrame.pack(fill='both', expand=True, padx=2, pady=2)

        #--- Initialize the view update mechanism.
        self._skipUpdate = False
        self.bind(MOUSE.TOGGLE_STATE, self.on_element_change)

        # "Close" button.
        ttk.Button(self, text=_('Close'), command=self.on_quit).pack(side='right', padx=5, pady=5)

    def on_quit(self, event=None):
        self.isOpen = False
        self._manager.kwargs['window_geometry'] = self.winfo_geometry()
        self.tableFrame.destroy()
        # this is necessary for deleting the event bindings
        self._ui.unregister_client(self)
        self.destroy()

    def refresh(self):
        """Refresh the view after changes have been made "outsides"."""
        if self.isOpen:
            if not self._skipUpdate:
                self.tableFrame.pack_forget()
                self.tableFrame.destroy()
                self.tableFrame = TableFrame(self.mainWindow)
                self.tableFrame.pack(fill='both', expand=True, padx=2, pady=2)
                self._relationsTable.draw_matrix(self.tableFrame)
                self._relationsTable.set_nodes()

    def on_element_change(self, event=None):
        """Update the model, but not the view."""
        self._skipUpdate = True
        self._relationsTable.get_nodes()
        self._skipUpdate = False
