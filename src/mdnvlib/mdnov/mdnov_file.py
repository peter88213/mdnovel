"""Provide a class for mdnov file import and export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date
import os

from mdnvlib.md.md_file import MdFile
from mdnvlib.md.md_helper import sanitize_markdown
from mdnvlib.model.basic_element import BasicElement
from mdnvlib.model.chapter import Chapter
from mdnvlib.model.character import Character
from mdnvlib.model.novel import Novel
from mdnvlib.model.plot_line import PlotLine
from mdnvlib.model.plot_point import PlotPoint
from mdnvlib.model.section import Section
from mdnvlib.model.world_element import WorldElement
from mdnvlib.novx_globals import CHAPTER_PREFIX, string_to_list
from mdnvlib.novx_globals import CHARACTER_PREFIX
from mdnvlib.novx_globals import CH_ROOT
from mdnvlib.novx_globals import CR_ROOT
from mdnvlib.novx_globals import ITEM_PREFIX
from mdnvlib.novx_globals import IT_ROOT
from mdnvlib.novx_globals import LC_ROOT
from mdnvlib.novx_globals import LOCATION_PREFIX
from mdnvlib.novx_globals import PLOT_LINE_PREFIX
from mdnvlib.novx_globals import PLOT_POINT_PREFIX
from mdnvlib.novx_globals import PL_ROOT
from mdnvlib.novx_globals import PN_ROOT
from mdnvlib.novx_globals import PRJ_NOTE_PREFIX
from mdnvlib.novx_globals import SECTION_PREFIX
from mdnvlib.novx_globals import _
from mdnvlib.novx_globals import intersection
from mdnvlib.novx_globals import list_to_string
from mdnvlib.novx_globals import verified_date
from mdnvlib.novx_globals import verified_int_string


class MdnovFile(MdFile):
    """mdnov file representation.

    Public instance variables:
        wcLog: dict[str, list[str, str]] -- Daily word count logs.
        wcLogUpdate: dict[str, list[str, str]] -- Word counts missing in the log.
        timestamp: float -- Time of last file modification (number of seconds since the epoch).
    
    
    """
    DESCRIPTION = _('mdnovel project')
    EXTENSION = '.mdnov'

    _fileHeader = '''@@book
    
---
$YAML
---


$Links
%%

'''
    _chapterTemplate = '''
@@$ID
    
---
$YAML
---

$Links$Desc$Notes
%%

'''
    _partTemplate = _chapterTemplate
    _unusedChapterTemplate = _chapterTemplate
    _sectionTemplate = '''
@@$ID
    
---
$YAML
---

$Links$Desc$Notes$Goal$Conflict$Outcome$Plotlines$SectionContent%%
'''
    _unusedSectionTemplate = _sectionTemplate
    _stage1Template = _sectionTemplate
    _stage2Template = _sectionTemplate
    _sectionDivider = ''
    _chapterEndTemplate = ''
    _unusedChapterEndTemplate = ''
    _characterSectionHeading = ''
    _characterTemplate = '''
@@$ID
    
---
$YAML
---

$Links$Desc$Bio$Goals
%%

'''
    _locationSectionHeading = ''
    _locationTemplate = '''
@@$ID
    
---
$YAML
---

$Links$Desc
%%

'''
    _itemSectionHeading = ''
    _itemTemplate = _locationTemplate
    _projectNoteTemplate = _locationTemplate
    _arcTemplate = '''
@@$ID
    
---
$YAML
---

$Links$Desc
%%

'''
    _fileFooter = '\n$Wordcountlog\n\n%%'

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.
        
        Positional arguments:
            filePath: str -- path to the mdnov file.
            
        Optional arguments:
            kwargs -- keyword arguments (not used here).            
        
        Extends the superclass constructor.
        """
        super().__init__(filePath)
        self.on_element_change = None

        self.wcLog = {}
        # key: str -- date (iso formatted)
        # value: list -- [word count: str, with unused: str]

        self.wcLogUpdate = {}
        # key: str -- date (iso formatted)
        # value: list -- [word count: str, with unused: str]

        self.timestamp = None
        self._range = None
        self._collectedLines = None
        self._properties = {}
        self._plId = None

    def adjust_section_types(self):
        """Make sure that nodes with "Unused" parents inherit the type."""
        partType = 0
        for chId in self.novel.tree.get_children(CH_ROOT):
            if self.novel.chapters[chId].chLevel == 1:
                partType = self.novel.chapters[chId].chType
            elif partType != 0 and not self.novel.chapters[chId].isTrash:
                self.novel.chapters[chId].chType = partType
            for scId in self.novel.tree.get_children(chId):
                if self.novel.sections[scId].scType < self.novel.chapters[chId].chType:
                    self.novel.sections[scId].scType = self.novel.chapters[chId].chType

    def count_words(self):
        """Return a tuple of word count totals.
        
        count: int -- Total words of "normal" type sections.
        totalCount: int -- Total words of "normal" and "unused" sections.
        """
        count = 0
        totalCount = 0
        for chId in self.novel.tree.get_children(CH_ROOT):
            if not self.novel.chapters[chId].isTrash:
                for scId in self.novel.tree.get_children(chId):
                    if self.novel.sections[scId].scType < 2:
                        totalCount += self.novel.sections[scId].wordCount
                        if self.novel.sections[scId].scType == 0:
                            count += self.novel.sections[scId].wordCount
        return count, totalCount

    def read(self):
        """Read and parse the mdnov file.
        
        Overrides the superclass method.
        """
        with open(self.filePath, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
        processor = None
        elemId = None
        chId = None
        self._collectedLines = None
        self.novel.tree.reset()
        for self._line in lines:
            if self._line.startswith('@@book'):
                processor = self._read_project
                elemId = None
                element = self.novel
                continue

            if self._line.startswith(f'@@{CHAPTER_PREFIX}'):
                processor = self._read_chapter
                elemId = self._line.split('@@')[1].strip()
                self.novel.chapters[elemId] = Chapter(on_element_change=self.on_element_change)
                self.novel.tree.append(CH_ROOT, elemId)
                element = self.novel.chapters[elemId]
                chId = elemId
                continue

            if self._line.startswith(f'@@{CHARACTER_PREFIX}'):
                processor = self._read_character
                elemId = self._line.split('@@')[1].strip()
                self.novel.characters[elemId] = Character(on_element_change=self.on_element_change)
                self.novel.tree.append(CR_ROOT, elemId)
                element = self.novel.characters[elemId]
                continue

            if self._line.startswith(f'@@{ITEM_PREFIX}'):
                processor = self._read_world_element
                elemId = self._line.split('@@')[1].strip()
                self.novel.items[elemId] = WorldElement(on_element_change=self.on_element_change)
                self.novel.tree.append(IT_ROOT, elemId)
                element = self.novel.items[elemId]
                continue

            if self._line.startswith(f'@@{LOCATION_PREFIX}'):
                processor = self._read_world_element
                elemId = self._line.split('@@')[1].strip()
                self.novel.locations[elemId] = WorldElement(on_element_change=self.on_element_change)
                self.novel.tree.append(LC_ROOT, elemId)
                element = self.novel.locations[elemId]
                continue

            if self._line.startswith(f'@@{PLOT_LINE_PREFIX}'):
                processor = self._read_plot_line
                elemId = self._line.split('@@')[1].strip()
                self.novel.plotLines[elemId] = PlotLine(on_element_change=self.on_element_change)
                self.novel.tree.append(PL_ROOT, elemId)
                element = self.novel.plotLines[elemId]
                plId = elemId
                continue

            if self._line.startswith(f'@@{PLOT_POINT_PREFIX}'):
                processor = self._read_plot_point
                elemId = self._line.split('@@')[1].strip()
                self.novel.plotPoints[elemId] = PlotPoint(on_element_change=self.on_element_change)
                self.novel.tree.append(plId, elemId)
                element = (self.novel.plotPoints[elemId])
                continue

            if self._line.startswith(f'@@{PRJ_NOTE_PREFIX}'):
                processor = self._read_project_note
                elemId = self._line.split('@@')[1].strip()
                self.novel.projectNotes[elemId] = BasicElement()
                self.novel.tree.append(PN_ROOT, elemId)
                element = self.novel.projectNotes[elemId]
                continue

            if self._line.startswith(f'@@{SECTION_PREFIX}'):
                processor = self._read_section
                elemId = self._line.split('@@')[1].strip()
                self.novel.sections[elemId] = Section(on_element_change=self.on_element_change)
                self.novel.tree.append(chId, elemId)
                element = self.novel.sections[elemId]
                continue

            if self._line.startswith(f'@@Progress'):
                processor = self._read_word_count_log
                elemId = None
                continue

            if processor is not None:
                processor(element)

        for scId in self.novel.sections:

            # Remove dead references.
            self.novel.sections[scId].characters = intersection(self.novel.sections[scId].characters, self.novel.characters)
            self.novel.sections[scId].locations = intersection(self.novel.sections[scId].locations, self.novel.locations)
            self.novel.sections[scId].items = intersection(self.novel.sections[scId].items, self.novel.items)

        for ppId in self.novel.plotPoints:

            # Verify section and create back reference.
            scId = self.novel.plotPoints[ppId].sectionAssoc
            if scId in self.novel.sections:
                self.novel.sections[scId].scPlotPoints[ppId] = plId
            else:
                self.novel.plotPoints[ppId].sectionAssoc = None

        for plId in self.novel.plotLines:

            # Remove dead references.
            self.novel.plotLines[plId].sections = intersection(self.novel.plotLines[plId].sections, self.novel.sections)

            # Create back references.
            for scId in self.novel.plotLines[plId].sections:
                self.novel.sections[scId].scPlotLines.append(plId)

        self._get_timestamp()
        self._keep_word_count()

    def write(self):
        super().write()
        self._get_timestamp()

    def _add_key(self, text, key):
        if not key:
            return ''

        if not text:
            return ''

        return f'%%{key}:\n\n{sanitize_markdown(text)}\n\n'

    def _add_links(self, element, mapping):
        links = element.get_links()
        linkRepr = []
        if links:
            for relativeLink, absoluteLink in links:
                linkRepr.append('%%Link:')
                linkRepr.append(relativeLink)
                linkRepr.append(absoluteLink)
        links = '\n\n'.join(linkRepr)
        mapping['Links'] = f'{links}\n'
        return mapping

    def _add_plotline_notes(self, prjScn, mapping):
        plRepr = []
        if prjScn.plotlineNotes:
            for plId in prjScn.plotlineNotes:
                if not plId in prjScn.scPlotLines:
                    continue

                if not prjScn.plotlineNotes[plId]:
                    continue

                plRepr.append('%%Plotline:')
                plRepr.append(plId)

                plRepr.append('%%Plotline note:')
                plRepr.append(sanitize_markdown(prjScn.plotlineNotes[plId]))
        plStr = '\n\n'.join(plRepr)
        mapping['Plotlines'] = f'{plStr}\n\n'
        return mapping

    def _add_yaml(self, element, mapping):
        yaml = element.to_yaml([])
        mapping['YAML'] = '\n'.join(yaml)
        return mapping

    def _get_arcMapping(self, plId):
        mapping = super()._get_arcMapping(plId)
        element = self.novel.plotLines[plId]
        mapping = self._add_yaml(element, mapping)
        mapping = self._add_links(element, mapping)
        mapping['Desc'] = self._add_key(element.desc, 'Desc')
        return mapping

    def _get_chapterMapping(self, chId, chapterNumber):
        mapping = super()._get_chapterMapping(chId, chapterNumber)
        element = self.novel.chapters[chId]
        mapping = self._add_yaml(element, mapping)
        mapping = self._add_links(element, mapping)
        mapping['Desc'] = self._add_key(element.desc, 'Desc')
        mapping['Notes'] = self._add_key(element.desc, 'Notes')
        return mapping

    def _get_characterMapping(self, crId):
        mapping = super()._get_characterMapping(crId)
        element = self.novel.characters[crId]
        mapping = self._add_yaml(element, mapping)
        mapping = self._add_links(element, mapping)
        mapping['Desc'] = self._add_key(element.desc, 'Desc')
        mapping['Bio'] = self._add_key(element.bio, 'Bio')
        mapping['Goals'] = self._add_key(element.goals, 'Goals')
        mapping['Notes'] = self._add_key(element.desc, 'Notes')
        return mapping

    def _get_fileFooterMapping(self):
        mapping = {}
        if not self.wcLog:
            mapping['Wordcountlog'] = ''
            return mapping

        lines = ['@@Progress']
        wcLastCount = None
        wcLastTotalCount = None
        for wc in self.wcLog:
            if self.novel.saveWordCount:
                # Discard entries with unchanged word count.
                if self.wcLog[wc][0] == wcLastCount and self.wcLog[wc][1] == wcLastTotalCount:
                    continue

                wcLastCount = self.wcLog[wc][0]
                wcLastTotalCount = self.wcLog[wc][1]
            lines.append(f'- {list_to_string([wc, self.wcLog[wc][0], self.wcLog[wc][1]])}')
        mapping['Wordcountlog'] = '\n'.join(lines)
        return mapping

    def _get_fileHeaderMapping(self):
        mapping = super()._get_fileHeaderMapping()
        element = self.novel
        mapping = self._add_yaml(element, mapping)
        mapping = self._add_links(element, mapping)
        mapping['Desc'] = self._add_key(element.desc, 'Desc')
        return mapping

    def _get_itemMapping(self, itId):
        mapping = super()._get_itemMapping(itId)
        element = self.novel.items[itId]
        mapping = self._add_yaml(element, mapping)
        mapping = self._add_links(element, mapping)
        mapping['Desc'] = self._add_key(element.desc, 'Desc')
        mapping['Notes'] = self._add_key(element.desc, 'Notes')
        return mapping

    def _get_locationMapping(self, lcId):
        mapping = super()._get_locationMapping(lcId)
        element = self.novel.locations[lcId]
        mapping = self._add_yaml(element, mapping)
        mapping = self._add_links(element, mapping)
        mapping['Desc'] = self._add_key(element.desc, 'Desc')
        mapping['Notes'] = self._add_key(element.desc, 'Notes')
        return mapping

    def _get_prjNoteMapping(self, pnId):
        mapping = super()._get_prjNoteMapping(pnId)
        element = self.novel.projectNotes[pnId]
        mapping = self._add_yaml(element, mapping)
        mapping = self._add_links(element, mapping)
        mapping['Desc'] = self._add_key(element.desc, 'Desc')
        return mapping

    def _get_sectionMapping(self, scId, sectionNumber, wordsTotal, firstInChapter=False):
        mapping = super()._get_sectionMapping(scId, sectionNumber, wordsTotal)
        element = self.novel.sections[scId]
        mapping = self._add_yaml(element, mapping)
        mapping = self._add_links(element, mapping)
        mapping = self._add_plotline_notes(element, mapping)
        mapping['Desc'] = self._add_key(element.desc, 'Desc')
        mapping['Goal'] = self._add_key(element.goal, 'Goal')
        mapping['Conflict'] = self._add_key(element.conflict, 'Conflict')
        mapping['Outcome'] = self._add_key(element.outcome, 'Outcome')
        mapping['Notes'] = self._add_key(element.notes, 'Notes')
        mapping['SectionContent'] = self._add_key(element.sectionContent, 'Content')
        return mapping

    def _get_timestamp(self):
        try:
            self.timestamp = os.path.getmtime(self.filePath)
        except:
            self.timestamp = None

    def _keep_word_count(self):
        """Keep the actual wordcount, if not logged."""
        if not self.wcLog:
            return

        actualCountInt, actualTotalCountInt = self.count_words()
        actualCount = str(actualCountInt)
        actualTotalCount = str(actualTotalCountInt)
        latestDate = list(self.wcLog)[-1]
        latestCount = self.wcLog[latestDate][0]
        latestTotalCount = self.wcLog[latestDate][1]
        if actualCount != latestCount or actualTotalCount != latestTotalCount:
            try:
                fileDateIso = date.fromtimestamp(self.timestamp).isoformat()
            except:
                fileDateIso = date.today().isoformat()
            self.wcLogUpdate[fileDateIso] = [actualCount, actualTotalCount]

    def _read_element(self, element):
        if self._line.startswith('---'):
            if self._range != 'yaml':
                self._range = 'yaml'
                self._collectedLines = []
            else:
                element.from_yaml(self._collectedLines)
                self._range = None
            return

        if self._line.startswith('%%'):

            if self._range is not None:
                # write collected lines
                text = '\n'.join(self._collectedLines).strip()
                classProperty = self._properties.get(self._range, None)
                if classProperty is not None:
                    classProperty.fset(element, f'{text}\n')
                    self._plId = None
                elif self._range == 'Plotline':
                    self._plId = text
                elif self._range == 'Plotline note'and self._plId is not None:
                    plNotes = element.plotlineNotes
                    plNotes[self._plId] = text
                    element.plotlineNotes = plNotes
                    self._plId = None
                elif self._range == 'Link':
                    self._set_links(element, text)
                elif self._range == 'Progress':
                    self._set_word_count(text)
            self._collectedLines = []
            tag = self._line.strip('%: ')
            if tag:
                self._range = tag

        elif self._range is not None:
            self._collectedLines.append(self._line)

    def _read_chapter(self, element):
        self._properties = {
            'Desc':Chapter.desc,
            'Notes':Chapter.notes,
        }
        self._read_element(element)

    def _read_character(self, element):
        self._properties = {
            'Desc':Character.desc,
            'Notes':Character.notes,
            'Bio':Character.bio,
            'Goals':Character.goals,
        }
        self._read_element(element)

    def _read_world_element(self, element):
        self._properties = {
            'Desc':WorldElement.desc,
            'Notes':WorldElement.notes,
        }
        self._read_element(element)

    def _read_plot_line(self, element):
        self._properties = {
            'Desc':PlotLine.desc,
            'Notes':PlotLine.notes,
        }
        self._read_element(element)

    def _read_plot_point(self, element):
        self._properties = {
            'Desc':PlotPoint.desc,
            'Notes':PlotPoint.notes,
        }
        self._read_element(element)

    def _read_project(self, element):
        self._properties = {
            'Desc':Novel.desc,
        }
        self._read_element(element)

    def _read_project_note(self, element):
        self._properties = {
            'Desc':BasicElement.desc,
        }
        self._read_element(element)

    def _read_section(self, element):
        if element.plotlineNotes is None:
            element.plotlineNotes = {}
        self._properties = {
            'Desc':Section.desc,
            'Notes':Section.notes,
            'Goal':Section.goal,
            'Conflict':Section.conflict,
            'Outcome':Section.outcome,
            'Content':Section.sectionContent,
        }
        self._read_element(element)

    def _read_word_count_log(self, element):
        self._range = 'Progress'
        self._read_element(element)

    def _set_links(self, element, text):
        linkList = []
        relativeLink = ''
        absoluteLink = ''
        for line in text.split('\n'):
            if not line:
                continue

            linkType, link = line.split('](')
            if linkType == '[LinkPath':
                relativeLink = link.strip(') ')
            elif linkType == '[FullPath':
                absoluteLink = link.strip(') ')
                if relativeLink:
                    linkList.append((relativeLink, absoluteLink))
                relativeLink = ''
                absoluteLink = ''
        element.set_links(linkList)

    def _set_word_count(self, text):
        for line in text.split('\n'):
            if not line:
                continue

            wc = (line.strip('- ').split(';'))
            self.wcLog[wc[0]] = [wc[1], wc[2]]

    def _update_word_count_log(self):
        """Add today's word count and word count when reading, if not logged."""
        if self.novel.saveWordCount:
            newCountInt, newTotalCountInt = self.count_words()
            newCount = str(newCountInt)
            newTotalCount = str(newTotalCountInt)
            todayIso = date.today().isoformat()
            self.wcLogUpdate[todayIso] = [newCount, newTotalCount]
            for wcDate in self.wcLogUpdate:
                self.wcLog[wcDate] = self.wcLogUpdate[wcDate]
        self.wcLogUpdate = {}

