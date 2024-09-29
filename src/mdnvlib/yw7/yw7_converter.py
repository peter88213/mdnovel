"""yw7 file import/export for mdnovel.

Requires Python 3.6+
Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from tkinter import filedialog

from mdnvlib.novx_globals import _
from mdnvlib.novx_globals import norm_path
from mdnvlib.yw7.yw7_file import Yw7File


class Yw7Converter:
    """yw7 file import/export class."""

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
        self._ui.newMenu.add_command(label=_('Create from yw7...'), command=self._import_yw7)

        # Add an entry to the "Export" menu.
        self._ui.exportMenu.insert_command(_('Options'), label=_('yw7 project'), command=self._export_yw7)
        self._ui.exportMenu.insert_separator(_('Options'))

    def _export_yw7(self):
        """Export the current project to yw7.
        
        Return True on success, otherwise return False.
        """
        if self._mdl.prjFile.filePath is None:
            return False

        path, __ = os.path.splitext(self._mdl.prjFile.filePath)
        yw7Path = f'{path}{Yw7File.EXTENSION}'
        if os.path.isfile(yw7Path):
            if not self._ui.ask_yes_no(_('Overwrite existing file "{}"?').format(norm_path(yw7Path))):
                self._ui.set_status(f'!{_("Action canceled by user")}.')
                return False

        self._ui.restore_status()
        self._ui.propertiesView.apply_changes()
        yw7File = Yw7File(yw7Path, nv_service=self._mdl.nvService)
        yw7File.novel = self._mdl.novel
        yw7File.wcLog = self._mdl.prjFile.wcLog
        try:
            yw7File.write()
        except TypeError as ex:
            self._ui.set_status(f'!{str(ex)}')
            return False

        self._ui.set_status(f'{_("File exported")}: {yw7Path}')
        return True

    def _import_yw7(self, yw7Path=''):
        """Convert a yw7 file to novx and open the novx file.
        
        Return True on success, otherwise return False.
        """
        self._ui.restore_status()
        initDir = os.path.dirname(self._prefs.get('last_open', ''))
        if not initDir:
            initDir = './'
        if not yw7Path or not os.path.isfile(yw7Path):
            fileTypes = [(Yw7File.DESCRIPTION, Yw7File.EXTENSION)]
            yw7Path = filedialog.askopenfilename(
                filetypes=fileTypes,
                defaultextension=Yw7File.EXTENSION,
                initialdir=initDir
                )
        if not yw7Path:
            return False

        try:
            filePath, extension = os.path.splitext(yw7Path)
            if extension == Yw7File.EXTENSION:
                novxPath = f'{filePath}{self._mdl.nvService.get_novx_file_extension()}'
                if os.path.isfile(novxPath):
                    if not self._ui.ask_yes_no(_('Overwrite existing file "{}"?').format(norm_path(novxPath))):
                        self._ui.set_status(f'!{_("Action canceled by user")}.')
                        return False

                self._ctrl.close_project()
                yw7File = Yw7File(yw7Path, nv_service=self._mdl.nvService)
                yw7File.novel = self._mdl.nvService.make_novel()
                yw7File.read()
                novxFile = self._mdl.nvService.make_mdnov_file(novxPath, nv_service=self._mdl.nvService)
                novxFile.novel = yw7File.novel
                novxFile.wcLog = yw7File.wcLog
                novxFile.write()
            else:
                self._ui.set_status(f'!{_("File type is not supported")}.')
                return False

        except Exception as ex:
            self._ui.set_status(f'!{str(ex)}')
            return False

        self._ctrl.open_project(filePath=novxFile.filePath)
        self._ui.set_status(f'{_("File imported")}: {yw7Path}')
        return True

