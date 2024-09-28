"""Provide a class for Markdown story structure export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.md.md_file import MdFile
from mdnvlib.novx_globals import STAGES_SUFFIX
from mdnvlib.novx_globals import _


class MdStages(MdFile):
    """Markdown story structure file representation.

    Export a plot description with story structure and arcs.
    """
    DESCRIPTION = _('Story structure')
    SUFFIX = STAGES_SUFFIX

    _fileHeader = f''

    _stage1Template = '''<text:h text:style-name="Heading_20_1" text:outline-level="1"><text:bookmark text:name="$ID"/>$Title
<text:section text:style-name="Sect1" text:name="$ID">
$Desc
</text:section>
'''

    _stage2Template = '''## <text:bookmark text:name="$ID"/>$Title
<text:section text:style-name="Sect1" text:name="$ID">
$Desc
</text:section>
'''

