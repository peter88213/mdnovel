"""Provide a class for Markdown brief synopsis export.

Copyright (c) 2024 Peter Triesberger
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

    _fileHeader = f''

    _partTemplate = '''<text:h text:style-name="Heading_20_1" text:outline-level="1">$Title</text:h>
'''

    _chapterTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">$Title</text:h>
'''

    _sectionTemplate = '''<text:p text:style-name="Text_20_body">$Title</text:p>
'''

