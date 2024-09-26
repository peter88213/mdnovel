"""Provide a class for csv character list export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from mdnvlib.csv.csv_file import CsvFile
from mdnvlib.novx_globals import CHARLIST_SUFFIX
from mdnvlib.novx_globals import _


class CsvCharList(CsvFile):
    """csv character list writer."""

    DESCRIPTION = _('Character list')
    SUFFIX = CHARLIST_SUFFIX

    _fileHeader = ''
    _characterTemplate = ''

