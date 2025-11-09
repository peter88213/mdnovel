"""Provide a class for Markdown chapter descriptions export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.md.md_file import MdFile
from mdnvlib.novx_globals import CHAPTERS_SUFFIX
from mdnvlib.novx_globals import _


class MdChapterDesc(MdFile):
    """Markdown chapter summaries file writer.

    Export a synopsis with chapter descriptions.
    """
    DESCRIPTION = _('Chapter descriptions')
    SUFFIX = CHAPTERS_SUFFIX

    _partTemplate = '\n# ${Title}\n\n'
    _chapterTemplate = '## ${Title}\n\n$Desc\n\n'

