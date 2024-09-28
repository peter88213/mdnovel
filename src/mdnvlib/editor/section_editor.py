"""A multi-section "plain text" editor plugin for mdnovel."""
import os
from pathlib import Path
import sys
from tkinter import messagebox

from mdnvlib.editor.editor_window import EditorWindow
from mdnvlib.novx_globals import SECTION_PREFIX
from mdnvlib.nv_globals import SC_EDITOR
from mdnvlib.nv_globals import SC_EDITOR_ICON
from mdnvlib.nv_globals import _
from mdnvlib.nv_globals import open_help
import tkinter as tk

ED_SETTINGS = dict(
        window_geometry='600x800',
        color_mode=0,
        color_fg_bright='white',
        color_bg_bright='black',
        color_fg_light='antique white',
        color_bg_light='black',
        color_fg_dark='light grey',
        color_bg_dark='gray20',
        font_family='Courier',
        font_size=12,
        line_spacing=4,
        paragraph_spacing=4,
        margin_x=40,
        margin_y=20,
)
ED_OPTIONS = dict(
        live_wordcount=False,
)


class SectionEditor:
    """novelibre multi-section "plain text" editor plugin class."""

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
            settings=ED_SETTINGS,
            options=ED_OPTIONS
            )
        self.configuration.read(self.iniFile)
        self.kwargs = {}
        self.kwargs.update(self.configuration.settings)
        self.kwargs.update(self.configuration.options)

        # Add the "Edit" command to novelibre's "Section" menu.
        self._ui.sectionMenu.add_separator()
        self._ui.sectionMenu.add_command(label=_('Edit'), underline=0, command=self.open_node)

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(label=_('Editor plugin Online help'), command=open_help)

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
            value=int(self.kwargs['color_mode'])
            )
        EditorWindow.liveWordCount = tk.BooleanVar(
            value=self.kwargs['live_wordcount']
            )

        # Set Key bindings.
        self._ui.tv.tree.bind('<Double-1>', self.open_node)
        self._ui.tv.tree.bind('<Return>', self.open_node)

    def on_close(self, event=None):
        """Actions to be performed when a project is closed.
        
        Close all open section editor windows. 
        Overrides the superclass method.
        """
        for scId in self.sectionEditors:
            if self.sectionEditors[scId].isOpen:
                self.sectionEditors[scId].on_quit()

    def on_quit(self, event=None):
        """Actions to be performed when novelibre is closed.
        
        Overrides the superclass method.
        """
        self.on_close()

        #--- Save project specific configuration
        self.kwargs['color_mode'] = EditorWindow.colorMode.get()
        self.kwargs['live_wordcount'] = EditorWindow.liveWordCount.get()
        for keyword in self.kwargs:
            if keyword in self.configuration.options:
                self.configuration.options[keyword] = self.kwargs[keyword]
            elif keyword in self.configuration.settings:
                self.configuration.settings[keyword] = self.kwargs[keyword]
        self.configuration.write(self.iniFile)

    def open_node(self, event=None):
        """Create a section editor window with a menu bar, a text box, and a status bar.
        
        Overrides the superclass method.
        """
        try:
            nodeId = self._ui.tv.tree.selection()[0]
            if nodeId.startswith(SECTION_PREFIX):
                if self._mdl.novel.sections[nodeId].scType > 1:
                    return

                # A section is selected
                if self._ctrl.isLocked:
                    messagebox.showinfo(SC_EDITOR, _('Cannot edit sections, because the project is locked.'))
                    return

                if nodeId in self.sectionEditors and self.sectionEditors[nodeId].isOpen:
                    self.sectionEditors[nodeId].lift()
                    return

                self.sectionEditors[nodeId] = EditorWindow(self, self._mdl, self._ui, self._ctrl, nodeId, self.kwargs['window_geometry'], icon=self._icon)

        except IndexError:
            # Nothing selected
            pass

