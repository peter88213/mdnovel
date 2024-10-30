"""Provide a class for export settings.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from mdnvlib.novx_globals import _
from mdnvlib.nv_globals import open_help
from mdnvlib.nv_globals import prefs
from mdnvlib.view.platform.platform_settings import KEYS
from apptk.view.modal_dialog import ModalDialog
import tkinter as tk


class ExportOptionsWindow(ModalDialog):
    """A pop-up window with export preference settings."""

    def __init__(self, model, view, controller, **kw):
        ModalDialog.__init__(self, model, view, controller, **kw)
        self.title(_('"Export" options'))
        window = ttk.Frame(self)
        window.pack(
            fill='both',
            padx=5,
            pady=5
            )
        frame1 = ttk.Frame(window)
        frame1.pack(fill='both', side='left')

        # Checkbox: Ask whether documents should be opened straight after export.
        self._askDocOpen = tk.BooleanVar(frame1, value=prefs['ask_doc_open'])
        ttk.Checkbutton(
            frame1,
            text=_('Ask before opening exported documents'),
            variable=self._askDocOpen
            ).pack(padx=5, pady=5, anchor='w')
        self._askDocOpen.trace('w', self._change_ask_doc_open)

        ttk.Separator(self, orient='horizontal').pack(fill='x')

        # "Close" button.
        ttk.Button(
            self,
            text=_('Close'),
            command=self.destroy
            ).pack(padx=5, pady=5, side='right')

        # "Help" button.
        ttk.Button(
            self,
            text=_('Online help'),
            command=self._open_help
            ).pack(padx=5, pady=5, side='right')

        # Set Key bindings.
        self.bind(KEYS.OPEN_HELP[0], self._open_help)

    def _change_ask_doc_open(self, *args):
        prefs['ask_doc_open'] = self._askDocOpen.get()

    def _open_help(self, event=None):
        open_help('export_menu#options')
