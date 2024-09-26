"""Provide a class for csv file representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.novx_globals import CHARLIST_SUFFIX
from mdnvlib.file.file_export import FileExport


class CsvFile(FileExport):
    """csv file representation."""

    EXTENSION = '.csv'
    SUFFIX = CHARLIST_SUFFIX

