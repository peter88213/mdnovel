"""Provide a class for the mdnovel project file.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
import os

from mdnvlib.mdnov.mdnov_file import MdnovFile
from mdnvlib.novx_globals import CH_ROOT
from mdnvlib.novx_globals import _


class NvWorkFile(MdnovFile):
    """mdnovel project file representation.
    
    Public properties:
        fileDate: str -- Localized file date/time.

    Extends the superclass.
    """
    DESCRIPTION = _('mdnovel project')
    _LOCKFILE_PREFIX = '.LOCK.'
    _LOCKFILE_SUFFIX = '#'

    @property
    def fileDate(self):
        if self.timestamp is None:
            return _('Never')
        else:
            return datetime.fromtimestamp(self.timestamp).strftime('%c')

    def adjust_section_types(self):
        """Make sure the "trash bin" is at the end.
        
        Extends the superclass method.
        """
        super().adjust_section_types()
        for chId in self.novel.tree.get_children(CH_ROOT):
            if self.novel.chapters[chId].isTrash and self.novel.tree.next(chId):
                self.novel.tree.move(chId, CH_ROOT, 'end')
                return

    def has_changed_on_disk(self):
        """Return True if the yw project file has changed since last opened."""
        try:
            if self.timestamp != os.path.getmtime(self.filePath):
                return True
            else:
                return False

        except:
            # this is for newly created projects
            return False

    def _split_file_path(self):
        head, tail = os.path.split(self.filePath)
        if head:
            head = f'{head}/'
        else:
            head = './'
        return head, tail

