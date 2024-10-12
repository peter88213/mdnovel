"""Timeline syncronization for mdnovel.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
import os
from pathlib import Path
import sys
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import webbrowser

from mdnvlib.file.doc_open import open_document
from mdnvlib.novx_globals import Error
from mdnvlib.novx_globals import _
from mdnvlib.novx_globals import norm_path
from mdnvlib.timeline.tl_file import TlFile
import tkinter as tk


class TimelineManager:
    """Class for synchronization with Timeline."""

    APPLICATION = 'Timeline'
    SETTINGS = dict(
        section_label='Section',
        section_color='170,240,160',
        new_event_spacing='1'
    )
    OPTIONS = dict(
        lock_on_export=False,
    )

    def __init__(self, model, view, controller):
        """Add a submenu to the main menu.
        
        Positional arguments:
            model -- reference to the main model instance of the application.
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.
        """
        self._mdl = model
        self._ui = view
        self._ctrl = controller

        # Create a submenu in the Tools menu.
        self._pluginMenu = tk.Menu(self._ui.toolsMenu, tearoff=0)
        self._ui.toolsMenu.add_cascade(label=self.APPLICATION, menu=self._pluginMenu)
        self._ui.toolsMenu.entryconfig(self.APPLICATION, state='disabled')
        self._pluginMenu.add_command(label=_('Information'), command=self._info)
        self._pluginMenu.add_separator()
        self._pluginMenu.add_command(label=_('Create or update the timeline'), command=self._export_from_mdnov)
        self._pluginMenu.add_command(label=_('Update the project'), command=self._import_to_mdnov)
        self._pluginMenu.add_separator()
        self._pluginMenu.add_command(label=_('Open Timeline'), command=self._launch_application)

        # Add an entry to the "File > New" menu.
        self._ui.newMenu.add_command(label=_('Create from Timeline...'), command=self._create_mdnov)

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(label=_('Timeline plugin Online help'), command=lambda: webbrowser.open(self._HELP_URL))

        #--- Configure the toolbar.
        self._configure_toolbar()

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(self.APPLICATION, state='disabled')
        self._timelineButton.config(state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(self.APPLICATION, state='normal')
        self._timelineButton.config(state='normal')

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
            tlIcon = tk.PhotoImage(file=f'{iconPath}/tl.png')
        except:
            tlIcon = None

        # Put a Separator on the toolbar.
        tk.Frame(self._ui.toolbar.buttonBar, bg='light gray', width=1).pack(side='left', fill='y', padx=4)

        # Put a button on the toolbar.
        self._timelineButton = ttk.Button(
            self._ui.toolbar.buttonBar,
            text=_('Open Timeline'),
            image=tlIcon,
            command=self._launch_application
            )
        self._timelineButton.pack(side='left')
        self._timelineButton.image = tlIcon

        # Initialize tooltip.
        if not prefs['enable_hovertips']:
            return

        try:
            from idlelib.tooltip import Hovertip
        except ModuleNotFoundError:
            return

        Hovertip(self._timelineButton, self._timelineButton['text'])

    def _create_mdnov(self):
        """Create a mdnovel project from a timeline."""
        timelinePath = filedialog.askopenfilename(
            filetypes=[(TlFile.DESCRIPTION, TlFile.EXTENSION)],
            defaultextension=TlFile.EXTENSION,
            )
        if not timelinePath:
            return

        self._ctrl.close_project()
        root, __ = os.path.splitext(timelinePath)
        novxPath = f'{root}{self._mdl.nvService.get_prj_file_extension()}'
        kwargs = self._get_configuration(timelinePath)
        kwargs['nv_service'] = self._mdl.nvService
        source = TlFile(timelinePath, **kwargs)
        target = self._mdl.nvService.make_prj_file(novxPath)

        if os.path.isfile(target.filePath):
            self._ui.set_status(f'!{_("File already exists")}: "{norm_path(target.filePath)}".')
            return

        message = ''
        try:
            source.novel = self._mdl.nvService.make_novel()
            source.read()
            target.novel = source.novel
            target.write()
        except Error as ex:
            message = f'!{str(ex)}'
        else:
            message = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self._ctrl.open_project(filePath=target.filePath, doNotSave=True)
        finally:
            self._ui.set_status(message)

    def _export_from_mdnov(self):
        """Update or create a timeline from the mdnovel project."""
        if not self._mdl.prjFile:
            return

        self._ui.propertiesView.apply_changes()
        self._ui.restore_status()
        if not self._mdl.prjFile.filePath:
            if not self._ctrl.save_project():
                return

        timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{TlFile.EXTENSION}'
        if os.path.isfile(timelinePath):
            action = _('update')
        else:
            action = _('create')
        if self._mdl.isModified:
            if not self._ui.ask_yes_no(_('Save the project and {} the timeline?').format(action)):
                return

            self._ctrl.save_project()
        elif action == _('update') and not self._ui.ask_yes_no(_('Update the timeline?')):
            return

        kwargs = self._get_configuration(self._mdl.prjFile.filePath)
        kwargs['nv_service'] = self._mdl.nvService
        source = self._mdl.nvService.make_prj_file(self._mdl.prjFile.filePath)
        source.novel = self._mdl.nvService.make_novel()
        target = TlFile(timelinePath, **kwargs)
        target.novel = self._mdl.nvService.make_novel()
        try:
            source.read()
            if os.path.isfile(target.filePath):
                target.read()
            target.write(source.novel)
            message = f'{_("File written")}: "{norm_path(target.filePath)}".'
        except Error as ex:
            message = f'!{str(ex)}'
        self._ui.set_status(message)

    def _get_configuration(self, sourcePath):
        """Return a dictionary with persistent configuration data."""
        sourceDir = os.path.dirname(sourcePath)
        if not sourceDir:
            sourceDir = '.'
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            pluginCnfDir = f'{homeDir}/.mdnovel/config'
        except:
            pluginCnfDir = '.'
        iniFiles = [f'{pluginCnfDir}/timeline.ini', f'{sourceDir}/timeline.ini']
        configuration = self._mdl.nvService.make_configuration(
            settings=self.SETTINGS,
            options=self.OPTIONS
            )
        for iniFile in iniFiles:
            configuration.read(iniFile)
        configData = {}
        configData.update(configuration.settings)
        configData.update(configuration.options)
        return configData

    def _import_to_mdnov(self):
        """Update the mdnovel project from a timeline."""
        if not self._mdl.prjFile:
            return

        self._ui.restore_status()
        self._ui.propertiesView.apply_changes()
        timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{TlFile.EXTENSION}'
        if not os.path.isfile(timelinePath):
            self._ui.set_status(_('!No {} file available for this project.').format(self.APPLICATION))
            return

        if self._mdl.isModified and not self._ui.ask_yes_no(_('Save the project and update it?')):
            return

        self._ctrl.save_project()
        kwargs = self._get_configuration(timelinePath)
        kwargs['nv_service'] = self._mdl.nvService
        source = TlFile(timelinePath, **kwargs)
        target = self._mdl.nvService.make_novx_file(self._mdl.prjFile.filePath, **kwargs)
        message = ''
        try:
            target.novel = self._mdl.nvService.make_novel()
            target.read()
            source.novel = target.novel
            source.read()
            target.novel = source.novel
            target.write()
            message = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self._ctrl.open_project(filePath=self._mdl.prjFile.filePath, doNotSave=True)
        except Error as ex:
            message = f'!{str(ex)}'
        self._ui.set_status(f'{message}')

    def _info(self):
        """Show information about the Timeline file."""
        if not self._mdl.prjFile:
            return

        timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{TlFile.EXTENSION}'
        if os.path.isfile(timelinePath):
            try:
                timestamp = os.path.getmtime(timelinePath)
                if timestamp > self._mdl.prjFile.timestamp:
                    cmp = _('newer')
                else:
                    cmp = _('older')
                fileDate = datetime.fromtimestamp(timestamp).strftime('%c')
                message = _('{0} file is {1} than the mdnovel project.\n (last saved on {2})').format(self.APPLICATION, cmp, fileDate)
            except:
                message = _('Cannot determine file date.')
        else:
            message = _('No {} file available for this project.').format(self.APPLICATION)
        messagebox.showinfo(self.APPLICATION, message)

    def _launch_application(self):
        """Launch Timeline with the current project."""
        if self._mdl.prjFile:
            timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{TlFile.EXTENSION}'
            if os.path.isfile(timelinePath):
                if self.OPTIONS['lock_on_export']:
                    self._ctrl.lock()
                open_document(timelinePath)
            else:
                self._ui.set_status(_('!No {} file available for this project.').format(self.APPLICATION))

