"""Provide a class for Markdown work-in-progress file representation. 

Copyright (c) 2024 Peter Triesberger
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


class MdImport(MdFile):
    """Markdown work-in-progress reader.

    Public methods:
        read() -- parse the file and get the instance variables.
    """

    def read(self):
        """Parse the WIP file and create a project."""
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
                    self.novel.sections[scId].status = 2

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
        for mdLine in mdLines:
            if mdLine.startswith('#'):

                # Write previous section.
                write_section_content(scId, lines)
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
            elif self.SECTION_DIVIDER in mdLine:
                # Write previous section.
                write_section_content(scId, lines)
                scId = None
            elif scId is not None:
                if mdLine or lines:
                    # skipping the first line if empty
                    lines.append(mdLine)
            elif mdLine and chId is not None:
                # Add a section.
                scCount += 1
                scId = create_id(self.novel.sections, SECTION_PREFIX)
                self.novel.sections[scId] = Section(
                    status=1,
                    scType=0,
                    scene=0,
                    )
                self.novel.tree.append(chId, scId)
                self.novel.sections[scId].title = f'{_("Section")} {scCount}'
                lines = [mdLine]
        write_section_content(scId, lines)
