"""Provide a converter class for test_mdnovel.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv-timeline
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os

from mdnvlib.converter.converter import Converter
from mdnvlib.novx_globals import Error
from mdnvlib.novx_globals import norm_path
from mdnvlib.model.nv_service import NvService
from mdnvlib.novx_globals import _
from mdnvlib.timeline.tl_file import TlFile


class TlConverter(Converter):
    """A converter class for mdnovel and Timeline."""

    def run(self, sourcePath, **kwargs):
        """Create source and target objects and run conversion.

        Positional arguments: 
            sourcePath: str -- the source file path.

        The direction of the conversion is determined by the source file type.
        Only mdnovel project files and Timeline files are accepted.
        """
        nvService = NvService()
        kwargs['nv_service'] = nvService
        self.newFile = None
        if not os.path.isfile(sourcePath):
            self.ui.set_status(f'!{_("File not found")}: "{norm_path(sourcePath)}".')
            return

        fileName, fileExtension = os.path.splitext(sourcePath)
        if fileExtension == TlFile.EXTENSION:
            # Source is a timeline
            sourceFile = TlFile(sourcePath, **kwargs)
            targetFile = nvService.make_novx_file(f'{fileName}{nvService.get_novx_file_extension()}', **kwargs)
            if os.path.isfile(f'{fileName}{nvService.get_novx_file_extension()}'):
                # Update existing mdnovel project from timeline
                self.import_to_novx(sourceFile, targetFile)
            else:
                # Create new mdnovel project from timeline
                self.create_novx(sourceFile, targetFile)
        elif fileExtension == nvService.get_novx_file_extension():
            # Update existing timeline from mdnovel project
            sourceFile = nvService.make_novx_file(sourcePath, **kwargs)
            targetFile = TlFile(f'{fileName}{TlFile.EXTENSION}', **kwargs)
            self.export_from_novx(sourceFile, targetFile)
        else:
            # Source file format is not supported
            self.ui.set_status(f'!{_("File type is not supported")}: "{norm_path(sourcePath)}".')

    def export_from_novx(self, source, target):
        """Convert from mdnovel project to other file format.

        Positional arguments:
            source -- NovxFile subclass instance.
            target -- Any Novel subclass instance.

        Operation:
        1. Send specific information about the conversion to the UI.
        2. Convert source into target.
        3. Pass the message to the UI.
        4. Save the new file pathname.

        Error handling:
        - If the conversion fails, newFile is set to None.
        
        Overrides the superclass method.
        """
        nvService = NvService()
        self.ui.set_info(
            _('Input: {0} "{1}"\nOutput: {2} "{3}"').format(source.DESCRIPTION, norm_path(source.filePath), target.DESCRIPTION, norm_path(target.filePath)))
        message = ''
        try:
            self.check(source, target)
            source.novel = nvService.make_novel()
            target.novel = nvService.make_novel()
            source.read()
            if os.path.isfile(target.filePath):
                target.read()
            target.write(source.novel)
        except Error as ex:
            message = f'!{str(ex)}'
            self.newFile = None
        else:
            message = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self.newFile = target.filePath
        finally:
            self.ui.set_status(message)

