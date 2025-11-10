"""Provide a base class for mdnovel project files.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date
import os

from mdnvlib.file.file import File
from mdnvlib.novx_globals import CH_ROOT
from mdnvlib.novx_globals import Error
from mdnvlib.novx_globals import _


class PrjFile(File):
    """Project file representation.

    Public instance variables:
        wcLog: dict[str, list[str, str]] -- Daily word count logs.
        wcLogUpdate: dict[str, list[str, str]] -- Word counts missing in the log.
        timestamp: float -- Time of last file modification (number of seconds since the epoch).
    
    
    """
    DESCRIPTION = _('mdnovel project')
    SUFFIX = ''

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.
        
        Positional arguments:
            filePath: str -- path to the mdnov file.
            
        Optional arguments:
            kwargs -- keyword arguments (not used here).            
        
        Extends the superclass constructor.
        """
        super().__init__(filePath)
        self.on_element_change = None

        self.wcLog = {}
        # key: str -- date (iso formatted)
        # value: list -- [word count: str, with unused: str]

        self.wcLogUpdate = {}
        # key: str -- date (iso formatted)
        # value: list -- [word count: str, with unused: str]

        self.timestamp = None

    def adjust_section_types(self):
        """Make sure that nodes with "Unused" parents inherit the type."""
        partType = 0
        for chId in self.novel.tree.get_children(CH_ROOT):
            if self.novel.chapters[chId].chLevel == 1:
                partType = self.novel.chapters[chId].chType
            elif partType != 0 and not self.novel.chapters[chId].isTrash:
                self.novel.chapters[chId].chType = partType
            for scId in self.novel.tree.get_children(chId):
                if self.novel.sections[scId].scType < self.novel.chapters[chId].chType:
                    self.novel.sections[scId].scType = self.novel.chapters[chId].chType

    def _check_id(self, elemId, elemPrefix):
        """Raise an exception if elemId does not start with the correct prefix."""
        if not elemId.startswith(elemPrefix):
            raise Error(f"bad ID: '{elemId}'")

    def count_words(self):
        """Return a tuple of word count totals.
        
        count: int -- Total words of "normal" type sections.
        totalCount: int -- Total words of "normal" and "unused" sections.
        """
        count = 0
        totalCount = 0
        for chId in self.novel.tree.get_children(CH_ROOT):
            if not self.novel.chapters[chId].isTrash:
                for scId in self.novel.tree.get_children(chId):
                    if self.novel.sections[scId].scType < 2:
                        totalCount += self.novel.sections[scId].wordCount
                        if self.novel.sections[scId].scType == 0:
                            count += self.novel.sections[scId].wordCount
        return count, totalCount

    def _get_timestamp(self):
        try:
            self.timestamp = os.path.getmtime(self.filePath)
        except:
            self.timestamp = None

    def _keep_word_count(self):
        """Keep the actual wordcount, if not logged."""
        if not self.wcLog:
            return

        actualCount, actualTotalCount = self.count_words()
        latestDate = list(self.wcLog)[-1]
        latestCount = self.wcLog[latestDate][0]
        latestTotalCount = self.wcLog[latestDate][1]
        if actualCount != latestCount or actualTotalCount != latestTotalCount:
            try:
                fileDateIso = date.fromtimestamp(self.timestamp).isoformat()
            except:
                fileDateIso = date.today().isoformat()
            self.wcLogUpdate[fileDateIso] = [actualCount, actualTotalCount]

    def _update_word_count_log(self):
        """Add today's word count and word count when reading, if not logged."""
        if self.novel.saveWordCount:
            newCount, newTotalCount = self.count_words()
            todayIso = date.today().isoformat()
            self.wcLogUpdate[todayIso] = [newCount, newTotalCount]
            for wcDate in self.wcLogUpdate:
                self.wcLog[wcDate] = self.wcLogUpdate[wcDate]
        self.wcLogUpdate = {}

