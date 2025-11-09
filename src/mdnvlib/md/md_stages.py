"""Provide a class for Markdown story structure export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.md.md_file import MdFile
from mdnvlib.novx_globals import STAGES_SUFFIX
from mdnvlib.novx_globals import _


class MdStages(MdFile):
    """Markdown story structure file representation.

    Export a story structure description with stages.
    """
    DESCRIPTION = _('Story structure')
    SUFFIX = STAGES_SUFFIX

    _fileHeader = f'{MdFile._fileHeader}# {DESCRIPTION}\n\n'

    _stage1Template = '\n## $Title\n\n$Desc\n\n'
    _stage2Template = '\n### $Title\n\n$Desc\n\n'

