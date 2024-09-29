"""novx file import/export for mdnovel.

Requires Python 3.6+
Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from tkinter import filedialog

from mdnvlib.novx_globals import _
from mdnvlib.novx_globals import norm_path
from mdnvlib.novx.novx_file import NovxFile


class NovxConverter:
    """novx file import/export class."""

    def __init__(self, model, view, controller, prefs=None):
        """Add commands to the view.
        
        Positional arguments:
            model -- reference to the main model instance of the application.
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.

        Optional arguments:
            prefs -- deprecated. Please use controller.get_preferences() instead.
        
        Overrides the superclass method.
       """
        self._mdl = model
        self._ui = view
        self._ctrl = controller
        self._prefs = controller.get_preferences()

        # Add an entry to the "File > New" menu.
        self._ui.newMenu.add_command(label=_('Create from novx...'), command=self._import_novx)

        # Add an entry to the "Export" menu.
        self._ui.exportMenu.insert_command(_('Options'), label=NovxFile.DESCRIPTION, command=self._export_novx)
        self._ui.exportMenu.insert_separator(_('Options'))

    def _export_novx(self):
        """Export the current project to novx.
        
        Return True on success, otherwise return False.
        """
        if self._mdl.prjFile.filePath is None:
            return False

        path, __ = os.path.splitext(self._mdl.prjFile.filePath)
        novxPath = f'{path}{NovxFile.EXTENSION}'
        if os.path.isfile(novxPath):
            if not self._ui.ask_yes_no(_('Overwrite existing file "{}"?').format(norm_path(novxPath))):
                self._ui.set_status(f'!{_("Action canceled by user")}.')
                return False

        self._ui.restore_status()
        self._ui.propertiesView.apply_changes()
        novxFile = NovxFile(novxPath, nv_service=self._mdl.nvService)
        novxFile.novel = self._mdl.novel
        novxFile.wcLog = self._mdl.prjFile.wcLog
        try:
            novxFile.write()
        except TypeError as ex:
            self._ui.set_status(f'!{str(ex)}')
            return False

        self._ui.set_status(f'{_("File exported")}: {novxPath}')
        return True

    def _import_novx(self, novxPath=''):
        """Convert a novx file to novx and open the novx file.
        
        Return True on success, otherwise return False.
        """
        self._ui.restore_status()
        initDir = os.path.dirname(self._prefs.get('last_open', ''))
        if not initDir:
            initDir = './'
        if not novxPath or not os.path.isfile(novxPath):
            fileTypes = [(NovxFile.DESCRIPTION, NovxFile.EXTENSION)]
            novxPath = filedialog.askopenfilename(
                filetypes=fileTypes,
                defaultextension=NovxFile.EXTENSION,
                initialdir=initDir
                )
        if not novxPath:
            return False

        try:
            filePath, extension = os.path.splitext(novxPath)
            if extension == NovxFile.EXTENSION:
                mdnovPath = f'{filePath}{self._mdl.nvService.get_novx_file_extension()}'
                if os.path.isfile(mdnovPath):
                    if not self._ui.ask_yes_no(_('Overwrite existing file "{}"?').format(norm_path(mdnovPath))):
                        self._ui.set_status(f'!{_("Action canceled by user")}.')
                        return False

                self._ctrl.close_project()
                novxFile = NovxFile(novxPath, nv_service=self._mdl.nvService)
                novxFile.novel = self._mdl.nvService.make_novel()
                novxFile.read()
                mdnovFile = self._mdl.nvService.make_mdnov_file(mdnovPath, nv_service=self._mdl.nvService)
                mdnovFile.novel = novxFile.novel
                mdnovFile.wcLog = novxFile.wcLog
                mdnovFile.write()
            else:
                self._ui.set_status(f'!{_("File type is not supported")}.')
                return False

        except Exception as ex:
            self._ui.set_status(f'!{str(ex)}')
            return False

        self._ctrl.open_project(filePath=mdnovFile.filePath)
        self._ui.set_status(f'{_("File imported")}: {mdnovPath}')
        return True

