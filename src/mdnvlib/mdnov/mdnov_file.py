"""Provide a class for mdnov file import and export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date
import os

from mdnvlib.file.file_export import FileExport
from mdnvlib.model.basic_element import BasicElement
from mdnvlib.model.chapter import Chapter
from mdnvlib.model.character import Character
from mdnvlib.model.plot_line import PlotLine
from mdnvlib.model.plot_point import PlotPoint
from mdnvlib.model.section import Section
from mdnvlib.model.world_element import WorldElement
from mdnvlib.novx_globals import CHAPTER_PREFIX
from mdnvlib.novx_globals import CHARACTER_PREFIX
from mdnvlib.novx_globals import CH_ROOT
from mdnvlib.novx_globals import CR_ROOT
from mdnvlib.novx_globals import Error
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
from mdnvlib.novx_globals import norm_path
from mdnvlib.novx_globals import verified_date
from mdnvlib.novx_globals import verified_int_string
import xml.etree.ElementTree as ET


def get_xml_root(filePath):
    try:
        xmlTree = ET.parse(filePath)
    except Exception as ex:
        raise Error(f'{_("Cannot process file")}: "{norm_path(filePath)}" - {str(ex)}')

    return xmlTree.getroot()


class MdnovFile(FileExport):
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


'''
    _chapterTemplate = '''@@$ID
    
---
$YAML
---

$Desc$Notes
'''
    _partTemplate = _chapterTemplate
    _unusedChapterTemplate = _chapterTemplate
    _sectionTemplate = '''@@$ID
    
---
$YAML
---

$Desc$Notes$Goal$Conflict$Outcome$SectionContent
'''
    _unusedSectionTemplate = _sectionTemplate
    _stage1Template = _sectionTemplate
    _stage2Template = _sectionTemplate
    _sectionDivider = ''
    _chapterEndTemplate = ''
    _unusedChapterEndTemplate = ''
    _characterSectionHeading = ''
    _characterTemplate = '''@@$ID
    
---
$YAML
---

$Desc$Bio$Goals
'''
    _locationSectionHeading = ''
    _locationTemplate = '''@@$ID
    
---
$YAML
---

$Desc
'''
    _itemSectionHeading = ''
    _itemTemplate = _locationTemplate
    _projectNoteTemplate = _locationTemplate
    _arcTemplate = '''@@$ID
    
---
$YAML
---

$Desc
'''
    _fileFooter = ''

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
        self.xmlTree = None

        self.wcLog = {}
        # key: str -- date (iso formatted)
        # value: list -- [word count: str, with unused: str]

        self.wcLogUpdate = {}
        # key: str -- date (iso formatted)
        # value: list -- [word count: str, with unused: str]

        self.timestamp = None

    def _add_key(self, text, key):
        if not key:
            return ''

        if not text:
            return ''

        return f'%%{key}:\n\n{text.strip()}\n\n'

    def _add_yaml(self, element, mapping):
        yaml = element.to_yaml([])
        mapping['YAML'] = '\n'.join(yaml)
        return mapping

    def _get_arcMapping(self, plId):
        mapping = super()._get_arcMapping(plId)
        element = self.novel.arcs[plId]
        mapping = self._add_yaml(element, mapping)
        mapping['Desc'] = self._add_key(element.desc, 'Desc')
        return mapping

    def _get_chapterMapping(self, chId, chapterNumber):
        mapping = super()._get_chapterMapping(chId, chapterNumber)
        element = self.novel.chapters[chId]
        mapping = self._add_yaml(element, mapping)
        mapping['Desc'] = self._add_key(element.desc, 'Desc')
        mapping['Notes'] = self._add_key(element.desc, 'Notes')
        return mapping

    def _get_characterMapping(self, crId):
        mapping = super()._get_characterMapping(crId)
        element = self.novel.characters[crId]
        mapping = self._add_yaml(element, mapping)
        mapping['Desc'] = self._add_key(element.desc, 'Desc')
        mapping['Bio'] = self._add_key(element.bio, 'Bio')
        mapping['Goals'] = self._add_key(element.goals, 'Goals')
        mapping['Notes'] = self._add_key(element.desc, 'Notes')
        return mapping

    def _get_sectionMapping(self, scId, sectionNumber, wordsTotal, firstInChapter=False):
        mapping = super()._get_sectionMapping(scId, sectionNumber, wordsTotal)
        element = self.novel.sections[scId]
        mapping = self._add_yaml(element, mapping)
        mapping['Desc'] = self._add_key(element.desc, 'Desc')
        mapping['Goal'] = self._add_key(element.goal, 'Goal')
        mapping['Conflict'] = self._add_key(element.conflict, 'Conflict')
        mapping['Outcome'] = self._add_key(element.outcome, 'Outcome')
        mapping['Notes'] = self._add_key(element.notes, 'Notes')
        mapping['SectionContent'] = self._add_key(element.sectionContent, 'Content')
        return mapping

    def _get_fileHeaderMapping(self):
        mapping = super()._get_fileHeaderMapping()
        element = self.novel
        mapping = self._add_yaml(element, mapping)
        mapping['Desc'] = self._add_key(element.desc, 'Desc')
        return mapping

    def _get_itemMapping(self, itId):
        mapping = super()._get_itemMapping(itId)
        element = self.novel.items[itId]
        mapping = self._add_yaml(element, mapping)
        mapping['Desc'] = self._add_key(element.desc, 'Desc')
        mapping['Notes'] = self._add_key(element.desc, 'Notes')
        return mapping

    def _get_locationMapping(self, lcId):
        mapping = super()._get_locationMapping(lcId)
        element = self.novel.locations[lcId]
        mapping = self._add_yaml(element, mapping)
        mapping['Desc'] = self._add_key(element.desc, 'Desc')
        mapping['Notes'] = self._add_key(element.desc, 'Notes')
        return mapping

    def _get_prjNoteMapping(self, pnId):
        mapping = super()._get_prjNoteMapping(pnId)
        element = self.novel.projectNotes[pnId]
        mapping = self._add_yaml(element, mapping)
        mapping['Desc'] = self._add_key(element.desc, 'Desc')
        return mapping

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
        xmlRoot = get_xml_root(self.filePath)
        try:
            locale = xmlRoot.attrib['{http://www.w3.org/XML/1998/namespace}lang']
            self.novel.languageCode, self.novel.countryCode = locale.split('-')
        except:
            pass
        self.novel.tree.reset()
        try:
            self._read_project(xmlRoot)
            self._read_locations(xmlRoot)
            self._read_items(xmlRoot)
            self._read_characters(xmlRoot)
            self._read_chapters_and_sections(xmlRoot)
            self._read_plot_lines_and_points(xmlRoot)
            self._read_project_notes(xmlRoot)
            self.adjust_section_types()
            self._read_word_count_log(xmlRoot)
        except Exception as ex:
            raise Error(f"{_('Corrupt project data')} ({str(ex)})")
        self._get_timestamp()
        self._keep_word_count()

    def write(self):
        super().write()
        self._get_timestamp()

    def _check_id(self, elemId, elemPrefix):
        """Raise an exception if elemId does not start with the correct prefix."""
        if not elemId.startswith(elemPrefix):
            raise Error(f"bad ID: '{elemId}'")

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

    def _read_chapters_and_sections(self, root):
        """Read data at chapter level from the xml element tree."""
        xmlChapters = root.find('CHAPTERS')
        if xmlChapters is None:
            return

        for xmlChapter in xmlChapters.iterfind('CHAPTER'):
            chId = xmlChapter.attrib['id']
            self._check_id(chId, CHAPTER_PREFIX)
            self.novel.chapters[chId] = Chapter(on_element_change=self.on_element_change)
            self.novel.chapters[chId].from_xml(xmlChapter)
            self.novel.tree.append(CH_ROOT, chId)

            for xmlSection in xmlChapter.iterfind('SECTION'):
                scId = xmlSection.attrib['id']
                self._check_id(scId, SECTION_PREFIX)
                self._read_section(xmlSection, scId)
                self.novel.tree.append(chId, scId)

    def _read_characters(self, root):
        """Read characters from the xml element tree."""
        xmlCharacters = root.find('CHARACTERS')
        if xmlCharacters is None:
            return

        for xmlCharacter in xmlCharacters.iterfind('CHARACTER'):
            crId = xmlCharacter.attrib['id']
            self._check_id(crId, CHARACTER_PREFIX)
            self.novel.characters[crId] = Character(on_element_change=self.on_element_change)
            self.novel.characters[crId].from_xml(xmlCharacter)
            self.novel.tree.append(CR_ROOT, crId)

    def _read_items(self, root):
        """Read items from the xml element tree."""
        xmlItems = root.find('ITEMS')
        if xmlItems is None:
            return

        for xmlItem in xmlItems.iterfind('ITEM'):
            itId = xmlItem.attrib['id']
            self._check_id(itId, ITEM_PREFIX)
            self.novel.items[itId] = WorldElement(on_element_change=self.on_element_change)
            self.novel.items[itId].from_xml(xmlItem)
            self.novel.tree.append(IT_ROOT, itId)

    def _read_locations(self, root):
        """Read locations from the xml element tree."""
        xmlLocations = root.find('LOCATIONS')
        if xmlLocations is None:
            return

        for xmlLocation in xmlLocations.iterfind('LOCATION'):
            lcId = xmlLocation.attrib['id']
            self._check_id(lcId, LOCATION_PREFIX)
            self.novel.locations[lcId] = WorldElement(on_element_change=self.on_element_change)
            self.novel.locations[lcId].from_xml(xmlLocation)
            self.novel.tree.append(LC_ROOT, lcId)

    def _read_plot_lines_and_points(self, root):
        """Read plot lines and plot points from the xml element tree."""
        xmlPlotLines = root.find('ARCS')
        if xmlPlotLines is None:
            return

        for xmlPlotLine in xmlPlotLines.iterfind('ARC'):
            plId = xmlPlotLine.attrib['id']
            self._check_id(plId, PLOT_LINE_PREFIX)
            self.novel.plotLines[plId] = PlotLine(on_element_change=self.on_element_change)
            self.novel.plotLines[plId].from_xml(xmlPlotLine)
            self.novel.tree.append(PL_ROOT, plId)

            # Remove dead references.
            self.novel.plotLines[plId].sections = intersection(self.novel.plotLines[plId].sections, self.novel.sections)

            # Create back references.
            for scId in self.novel.plotLines[plId].sections:
                self.novel.sections[scId].scPlotLines.append(plId)

            for xmlPlotPoint in xmlPlotLine.iterfind('POINT'):
                ppId = xmlPlotPoint.attrib['id']
                self._check_id(ppId, PLOT_POINT_PREFIX)
                self._read_plot_point(xmlPlotPoint, ppId, plId)
                self.novel.tree.append(plId, ppId)

    def _read_plot_point(self, xmlPlotPoint, ppId, plId):
        """Read a plot point from the xml element tree."""
        self.novel.plotPoints[ppId] = PlotPoint(on_element_change=self.on_element_change)
        self.novel.plotPoints[ppId].from_xml(xmlPlotPoint)

        # Verify section and create back reference.
        scId = self.novel.plotPoints[ppId].sectionAssoc
        if scId in self.novel.sections:
            self.novel.sections[scId].scPlotPoints[ppId] = plId
        else:
            self.novel.plotPoints[ppId].sectionAssoc = None

    def _read_project(self, root):
        """Read data at project level from the xml element tree."""
        xmlProject = root.find('PROJECT')
        if xmlProject is None:
            return

        self.novel.from_xml(xmlProject)

    def _read_project_notes(self, root):
        """Read project notes from the xml element tree."""
        xmlProjectNotes = root.find('PROJECTNOTES')
        if xmlProjectNotes is None:
            return

        for xmlProjectNote in xmlProjectNotes.iterfind('PROJECTNOTE'):
            pnId = xmlProjectNote.attrib['id']
            self._check_id(pnId, PRJ_NOTE_PREFIX)
            self.novel.projectNotes[pnId] = BasicElement()
            self.novel.projectNotes[pnId].from_xml(xmlProjectNote)
            self.novel.tree.append(PN_ROOT, pnId)

    def _read_section(self, xmlSection, scId):
        """Read data at section level from the xml element tree."""
        self.novel.sections[scId] = Section(on_element_change=self.on_element_change)
        self.novel.sections[scId].from_xml(xmlSection)

        # Remove dead references.
        self.novel.sections[scId].characters = intersection(self.novel.sections[scId].characters, self.novel.characters)
        self.novel.sections[scId].locations = intersection(self.novel.sections[scId].locations, self.novel.locations)
        self.novel.sections[scId].items = intersection(self.novel.sections[scId].items, self.novel.items)

    def _read_word_count_log(self, xmlRoot):
        """Read the word count log from the xml element tree."""
        xmlWclog = xmlRoot.find('PROGRESS')
        if xmlWclog is None:
            return

        for xmlWc in xmlWclog.iterfind('WC'):
            wcDate = verified_date(xmlWc.find('Date').text)
            wcCount = verified_int_string(xmlWc.find('Count').text)
            wcTotalCount = verified_int_string(xmlWc.find('WithUnused').text)
            if wcDate and wcCount and wcTotalCount:
                self.wcLog[wcDate] = [wcCount, wcTotalCount]

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

