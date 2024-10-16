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

    def _get_header_columns(self):
        """Return a list with all column records of a headline.
        
        Overrides the superclass method
        """
        pltPrgs, chrczn, wrldbld, goal, cflct, outcm, chrBio, chrGls = self._get_renamings()
        columns = []
        columns.append('ID')
        columns.append(_("Title"))
        columns.append(_("Aka"))
        columns.append(_("Description"))
        columns.append(_("Tags"))
        columns.append(_("Notes"))
        return columns

    def _get_item_columns(self, crId):
        """Return a list with all column records of a charcter row.
        
        Overrides the superclass method
        """
        columns = []
        mapping = self._get_itemMapping(crId)
        columns.append(mapping['ID'])
        columns.append(mapping['Title'])
        columns.append(mapping['AKA'])
        columns.append(mapping['Desc'])
        columns.append(mapping['Tags'])
        columns.append(mapping['Notes'])
        return columns

    def _get_text(self):
        return self._get_items()

