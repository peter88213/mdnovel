"""Provide a class for Markdown section descriptions export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.md.md_file import MdFile
from mdnvlib.novx_globals import SECTIONS_SUFFIX
from mdnvlib.novx_globals import _


class MdSectionDesc(MdFile):
    """Markdown section summaries file writer.

    Export a full synopsis with section descriptions.
    """
    DESCRIPTION = _('Section descriptions')
    SUFFIX = SECTIONS_SUFFIX

    _partTemplate = '\n# ${Title}\n\n'
    _chapterTemplate = '\n## ${Title}\n\n'
    _sectionTemplate = '${Desc}\n\n'
    _sectionDivider = f'{MdFile.SECTION_DIVIDER}\n\n'

    def _get_sectionMapping(self, scId, sectionNumber, wordsTotal, **kwargs):
        """Return a mapping dictionary for a section section.
        
        Positional arguments:
            scId: str -- section ID.
            sectionNumber: int -- section number to be displayed.
            wordsTotal: int -- accumulated wordcount.
        
        Extends the superclass method.
        """
        sectionMapping = super()._get_sectionMapping(scId, sectionNumber, wordsTotal, **kwargs)
        sectionMapping['Manuscript'] = _('Manuscript')
        return sectionMapping
