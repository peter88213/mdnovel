"""Provide a class for csv plot grid export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import csv

from string import Template

from mdnvlib.csv.csv_file import CsvFile
from mdnvlib.novx_globals import GRID_SUFFIX
from mdnvlib.novx_globals import PLOTLINES_SUFFIX
from mdnvlib.novx_globals import PL_ROOT
from mdnvlib.novx_globals import CH_ROOT
from mdnvlib.novx_globals import _


class CsvGrid(CsvFile):
    """csv plot grid writer."""

    DESCRIPTION = _('Plot grid')
    SUFFIX = GRID_SUFFIX

    def _get_header_columns(self):
        pltPrgs, chrczn, wrldbld, goal, cflct, outcm, chrBio, chrGls = self._get_renamings()
        columns = []
        columns.append(_("Section"))
        columns.append(_("Date"))
        columns.append(_("Time"))
        columns.append(_("Day"))
        columns.append(_("Title"))
        columns.append(_("Description"))
        columns.append(_("Viewpoint"))
        for plId in self.novel.tree.get_children(PL_ROOT):
            columns.append(self.novel.plotLines[plId].title)
        columns.append(_("Tags"))
        columns.append(_("Scene"))
        columns.append(f'{_("Goal")} / {_("Reaction")} / {goal}')
        columns.append(f'{chrczn} / {_("Conflict")} / {_("Dilemma")} / {cflct}')
        columns.append(f'{wrldbld} / {_("Outcome")} / {_("Choice")} / {outcm}')
        columns.append(_("Notes"))
        return columns

    def _get_section_columns(self, scId, scNumber):
        columns = []
        mapping = self._get_sectionMapping(scId, scNumber, 0)
        columns.append(mapping['SectionNumber'])
        columns.append(mapping['Date'])
        columns.append(mapping['Time'])
        columns.append(mapping['Day'])
        columns.append(mapping['Title'])
        columns.append(mapping['Desc'])
        columns.append(mapping['Viewpoint'])

        section = self.novel.sections[scId]
        for plId in self.novel.tree.get_children(PL_ROOT):
            plotlineNotes = section.plotlineNotes
            if plotlineNotes:
                arcNote = plotlineNotes.get(plId, '')
            else:
                arcNote = ''
            columns.append(arcNote)

        columns.append(mapping['Tags'])
        columns.append(mapping['Scene'])
        columns.append(mapping['Goal'])
        columns.append(mapping['Conflict'])
        columns.append(mapping['Outcome'])
        columns.append(mapping['Notes'])
        return columns

    def _get_text(self):
        csvRows = [self._get_header_columns()]
        scNumber = 0
        for chId in self.novel.tree.get_children(CH_ROOT):
            for scId in self.novel.tree.get_children(chId):
                if self.novel.sections[scId].scType > 0:
                    continue

                scNumber += 1
                csvColumns = self._get_section_columns(scId, scNumber)
                csvRows.append(csvColumns)
        return csvRows

