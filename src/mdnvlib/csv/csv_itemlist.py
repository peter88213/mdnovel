"""Provide a class for csv item list export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.csv.csv_file import CsvFile
from mdnvlib.novx_globals import ITEMLIST_SUFFIX
from mdnvlib.novx_globals import _


class CsvItemList(CsvFile):
    """csv item list writer."""

    DESCRIPTION = _('Item list')
    SUFFIX = ITEMLIST_SUFFIX

    _fileHeader = ''
    _itemTemplate = ''

