"""A "Story Templates" manager for mdnovel.

Adds a 'Add Story Templates' entry to the 'Tools' menu to open a window
with a combobox that lists all available themes. 
The selected theme will be persistently applied.  

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_templates
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from pathlib import Path
from tkinter import filedialog
from tkinter import messagebox

from mdnvlib.novx_globals import Error
from mdnvlib.novx_globals import _
from mdnvlib.novx_globals import norm_path
from apptk.plugin.plugin_base import PluginBase
from mdnvlib.plugin.templates.md_template import MdTemplate
import tkinter as tk


class Templates(PluginBase):
    """A 'Story Templates' manager class."""
    FEATURE = _('Story Templates')

    def __init__(self, model, view, controller):
        """Add a submenu to the 'Tools' menu.
        
        Positional arguments:
            model -- reference to the main model instance of the application.
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.

        Optional arguments:
            prefs -- deprecated. Please use controller.get_preferences() instead.
        
        """
        super().__init__(model, view, controller)
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            self._templateDir = f'{homeDir}/.mdnovel/templates'
        except:
            self._templateDir = '.'

        # Create "Story Templates" submenu.
        self._templatesMenu = tk.Menu(self._ui.toolsMenu, tearoff=0)
        self._templatesMenu.add_command(label=f"{_('Load')}...", command=self._load_template)
        self._templatesMenu.add_command(label=f"{_('Save')}...", command=self._save_template)
        self._templatesMenu.add_command(label=_('Open folder'), command=self._open_folder)

        # Add an entry to the "File > New" menu.
        self._ui.newMenu.add_command(label=_('Create from template...'), command=self._new_project)

        # Create Tools menu entry.
        self._ui.toolsMenu.add_cascade(label=self.FEATURE, menu=self._templatesMenu)
        self._fileTypes = [(MdTemplate.DESCRIPTION, MdTemplate.EXTENSION)]

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        self._templatesMenu.entryconfig(f"{_('Load')}...", state='disabled')
        self._templatesMenu.entryconfig(f"{_('Save')}...", state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        self._templatesMenu.entryconfig(f"{_('Load')}...", state='normal')
        self._templatesMenu.entryconfig(f"{_('Save')}...", state='normal')

    def _load_template(self):
        """Create a structure of "Todo" chapters and scenes from a Markdown file."""
        fileName = filedialog.askopenfilename(
            filetypes=self._fileTypes,
            defaultextension=self._fileTypes[0][1],
            initialdir=self._templateDir
            )
        if fileName:
            try:
                templates = MdTemplate(fileName, self._mdl, self._ctrl)
                templates.read()
            except Error as ex:
                messagebox.showerror(_('Template loading aborted'), str(ex))

    def _new_project(self):
        """Create a mdnovel project instance."""
        self._ctrl.new_project()
        self._load_template()

    def _open_folder(self):
        """Open the templates folder with the OS file manager."""
        try:
            os.startfile(norm_path(self._templateDir))
            # Windows
        except:
            try:
                os.system('xdg-open "%s"' % norm_path(self._templateDir))
                # Linux
            except:
                try:
                    os.system('open "%s"' % norm_path(self._templateDir))
                    # Mac
                except:
                    pass

    def _save_template(self):
        """Save a structure of "Todo" chapters and scenes to a Markdown file."""
        fileName = filedialog.asksaveasfilename(filetypes=self._fileTypes,
                                              defaultextension=self._fileTypes[0][1],
                                              initialdir=self._templateDir)
        if not fileName:
            return

        try:
            templates = MdTemplate(fileName, self._mdl, self._ctrl)
            templates.write()
        except Error as ex:
            messagebox.showerror(_('Cannot save template'), str(ex))

        self._ui.set_status(_('Template saved.'))

