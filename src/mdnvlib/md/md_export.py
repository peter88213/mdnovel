"""Provide a class for Markdown file representation. 

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from mdnvlib.md.md_file import MdFile


class MdExport(MdFile):
    """Markdown file representation.

    Public methods:
        read() -- parse the file and get the instance variables.
    """
    DESCRIPTION = 'Markdown file'
    EXTENSION = '.md'
    SUFFIX = ''
    _partTemplate = '\n# ${Title}\n\n'
    _chapterTemplate = '\n## ${Title}\n\n'
    _sectionTemplate = '${SectionContent}\n\n'
    _sectionDivider = f'{MdFile.SECTION_DIVIDER}\n\n'

