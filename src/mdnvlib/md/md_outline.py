"""Provide a class for Markdown file representation. 

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from mdnvlib.md.md_file import MdFile
from mdnvlib.model.chapter import Chapter
from mdnvlib.model.id_generator import create_id
from mdnvlib.model.section import Section
from mdnvlib.novx_globals import CHAPTER_PREFIX
from mdnvlib.novx_globals import CH_ROOT
from mdnvlib.novx_globals import Error
from mdnvlib.novx_globals import SECTION_PREFIX
from mdnvlib.novx_globals import _
from mdnvlib.novx_globals import norm_path


class MdOutline(MdFile):
    """Markdown outline file representation.

    Public methods:
        read() -- parse the file and get the instance variables.
    """

    def read(self):
        """Parse the outline file and create a project."""

        def write_desc(element, lines):
            # text = '\n\n'.join(lines)
            newlines = []
            for line in lines:
                newlines.append(line)
            text = ''.join(newlines)
            text = text.replace('\n', '')
            element.desc = text

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
        scTitle = None
        for mdLine in mdLines:
            if mdLine.startswith('# ') or mdLine.startswith('## '):
                if scId is not None:
                    # Write previous section.
                    write_desc(self.novel.sections[scId], lines)
                    scId = None

                elif chId is not None:
                    # Write previous section.
                    write_desc(self.novel.chapters[chId], lines)
                    scId = None

                # Add a chapter.
                chCount += 1
                chId = create_id(self.novel.chapters, CHAPTER_PREFIX)
                self.novel.chapters[chId] = Chapter()
                chTitle = mdLine.split('# ')[1]
                self.novel.chapters[chId].title = chTitle
                self.novel.tree.append(CH_ROOT, chId)
                self.novel.chapters[chId].chType = 0
                if mdLine.startswith('# '):
                    self.novel.chapters[chId].chLevel = 1
                else:
                    self.novel.chapters[chId].chLevel = 0
                scTitle = None
                lines = []
            elif mdLine.startswith('### '):
                if scId is not None:
                    write_desc(self.novel.sections[scId], lines)
                elif chId is not None:
                    write_desc(self.novel.chapters[chId], lines)
                scTitle = mdLine.lstrip('### ').strip()
                lines = []

                scCount += 1
                scId = create_id(self.novel.sections, SECTION_PREFIX)
                self.novel.sections[scId] = Section(
                    status=1,
                    scType=0,
                    scene=0,
                    )
                self.novel.tree.append(chId, scId)
                self.novel.sections[scId].title = f'Section {scCount}'
                if scTitle is not None:
                    self.novel.sections[scId].title = scTitle
            elif mdLine or lines:
                lines.append(mdLine)
        if scId is not None:
            write_desc(self.novel.sections[scId], lines)
        elif chId is not None:
            write_desc(self.novel.chapters[chId], lines)
