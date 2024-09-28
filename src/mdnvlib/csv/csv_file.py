"""Provide a class for csv file representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import csv
import os

from mdnvlib.file.file_export import FileExport
from mdnvlib.novx_globals import Error
from mdnvlib.novx_globals import _
from mdnvlib.novx_globals import norm_path


class CsvFile(FileExport):
    """csv file representation."""

    EXTENSION = '.csv'

    def write(self):
        """Write instance variables to the export file.
        
        Create a template-based output file. 
        Return a message in case of success.
        Raise the "Error" exception in case of error. 
        """
        csvRows = self._get_text()
        backedUp = False
        if os.path.isfile(self.filePath):
            try:
                os.replace(self.filePath, f'{self.filePath}.bak')
            except:
                raise Error(f'{_("Cannot overwrite file")}: "{norm_path(self.filePath)}".')
            else:
                backedUp = True
        try:
            with open(self.filePath, 'w', encoding='utf-8', newline='') as f:
                csvWriter = csv.writer(f, dialect='excel')
                for row in csvRows:
                    csvWriter.writerow(row)
        except:
            if backedUp:
                os.replace(f'{self.filePath}.bak', self.filePath)
            raise Error(f'{_("Cannot write file")}: "{norm_path(self.filePath)}".')

