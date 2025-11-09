"""Provide a class for csv section list export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.csv.csv_file import CsvFile
from mdnvlib.model.section import Section
from mdnvlib.novx_globals import SECTIONLIST_SUFFIX
from mdnvlib.novx_globals import _


class CsvSectionList(CsvFile):
    """csv section list writer."""

    DESCRIPTION = _('Section list')
    SUFFIX = SECTIONLIST_SUFFIX

    def _get_sectionMapping(self, scId, sectionNumber, wordsTotal, **kwargs):
        """Return a mapping dictionary for a section section.
        
        Positional arguments:
            scId: str -- section ID.
            sectionNumber: int -- section number to be displayed.
            wordsTotal: int -- accumulated wordcount.
        
        Extends the superclass method.
        """
        sectionMapping = super()._get_sectionMapping(scId, sectionNumber, wordsTotal)
        sectionMapping['Status'] = Section.STATUS[sectionMapping['Status']]
        return sectionMapping

    def _get_header_columns(self):
        """Return a list with all column records of a headline.
        
        Overrides the superclass method
        """
        pltPrgs, chrczn, wrldbld, goal, cflct, outcm, chrBio, chrGls = self._get_renamings()
        columns = []
        columns.append('ID')
        columns.append(_("Section"))
        columns.append(_("Title"))
        columns.append(_("Description"))
        columns.append(_("Viewpoint"))
        columns.append(_("Date"))
        columns.append(_("Time"))
        columns.append(_("Day"))
        columns.append(_("Duration"))
        columns.append(_("Tags"))
        columns.append(_("Notes"))
        columns.append(_("Scene"))
        columns.append(f'{_("Goal")} / {_("Reaction")} / {goal}')
        columns.append(f'{chrczn} / {_("Conflict")} / {_("Dilemma")} / {cflct}')
        columns.append(f'{wrldbld} / {_("Outcome")} / {_("Choice")} / {outcm}')
        columns.append(_("Status"))
        columns.append(_("Words total"))
        columns.append(_("Word count"))
        columns.append(_("Characters"))
        columns.append(_("Locations"))
        columns.append(_("Items"))
        return columns

    def _get_section_columns(self, scId, scNumber, wordsTotal):
        """Return a list with all column records of a section row.
        
        Overrides the superclass method
        """
        columns = []
        mapping = self._get_sectionMapping(scId, scNumber, wordsTotal)
        columns.append(mapping['ID'])
        columns.append(mapping['SectionNumber'])
        columns.append(mapping['Title'])
        columns.append(mapping['Desc'])
        columns.append(mapping['Viewpoint'])
        columns.append(mapping['Date'])
        columns.append(mapping['Time'])
        columns.append(mapping['Day'])
        columns.append(mapping['Duration'])
        columns.append(mapping['Tags'])
        columns.append(mapping['Notes'])
        columns.append(mapping['Scene'])
        columns.append(mapping['Goal'])
        columns.append(mapping['Conflict'])
        columns.append(mapping['Outcome'])
        columns.append(mapping['Status'])
        columns.append(mapping['WordsTotal'])
        columns.append(mapping['WordCount'])
        columns.append(mapping['Characters'])
        columns.append(mapping['Locations'])
        columns.append(mapping['Items'])
        return columns

    def _get_text(self):
        return self._get_sections()

