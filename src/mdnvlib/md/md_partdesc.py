"""Provide a class for Markdown part descriptions export.

Parts are chapters marked `This chapter  begins a new section` in novelibre.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.md.md_file import MdFile
from mdnvlib.novx_globals import PARTS_SUFFIX
from mdnvlib.novx_globals import _


class MdPartDesc(MdFile):
    """Markdown part summaries file writer.

    Export a synopsis with part descriptions.
    """
    DESCRIPTION = _('Part descriptions')
    SUFFIX = PARTS_SUFFIX

    _fileHeader = f''

    _partTemplate = '''<text:section text:style-name="Sect1" text:name="$ID">
<text:h text:style-name="Heading_20_1" text:outline-level="1"><text:a xlink:href="../$ProjectName$ManuscriptSuffix.odt#$Title|outline">$Title</text:a></text:h>
$Desc
</text:section>
'''

