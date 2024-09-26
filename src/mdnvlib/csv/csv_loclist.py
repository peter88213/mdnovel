"""Provide a class for csv location list export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.csv.csv_file import CsvFile
from mdnvlib.novx_globals import LOCLIST_SUFFIX
from mdnvlib.novx_globals import _


class CsvLocList(CsvFile):
    """csv location list writer."""
    DESCRIPTION = _('Location list')
    SUFFIX = LOCLIST_SUFFIX

    _fileHeader = f''
    _locationTemplate = ''
