"""Provide a class for Markdown story template representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_templates
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.novx_globals import CH_ROOT
from mdnvlib.novx_globals import Error
from mdnvlib.novx_globals import _
from mdnvlib.novx_globals import norm_path


class MdTemplate:
    """Markdown story template representation.
    
    Public instance variables:
        filePath: str -- path to the file (property with getter and setter). 
    """
    DESCRIPTION = _('Story Template')
    EXTENSION = '.md'

    def __init__(self, filePath, model, controller):
        """Initialize instance variables.

        Positional arguments:
            filePath: str -- path to the file represented by the File instance.
            model -- Reference to the model instance of the application.
            controller -- Reference to the main controller instance of the application.
        """
        self.filePath = filePath
        self._mdl = model
        self._ctrl = controller

    def read(self):
        """Parse the Markdown file and create parts, chapters, and sections.
        
        Raise the "Error" exception in case of error. 
        """
        try:
            with open(self.filePath, 'r', encoding='utf-8') as f:
                mdLines = f.readlines()
        except(FileNotFoundError):
            raise Error(f'{_("File not found")}: "{norm_path(self.filePath)}".')
        except:
            raise Error(f'{_("Cannot read file")}: "{norm_path(self.filePath)}".')

        if self._mdl.novel.chapters:
            self.list_stages(mdLines)
        else:
            self.create_chapter_structure(mdLines)

    def create_chapter_structure(self, mdLines):
        i = 0
        chId = CH_ROOT
        addChapter = True
        newElement = None
        notes = []
        for mdLine in mdLines:
            mdLine = mdLine.strip()
            if mdLine.startswith('#'):
                if newElement is not None:
                    newElement.notes = ''.join(notes).strip().replace('  ', ' ')
                    notes = []
                    newElement = None
                if mdLine.startswith('## '):
                    # Add a 2nd level stage.
                    if addChapter:
                        i += 1
                        chId = self._ctrl.add_chapter(targetNode=chId, title=f"{_('Chapter')} {i}", chLevel=2, chType=0)
                        scId = chId
                    newTitle = mdLine[3:].strip()
                    scId = self._ctrl.add_stage(targetNode=scId, title=newTitle, scType=3)
                    newElement = self._mdl.novel.sections[scId]
                    scId = self._ctrl.add_section(targetNode=scId, title=_('New Section'), scType=0, status=1)
                    addChapter = True
                elif mdLine.startswith('# '):
                    # Add a ist level stage.
                    i += 1
                    chId = self._ctrl.add_chapter(targetNode=chId, title=f"{_('Chapter')} {i}", chLevel=2, chType=0)
                    newTitle = mdLine[2:].strip()
                    scId = self._ctrl.add_stage(targetNode=chId, title=newTitle, scType=2)
                    newElement = self._mdl.novel.sections[scId]
                    addChapter = False
                else:
                    scId = None
            elif mdLine:
                notes.append(f'{mdLine} ')
            else:
                notes.append('\n')
        try:
            newElement.notes = ''.join(notes).strip().replace('  ', ' ')
        except AttributeError:
            pass

    def list_stages(self, mdLines):
        chId = self._ctrl.add_chapter(targetNode=CH_ROOT, title=_('Stages'), chLevel=2, chType=3)
        scId = chId
        newElement = None
        notes = []
        for mdLine in mdLines:
            mdLine = mdLine.strip()
            if mdLine.startswith('#'):
                if newElement is not None:
                    newElement.notes = ''.join(notes).strip().replace('  ', ' ')
                    notes = []
                    newElement = None
                if mdLine.startswith('## '):
                    # Add a 2nd level stage.
                    newTitle = mdLine[3:].strip()
                    scId = self._ctrl.add_stage(targetNode=scId, title=newTitle, scType=3)
                elif mdLine.startswith('# '):
                    # Add a 1st level stage.
                    newTitle = mdLine[2:].strip()
                    scId = self._ctrl.add_stage(targetNode=scId, title=newTitle, scType=2)
                else:
                    scId = None
                if scId:
                    newElement = self._mdl.novel.sections[scId]
            elif mdLine:
                notes.append(f'{mdLine} ')
            else:
                notes.append('\n')
        try:
            newElement.notes = ''.join(notes).strip().replace('  ', ' ')
        except AttributeError:
            pass

    def write(self):
        """Iterate the project structure and write the new elements to a Markdown file.
        
        Raise the "Error" exception in case of error. 
        """
        mdLines = []
        for chId in self._mdl.novel.tree.get_children(CH_ROOT):
            for scId in self._mdl.novel.tree.get_children(chId):
                if self._mdl.novel.sections[scId].scType == 2:
                    mdLines.append(f'# {self._mdl.novel.sections[scId].title}')
                    notes = self._mdl.novel.sections[scId].notes
                    if notes:
                        mdLines.append(notes.replace('\n', '\n\n'))
                elif self._mdl.novel.sections[scId].scType == 3:
                    mdLines.append(f'## {self._mdl.novel.sections[scId].title}')
                    notes = self._mdl.novel.sections[scId].notes
                    if notes:
                        mdLines.append(notes.replace('\n', '\n\n'))

        content = '\n\n'.join(mdLines)
        try:
            with open(self.filePath, 'w', encoding='utf-8') as f:
                f.write(content)
        except:
            raise Error(f'{_("Cannot write file")}: "{norm_path(self.filePath)}".')

