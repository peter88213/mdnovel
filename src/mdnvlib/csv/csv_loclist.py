"""Provide a class for csv location list export.

Copyright (c) 2025 Peter Triesberger
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

    def _get_location_columns(self, crId):
        """Return a list with all column records of a charcter row.
        
        Overrides the superclass method
        """
        columns = []
        mapping = self._get_locationMapping(crId)
        columns.append(mapping['ID'])
        columns.append(mapping['Title'])
        columns.append(mapping['AKA'])
        columns.append(mapping['Desc'])
        columns.append(mapping['Tags'])
        columns.append(mapping['Notes'])
        return columns

    def _get_text(self):
        return self._get_locations()

