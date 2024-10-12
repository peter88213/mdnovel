"""Provide a class for the mdnovel settings window.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from mdnvlib.widgets.label_combo import LabelCombo
from mdnvlib.novx_globals import _
import tkinter as tk


class SettingsWindow(tk.Toplevel):

    def __init__(self, view, prefs, extraThemes, size, **kw):
        self._ui = view
        self._prefs = prefs
        self._extraThemes = extraThemes
        super().__init__(**kw)
        self.title(_('Theme Changer'))
        self.geometry(size)
        self.grab_set()
        self.focus()
        window = ttk.Frame(self)
        window.pack(fill='both')

        # Combobox for theme setting.
        theme = self._ui.guiStyle.theme_use()
        themeList = list(self._ui.guiStyle.theme_names())
        themeList.sort()
        self._theme = tk.StringVar(value=theme)
        self._theme.trace('w', self._change_theme)
        themeCombobox = LabelCombo(
            window,
            text=_('GUI Theme'),
            textvariable=self._theme,
            values=themeList,
            lblWidth=20
            )
        themeCombobox.pack(padx=5, pady=5)

        # "Close" button.
        ttk.Button(window, text=_('Close'), command=self.destroy).pack(side='right', padx=5, pady=5)

    def _change_theme(self, *args, **kwargs):
        theme = self._theme.get()
        self._prefs['gui_theme'] = theme
        if self._extraThemes:
            self._ui.guiStyle.set_theme(self._prefs['gui_theme'])
        else:
            self._ui.guiStyle.theme_use(self._prefs['gui_theme'])

