"""Provide a class for csv file representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import csv
import os

from mdnvlib.file.file_export import FileExport
from mdnvlib.novx_globals import CH_ROOT
from mdnvlib.novx_globals import CR_ROOT
from mdnvlib.novx_globals import LC_ROOT
from mdnvlib.novx_globals import IT_ROOT
from mdnvlib.novx_globals import PL_ROOT
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

    def _get_character_columns(self, crId):
        """Return a list with all column records of a character row."""
        return []

    def _get_characters(self):
        """Return a list with a row per character."""
        csvRows = [self._get_header_columns()]
        for crId in self.novel.tree.get_children(CR_ROOT):
            csvColumns = self._get_character_columns(crId)
            csvRows.append(csvColumns)
        return csvRows

    def _get_chapter_columns(self, chId, chNumber):
        """Return a list with all column records of a chapter row."""
        return []

    def _get_chapters(self):
        """Return a list with a row per chapter."""
        csvRows = [self._get_header_columns()]
        chNumber = 0
        for chId in self.novel.tree.get_children(CH_ROOT):
            if self.novel.chapters[chId].chType > 0:
                continue

                chNumber += 1
                csvColumns = self._get_chapter_columns(chId, chNumber)
                csvRows.append(csvColumns)
        return csvRows

    def _get_header_columns(self):
        """Return a list with all column records of a headline."""
        return []

    def _get_item_columns(self, ItId):
        """Return a list with all column records of an item row."""
        return []

    def _get_items(self):
        """Return a list with a row per item."""
        csvRows = [self._get_header_columns()]
        for ItId in self.novel.tree.get_children(IT_ROOT):
            csvColumns = self._get_item_columns(ItId)
            csvRows.append(csvColumns)
        return csvRows

    def _get_location_columns(self, lcId):
        """Return a list with all column records of a location row."""
        return []

    def _get_locations(self):
        """Return a list with a row per location."""
        csvRows = [self._get_header_columns()]
        for lcId in self.novel.tree.get_children(LC_ROOT):
            csvColumns = self._get_location_columns(lcId)
            csvRows.append(csvColumns)
        return csvRows

    def _get_plotline_columns(self, plId):
        """Return a list with all column records of a plotline row."""
        return []

    def _get_plotlines(self):
        """Return a list with a row per plotline."""
        csvRows = [self._get_header_columns()]
        for plId in self.novel.tree.get_children(PL_ROOT):
            csvColumns = self._get_plotline_columns(plId)
            csvRows.append(csvColumns)
        return csvRows

    def _get_section_columns(self, scId, scNumber, wordsTotal):
        """Return a list with all column records of a section row."""
        return []

    def _get_sections(self):
        """Return a list with a row per section."""
        csvRows = [self._get_header_columns()]
        scNumber = 0
        wordsTotal = 0
        for chId in self.novel.tree.get_children(CH_ROOT):
            for scId in self.novel.tree.get_children(chId):
                if self.novel.sections[scId].scType > 0:
                    continue

                scNumber += 1
                wordsTotal += self.novel.sections[scId].wordCount
                csvColumns = self._get_section_columns(scId, scNumber, wordsTotal)
                csvRows.append(csvColumns)
        return csvRows

