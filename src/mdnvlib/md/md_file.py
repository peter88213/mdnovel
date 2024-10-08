"""Provide a class for Markdown file representation. 

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from mdnvlib.file.file_export import FileExport


class MdFile(FileExport):
    """Markdown file representation.

    Public methods:
        read() -- parse the file and get the instance variables.
    """
    DESCRIPTION = 'Markdown file'
    EXTENSION = '.md'
    SUFFIX = ''
    SECTION_DIVIDER = '* * *'
    _fileHeader = '''**${Title}**  
  
*${AuthorName}*  
  
'''

    def _convert_from_novx(self, text, quick=False, append=False, firstInChapter=False, xml=False):
        """Return text, converted to Markdown.
        
        Positional arguments:
            text -- string to convert.
        
        Optional arguments:
            quick -- bool: if True, apply a conversion mode for one-liners without formatting.
        
        Overrides the superclass method.
        """
        if text is None:
            return ''

        if quick:
            # Just clean up a one-liner without sophisticated formatting.
            return text

        return text.replace('\n\n', '\n').replace('\n', '\n\n').strip()

