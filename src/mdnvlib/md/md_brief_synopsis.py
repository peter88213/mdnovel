"""Provide a class for Markdown brief synopsis export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.novx_globals import BRF_SYNOPSIS_SUFFIX
from mdnvlib.novx_globals import _
from mdnvlib.md.md_file import MdFile


class MdBriefSynopsis(MdFile):
    """Markdown brief synopsis file writer.

    Export a brief synopsis with chapter titles and section titles.
    """
    DESCRIPTION = _('Brief synopsis')
    SUFFIX = BRF_SYNOPSIS_SUFFIX

    _partTemplate = '\n# ${Title}\n\n'
    _chapterTemplate = '\n## ${Title}\n\n'
    _sectionTemplate = '${Title}\n\n'
