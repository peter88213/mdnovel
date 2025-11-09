"""Provide a class for Novel file conversion with file factories.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os

from mdnvlib.converter.converter import Converter
from mdnvlib.converter.export_source_factory import ExportSourceFactory
from mdnvlib.converter.export_target_factory import ExportTargetFactory
from mdnvlib.converter.import_source_factory import ImportSourceFactory
from mdnvlib.converter.import_target_factory import ImportTargetFactory
from mdnvlib.novx_globals import Error
from mdnvlib.novx_globals import _
from mdnvlib.novx_globals import norm_path


class ConverterFf(Converter):
    """Class for Novel file conversion using factory methods to create target and source classes.

    Class constants:
        EXPORT_SOURCE_CLASSES -- list of NovxFile subclasses from which can be exported.
        EXPORT_TARGET_CLASSES -- list of FileExport subclasses to which export is possible.
        IMPORT_SOURCE_CLASSES -- list of File subclasses from which can be imported.
        IMPORT_TARGET_CLASSES -- list of NovxFile subclasses to which import is possible.

    All lists are empty and meant to be overridden by subclasses.

    Instance variables:
        exportSourceFactory: ExportSourceFactory.
        exportTargetFactory: ExportTargetFactory.
        importSourceFactory: ImportSourceFactory.
        importTargetFactory: ImportTargetFactory.
        newProjectFactory: FileFactory (to be overridden by subclasses).
    """
    EXPORT_SOURCE_CLASSES = []
    EXPORT_TARGET_CLASSES = []
    IMPORT_SOURCE_CLASSES = []
    IMPORT_TARGET_CLASSES = []

    def __init__(self):
        """Create strategy class instances.
        
        Extends the superclass constructor.
        """
        super().__init__()
        self.exportSourceFactory = ExportSourceFactory(self.EXPORT_SOURCE_CLASSES)
        self.exportTargetFactory = ExportTargetFactory(self.EXPORT_TARGET_CLASSES)
        self.importSourceFactory = ImportSourceFactory(self.IMPORT_SOURCE_CLASSES)
        self.importTargetFactory = ImportTargetFactory(self.IMPORT_TARGET_CLASSES)
        self.newProjectFactory = None

    def run(self, sourcePath, **kwargs):
        """Create source and target objects and run conversion.

        Positional arguments: 
            sourcePath: str -- the source file path.
        
        Required keyword arguments: 
            suffix: str -- target file name suffix.

        This is a template method that calls superclass methods as primitive operations by case.
        """
        self.newFile = None
        if not os.path.isfile(sourcePath):
            self.ui.set_status(f'!{_("File not found")}: "{norm_path(sourcePath)}".')
            return

        try:
            source, __ = self.exportSourceFactory.make_file_objects(sourcePath, **kwargs)
        except Error:
            # The source file is not a mdnovel project.
            try:
                source, __ = self.importSourceFactory.make_file_objects(sourcePath, **kwargs)
            except Error:
                # A new mdnovel project might be required.
                try:
                    source, target = self.newProjectFactory.make_file_objects(sourcePath, **kwargs)
                except Error as ex:
                    self.ui.set_status(f'!{str(ex)}')
                else:
                    self.create_mdnov(source, target)
            else:
                # Try to update an existing mdnovel project.
                kwargs['suffix'] = source.SUFFIX
                try:
                    __, target = self.importTargetFactory.make_file_objects(sourcePath, **kwargs)
                except Error as ex:
                    self.ui.set_status(f'!{str(ex)}')
                else:
                    self.import_to_mdnov(source, target)
        else:
            # The source file is a mdnovel project.
            try:
                __, target = self.exportTargetFactory.make_file_objects(sourcePath, **kwargs)
            except Error as ex:
                self.ui.set_status(f'!{str(ex)}')
            else:
                self.export_from_mdnov(source, target)
