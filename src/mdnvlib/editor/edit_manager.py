"""A multi-section "plain text" editor class for mdnovel.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from pathlib import Path
import sys

from mdnvlib.editor.editor_window import EditorWindow
from mdnvlib.novx_globals import SECTION_PREFIX
from mdnvlib.nv_globals import SC_EDITOR_ICON
from mdnvlib.nv_globals import _
import tkinter as tk


class EditManager:
    """mdnovel multi-section "plain text" editor class."""
    SETTINGS = dict(
        ed_win_geometry='600x800',
        ed_color_mode=0,
        ed_color_bg_bright='white',
        ed_color_fg_bright='black',
        ed_color_bg_light='antique white',
        ed_color_fg_light='black',
        ed_color_bg_dark='gray20',
        ed_color_fg_dark='light grey',
        ed_font_family='Courier',
        ed_font_size=12,
        ed_line_spacing=4,
        ed_line_width=600,
        ed_paragraph_spacing=4,
        ed_margin_x=40,
        ed_margin_y=20,
    )
    OPTIONS = dict(
        ed_fullscreen=False,
        ed_live_wordcount=False,
    )

    def __init__(self, model, view, controller):
        """Add a submenu to the main menu.
        
        Positional arguments:
            model -- reference to the main model instance of the application.
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.

        Overrides the superclass method.
        """
        self._mdl = model
        self._ui = view
        self._ctrl = controller

        #--- Load configuration.
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            configDir = f'{homeDir}/.mdnovel/config'
        except:
            configDir = '.'
        self.iniFile = f'{configDir}/editor.ini'
        self.configuration = self._mdl.nvService.make_configuration(
            settings=self.SETTINGS,
            options=self.OPTIONS
            )
        self.configuration.read(self.iniFile)
        self.kwargs = {}
        self.kwargs.update(self.configuration.settings)
        self.kwargs.update(self.configuration.options)

        # Add the "Edit" command to mdnovel's "Section" menu.
        self._ui.sectionMenu.add_separator()
        self._ui.sectionMenu.add_command(label=_('Edit'), underline=0, command=self.open_editor_window)

        # Set window icon.
        self.sectionEditors = {}
        try:
            path = os.path.dirname(sys.argv[0])
            if not path:
                path = '.'
            self._icon = tk.PhotoImage(file=f'{path}/icons/{SC_EDITOR_ICON}.png')
        except:
            self._icon = None

        # Configure the editor box.
        EditorWindow.colorMode = tk.IntVar(
            value=int(self.kwargs['ed_color_mode'])
            )
        EditorWindow.liveWordCount = tk.BooleanVar(
            value=self.kwargs['ed_live_wordcount']
            )

        # Set Key bindings.
        self._ui.tv.tree.bind('<Double-1>', self.open_editor_window)
        self._ui.tv.tree.bind('<Return>', self.open_editor_window)

        # Register to be refreshed when a section is deleted.
        self._mdl.register_client(self)

    def close_editor_window(self, nodeId):
        if nodeId in self.sectionEditors and self.sectionEditors[nodeId].isOpen:
            self.sectionEditors[nodeId].on_quit()
            del self.sectionEditors[nodeId]

    def on_close(self, event=None):
        """Actions to be performed when a project is closed.
        
        Close all open section editor windows. 
        Overrides the superclass method.
        """
        for scId in self.sectionEditors:
            if self.sectionEditors[scId].isOpen:
                self.sectionEditors[scId].on_quit()

    def on_quit(self, event=None):
        """Actions to be performed when mdnovel is closed.
        
        Overrides the superclass method.
        """
        self.on_close()

        #--- Save project specific configuration
        self.kwargs['ed_color_mode'] = EditorWindow.colorMode.get()
        self.kwargs['ed_live_wordcount'] = EditorWindow.liveWordCount.get()
        for keyword in self.kwargs:
            if keyword in self.configuration.options:
                self.configuration.options[keyword] = self.kwargs[keyword]
            elif keyword in self.configuration.settings:
                self.configuration.settings[keyword] = self.kwargs[keyword]
        self.configuration.write(self.iniFile)

    def open_editor_window(self, event=None):
        """Create a section editor window with a menu bar, a text box, and a status bar.
        
        Overrides the superclass method.
        """
        try:
            nodeId = self._ui.tv.tree.selection()[0]
            if nodeId.startswith(SECTION_PREFIX):
                if self._mdl.novel.sections[nodeId].scType > 1:
                    return

                # A section is selected
                if nodeId in self.sectionEditors and self.sectionEditors[nodeId].isOpen:
                    self.sectionEditors[nodeId].lift()
                    return

                self.sectionEditors[nodeId] = EditorWindow(self, self._mdl, self._ui, self._ctrl, nodeId, self.kwargs['ed_win_geometry'], icon=self._icon)

        except IndexError:
            # Nothing selected
            pass

    def refresh(self):
        for scId in list(self.sectionEditors):
            if not scId in self._mdl.novel.sections:
                self.close_editor_window(scId)
