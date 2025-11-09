"""Provide a class for csv character list export.

Copyright (c) 2025 Peter Triesberger
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

    def _get_header_columns(self):
        """Return a list with all column records of a headline.
        
        Overrides the superclass method
        """
        pltPrgs, chrczn, wrldbld, goal, cflct, outcm, chrBio, chrGls = self._get_renamings()
        columns = []
        columns.append('ID')
        columns.append(_("Title"))
        columns.append(_("Full name"))
        columns.append(_("Aka"))
        columns.append(_("Description"))
        columns.append(chrBio)
        columns.append(chrGls)
        columns.append(_("Status"))
        columns.append(_("Tags"))
        columns.append(_("Notes"))
        return columns

    def _get_character_columns(self, crId):
        """Return a list with all column records of a charcter row.
        
        Overrides the superclass method
        """
        columns = []
        mapping = self._get_characterMapping(crId)
        columns.append(mapping['ID'])
        columns.append(mapping['Title'])
        columns.append(mapping['FullName'])
        columns.append(mapping['AKA'])
        columns.append(mapping['Desc'])
        columns.append(mapping['Bio'])
        columns.append(mapping['Goals'])
        columns.append(mapping['Status'])
        columns.append(mapping['Tags'])
        columns.append(mapping['Notes'])
        return columns

    def _get_text(self):
        return self._get_characters()

