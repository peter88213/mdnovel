"""Provide a class for Markdown file representation. 

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re

from mdnvlib.file.file_export import FileExport
from mdnvlib.model.chapter import Chapter
from mdnvlib.model.section import Section
from mdnvlib.novx_globals import CHAPTER_PREFIX
from mdnvlib.novx_globals import CH_ROOT
from mdnvlib.novx_globals import Error
from mdnvlib.novx_globals import SECTION_PREFIX
from mdnvlib.novx_globals import _
from mdnvlib.novx_globals import norm_path


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

    def _get_chapterMapping(self, chId, chapterNumber):
        """Return a mapping dictionary for a chapter section.
        
        Positional arguments:
            chId -- str: chapter ID.
            chapterNumber -- int: chapter number.
        
        Suppress the chapter title if necessary.
        Extends the superclass method.
        """
        chapterMapping = super()._get_chapterMapping(chId, chapterNumber)
        return chapterMapping

    def _convert_from_novx(self, text, quick=False, append=False, firstInChapter=False, xml=False):
        """Return text, converted to Markdown.
        
        Positional arguments:
            text -- string to convert.
        
        Optional arguments:
            quick -- bool: if True, apply a conversion mode for one-liners without formatting.
        
        Overrides the superclass method.
        """
        if quick:
            # Just clean up a one-liner without sophisticated formatting.
            if text is None:
                return ''
            else:
                return re.sub(r'<.*?>', '', text)

        MD_REPLACEMENTS = [
            ('<em> ', ' <em>'),
            ('<strong> ', ' <strong>'),
            ('<p>', ''),
            ('</p>', '\n\n'),
            ('<em>', '*'),
            ('</em>', '*'),
            ('<strong>', '**'),
            ('</strong>', '**'),
            ('<comment>', '<!---\n'),
            ('\n\n</comment>', '\n--->'),
            ('</comment>\n\n', '--->'),
            ('</comment>', '--->'),
            ('  ', ' '),
        ]
        try:
            for novx, md in MD_REPLACEMENTS:
                text = text.replace(novx, md)
            text = re.sub(r'<creator>.*?</creator>', '', text)
            text = re.sub(r'<date>.*?</date>', '', text)
            text = re.sub(r'<.*?>', '', text)
            # removing the remaining XML tags, if any
        except AttributeError:
            text = ''
        return re.sub(r'<.*?>', '', text).strip()

    def read(self):
        """Parse the file and get the instance variables.
        
        Return a message beginning with the ERROR constant in case of error.
        """
        LOW_WORDCOUNT = 10
        # Defines the difference between "Outline" and "Draft"

        def write_section_content(scId, lines):
            if scId is not None:
                # text = '\n\n'.join(lines)
                newlines = []
                for line in lines:
                    newlines.append(f'<p>{line}</p>')
                text = ''.join(newlines)
                text = text.replace('\n', '')

                self.novel.sections[scId].sectionContent = text
                if self.novel.sections[scId].wordCount < LOW_WORDCOUNT:
                    self.novel.sections[scId].status = 1
                else:
                    self.novel.sections[scId].status = 0

        chCount = 0
        scCount = 0
        lines = []
        chId = None
        scId = None
        try:
            with open(self.filePath, 'r', encoding='utf-8') as f:
                mdText = f.read()
        except(FileNotFoundError):
            raise Error(f'{_("File not found")}: "{norm_path(self.filePath)}".')

        except:
            try:
                # the file may be ANSI encoded.
                with open(self.filePath, 'r') as f:
                    mdText = f.read()
            except:
                raise Error(f'{_("Cannot read file")}: "{norm_path(self.filePath)}".')

        cnvText = mdText
        mdLines = cnvText.split('\n')
        scTitlePrefix = '### '
        scTitle = None
        for mdLine in mdLines:
            if mdLine.startswith('# ') or mdLine.startswith('## '):

                # Write previous section.
                write_section_content(scId, lines)
                scId = None

                # Add a chapter.
                chCount += 1
                chId = f'{CHAPTER_PREFIX}{chCount}'
                self.novel.chapters[chId] = Chapter()
                chTitle = mdLine.split('# ')[1]
                self.novel.chapters[chId].title = chTitle
                self.novel.tree.append(CH_ROOT, chId)
                self.novel.chapters[chId].chType = 0
                if mdLine.startswith('# '):
                    self.novel.chapters[chId].chLevel = 1
                else:
                    self.novel.chapters[chId].chLevel = 0
                self.novel.chapters[chId].srtSections = []
                scTitle = None
            elif self.SECTION_DIVIDER in mdLine:
                # Write previous section.
                write_section_content(scId, lines)
                scTitle = None
                scId = None
            elif mdLine.startswith(scTitlePrefix):
                write_section_content(scId, lines)
                scTitle = mdLine.lstrip(scTitlePrefix).strip()
                scId = None
            elif scId is not None:
                if mdLine or lines:
                    # skipping the first line if empty
                    lines.append(mdLine)
            elif mdLine and chId is not None:
                # Add a section.
                scCount += 1
                scId = f'{SECTION_PREFIX}{scCount}'
                self.novel.sections[scId] = Section(
                    status=1,
                    scType=0,
                    scene=0,
                    )
                self.novel.tree.append(chId, scId)
                if scTitle is not None:
                    self.novel.sections[scId].title = scTitle
                else:
                    self.novel.sections[scId].title = f'{_("Section")} {scCount}'
                lines = []
        write_section_content(scId, lines)
        return 'Markdown formatted text converted to novel structure.'
