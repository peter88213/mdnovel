"""A relationship matrix view for mdnovel

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from pathlib import Path
import sys
from tkinter import ttk

from mdnvlib.matrix.table_manager import TableManager
from mdnvlib.novx_globals import _
from mdnvlib.view.icons.set_icon_tk import set_icon
import tkinter as tk


class MatrixViewManager:
    """mdnovel relationship matrix view class."""
    APPLICATION = _('Matrix')
    SETTINGS = dict(
        window_geometry='600x800',
        color_bg_00='gray80',
        color_bg_01='gray85',
        color_bg_10='gray95',
        color_bg_11='white',
        color_arc_heading='deepSkyBlue',
        color_arc_node='deepSkyBlue3',
        color_character_heading='goldenrod1',
        color_character_node='goldenrod3',
        color_location_heading='coral1',
        color_location_node='coral3',
        color_item_heading='aquamarine1',
        color_item_node='aquamarine3',
    )
    OPTIONS = {}

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        self._ui.toolsMenu.entryconfig(self.APPLICATION, state='disabled')
        self._matrixButton.config(state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        self._ui.toolsMenu.entryconfig(self.APPLICATION, state='normal')
        self._matrixButton.config(state='normal')

    def __init__(self, model, view, controller, prefs=None):
        """Add a submenu to the 'Tools' menu.
        
        Positional arguments:
            model -- Reference to the model instance of the application.
            view -- Reference to the main view instance of the application.
            controller -- Reference to the main controller instance of the application.

        Optional arguments:
            prefs -- deprecated. Please use controller.get_preferences() instead.
        
        """
        self._mdl = model
        self._ui = view
        self._ctrl = controller
        self._matrixViewer = None

        #--- Load configuration.
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            configDir = f'{homeDir}/.mdnovel/config'
        except:
            configDir = '.'
        self.iniFile = f'{configDir}/matrix.ini'
        self.configuration = self._mdl.nvService.make_configuration(
            settings=self.SETTINGS,
            options=self.OPTIONS
            )
        self.configuration.read(self.iniFile)
        self.kwargs = {}
        self.kwargs.update(self.configuration.settings)
        self.kwargs.update(self.configuration.options)

        # Create an entry to the Tools menu.
        self._ui.toolsMenu.add_command(label=self.APPLICATION, command=self._start_viewer)
        self._ui.toolsMenu.entryconfig(self.APPLICATION, state='disabled')

        #--- Configure the toolbar.
        self._configure_toolbar()

    def lock(self):
        """Inhibit changes on the model."""
        self._ui.toolsMenu.entryconfig(self.APPLICATION, state='disabled')
        self._matrixButton.disable()
        if self._matrixViewer:
            self._matrixViewer.lock()

    def on_close(self):
        """Apply changes and close the window."""
        self.on_quit()

    def on_quit(self):
        """Actions to be performed when mdnovel is closed."""
        if self._matrixViewer:
            if self._matrixViewer.isOpen:
                self._matrixViewer.on_quit()

        #--- Save configuration
        for keyword in self.kwargs:
            if keyword in self.configuration.options:
                self.configuration.options[keyword] = self.kwargs[keyword]
            elif keyword in self.configuration.settings:
                self.configuration.settings[keyword] = self.kwargs[keyword]
        self.configuration.write(self.iniFile)

    def unlock(self):
        """Enable changes on the model."""
        self._ui.toolsMenu.entryconfig(self.APPLICATION, state='normal')
        self._matrixButton.enable()
        if self._matrixViewer:
            self._matrixViewer.unlock()

    def _configure_toolbar(self):

        # Get the icons.
        prefs = self._ctrl.get_preferences()
        if prefs.get('large_icons', False):
            size = 24
        else:
            size = 16
        try:
            iconPath = f'{os.path.dirname(sys.argv[0])}/icons/{size}'
        except:
            iconPath = None
        try:
            matrixIcon = tk.PhotoImage(file=f'{iconPath}/matrix.png')
        except:
            matrixIcon = None

        # Put a Separator on the toolbar.
        tk.Frame(self._ui.toolbar.buttonBar, bg='light gray', width=1).pack(side='left', fill='y', padx=4)

        # Initialize the operation.
        self._matrixButton = ttk.Button(
            self._ui.toolbar.buttonBar,
            text=_('Matrix'),
            image=matrixIcon,
            command=self._start_viewer
            )
        self._matrixButton.pack(side='left')
        self._matrixButton.image = matrixIcon

        # Initialize tooltip.
        if not prefs['enable_hovertips']:
            return

        try:
            from idlelib.tooltip import Hovertip
        except ModuleNotFoundError:
            return

        Hovertip(self._matrixButton, self._matrixButton['text'])

    def _start_viewer(self):
        if not self._mdl.prjFile:
            return

        if self._matrixViewer:
            if self._matrixViewer.isOpen:
                if self._matrixViewer.state() == 'iconic':
                    self._matrixViewer.state('normal')
                self._matrixViewer.lift()
                self._matrixViewer.focus()
                return

        self._matrixViewer = TableManager(self._mdl, self._ui, self._ctrl, self, **self.kwargs)
        self._matrixViewer.title(f'{self._mdl.novel.title} - {self.APPLICATION}')
        set_icon(self._matrixViewer, icon='mLogo32', default=False)
