"""Provide a class for json file import and export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import json

from mdnvlib.file.prj_file import PrjFile
from mdnvlib.json.basic_element_json import BasicElementJson
from mdnvlib.json.chapter_json import ChapterJson
from mdnvlib.json.character_json import CharacterJson
from mdnvlib.json.novel_json import NovelJson
from mdnvlib.json.plot_line_json import PlotLineJson
from mdnvlib.json.plot_point_json import PlotPointJson
from mdnvlib.json.section_json import SectionJson
from mdnvlib.json.world_element_json import WorldElementJson
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


class JsonFile(PrjFile):
    """JSON file representation."""
    EXTENSION = '.json'

    MAJOR_VERSION = 1
    MINOR_VERSION = 0

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.
        
        Positional arguments:
            filePath: str -- path to the mdnov file.
            
        Optional arguments:
            kwargs -- keyword arguments (not used here).            
        
        Extends the superclass constructor.
        """
        super().__init__(filePath)
        self.plotLineCnv = PlotLineJson()
        self.characterCnv = CharacterJson()
        self.chapterCnv = ChapterJson()
        self.novelCnv = NovelJson()
        self.worldElementCnv = WorldElementJson()
        self.basicElementCnv = BasicElementJson()
        self.sectionCnv = SectionJson()
        self.plotPointCnv = PlotPointJson()

    def read(self):
        """Parse the file and get the instance variables.
        
        Raise the "Error" exception in case of error. 
        Overrides the superclass method.
        """
        with open(self.filePath, 'r', encoding='utf-8') as f:
            jsonData = json.load(f)
        try:
            self._check_version(jsonData)
            jsonRoot = jsonData['mdnov']
            self._read_project(jsonRoot)
            self._read_locations(jsonRoot)
            self._read_items(jsonRoot)
            self._read_characters(jsonRoot)
            self._read_chapters_and_sections(jsonRoot)
            self._read_plot_lines_and_points(jsonRoot)
            self._read_project_notes(jsonRoot)
            self.adjust_section_types()
            self._read_word_count_log(jsonRoot)
        except Exception as ex:
            raise Error(f"{_('Corrupt project data')} ({str(ex)})")

        self._get_timestamp()
        self._keep_word_count()

    def write(self):
        """Write instance variables to the file.
        
        Raise the "Error" exception in case of error. 
        Overrides the superclass method.
        """
        self._update_word_count_log()
        self.adjust_section_types()
        jsonData = {
            'mdnov':{
                'version':f'{self.MAJOR_VERSION}.{self.MINOR_VERSION}',
            },
        }
        jsonRoot = jsonData['mdnov']
        self._build_project(jsonRoot)
        self._build_chapters_and_sections(jsonRoot)
        self._build_characters(jsonRoot)
        self._build_locations(jsonRoot)
        self._build_items(jsonRoot)
        self._build_plot_lines_and_points(jsonRoot)
        self._build_project_notes(jsonRoot)
        self._build_word_count_log(jsonRoot)
        with open(self.filePath, 'w', encoding='utf-8') as f:
            json.dump(jsonData, f, indent=2)
        self._get_timestamp()

    def _build_project(self, root):
        root['PROJECT'] = {}
        self.novelCnv.export_data(self.novel, root['PROJECT'])

    def _build_chapters_and_sections(self, root):
        jsonChapters = {}
        for chId in self.novel.tree.get_children(CH_ROOT):
            jsonChapters[chId] = {}
            self.chapterCnv.export_data(
                self.novel.chapters[chId],
                jsonChapters[chId]
            )
            jsonSections = {}
            for scId in self.novel.tree.get_children(chId):
                jsonSections[scId] = {}
                self.sectionCnv.export_data(
                    self.novel.sections[scId],
                    jsonSections[scId]
                )
            if jsonSections:
                jsonChapters[chId]['SECTIONS'] = jsonSections
        if jsonChapters:
            root['CHAPTERS'] = jsonChapters

    def _build_characters(self, root):
        jsonCharacters = {}
        for crId in self.novel.tree.get_children(CR_ROOT):
            jsonCharacters[crId] = {}
            self.characterCnv.export_data(
                self.novel.characters[crId],
                jsonCharacters[crId]
            )
        if jsonCharacters:
            root['CHARACTERS'] = jsonCharacters

    def _build_locations(self, root):
        jsonLocations = {}
        for lcId in self.novel.tree.get_children(LC_ROOT):
            jsonLocations[lcId] = {}
            self.worldElementCnv.export_data(
                self.novel.locations[lcId],
                jsonLocations[lcId]
            )
        if jsonLocations:
            root['LOCATIONS'] = jsonLocations

    def _build_items(self, root):
        jsonItems = {}
        for itId in self.novel.tree.get_children(IT_ROOT):
            jsonItems[itId] = {}
            self.worldElementCnv.export_data(
                self.novel.items[itId],
                jsonItems[itId]
            )
        if jsonItems:
            root['ITEMS'] = jsonItems

    def _build_plot_lines_and_points(self, root):
        jsonPlotLines = {}
        for plId in self.novel.tree.get_children(PL_ROOT):
            jsonPlotLines[plId] = {}
            self.plotLineCnv.export_data(
                self.novel.plotLines[plId],
                jsonPlotLines[plId]
            )
            jsonPoints = {}
            for ppId in self.novel.tree.get_children(plId):
                jsonPoints[ppId] = {}
                self.plotPointCnv.export_data(
                    self.novel.plotPoints[ppId],
                    jsonPoints[ppId]
                )
            if jsonPoints:
                jsonPlotLines[plId]['POINTS'] = jsonPoints
        if jsonPlotLines:
            root['ARCS'] = jsonPlotLines

    def _build_project_notes(self, root):
        jsonProjectNotes = {}
        for pnId in self.novel.tree.get_children(PN_ROOT):
            jsonProjectNotes[pnId] = {}
            self.basicElementCnv.export_data(
                self.novel.projectNotes[pnId],
                jsonProjectNotes[pnId]
            )
        if jsonProjectNotes:
            root['PROJECTNOTES'] = jsonProjectNotes

    def _build_word_count_log(self, root):
        if not self.wcLog:
            return

        jsonWcLog = {}
        wcLastCount = None
        wcLastTotalCount = None
        for wc in self.wcLog:
            if self.novel.saveWordCount:
                # Discard entries with unchanged word count.
                if (
                    self.wcLog[wc][0] == wcLastCount
                    and self.wcLog[wc][1] == wcLastTotalCount
                ):
                    continue

                wcLastCount = self.wcLog[wc][0]
                wcLastTotalCount = self.wcLog[wc][1]
                jsonWcLog[wc] = self.wcLog[wc]
        if jsonWcLog:
            root['PROGRESS'] = jsonWcLog

    def _check_version(self, jsonData):
        """Raise an exception if the jsonData element is not compatible with the supported DTD."""
        if not 'mdnov' in jsonData:
            raise Error(f'{_("No valid JSON root element found in file")}: "{norm_path(self.filePath)}".')
        try:
            majorVersionStr, minorVersionStr = jsonData['mdnov']['version'].split('.')
            majorVersion = int(majorVersionStr)
            minorVersion = int(minorVersionStr)
        except NotImplementedError:
            raise Error(f'{_("No valid version found in file")}: "{norm_path(self.filePath)}".')
        if majorVersion > self.MAJOR_VERSION:
            raise Error(_('The project "{}" was created with a newer mdnovel version.').format(norm_path(self.filePath)))
        elif majorVersion < self.MAJOR_VERSION:
            raise Error(_('The project "{}" was created with an outdated mdnovel version.').format(norm_path(self.filePath)))
        elif minorVersion > self.MINOR_VERSION:
            raise Error(_('The project "{}" was created with a newer mdnovel version.').format(norm_path(self.filePath)))

    def _read_chapters_and_sections(self, root):
        """Read data at chapter level from the json element tree."""
        jsonChapters = root.get('CHAPTERS', None)
        if jsonChapters is None:
            return

        for chId in jsonChapters:
            self._check_id(chId, CHAPTER_PREFIX)
            self.novel.chapters[chId] = Chapter(on_element_change=self.on_element_change)
            self.chapterCnv.import_data(
                self.novel.chapters[chId],
                jsonChapters[chId]
            )
            self.novel.tree.append(CH_ROOT, chId)

            jsonSections = jsonChapters[chId].get('SECTIONS', {})
            for scId in jsonSections:
                self._check_id(scId, SECTION_PREFIX)
                self._read_section(jsonSections[scId], scId)
                self.novel.tree.append(chId, scId)

    def _read_characters(self, root):
        """Read characters from the json element tree."""
        jsonCharacters = root.get('CHARACTERS', None)
        if jsonCharacters is None:
            return

        for crId in jsonCharacters:
            self._check_id(crId, CHARACTER_PREFIX)
            self.novel.characters[crId] = Character(on_element_change=self.on_element_change)
            self.characterCnv.import_data(
                self.novel.characters[crId],
                jsonCharacters[crId]
            )
            self.novel.tree.append(CR_ROOT, crId)

    def _read_items(self, root):
        """Read items from the json element tree."""
        jsonItems = root.get('ITEMS', None)
        if jsonItems is None:
            return

        for itId in jsonItems:
            self._check_id(itId, ITEM_PREFIX)
            self.novel.items[itId] = WorldElement(on_element_change=self.on_element_change)
            self.worldElementCnv.import_data(
                self.novel.items[itId],
                jsonItems[itId]
            )
            self.novel.tree.append(IT_ROOT, itId)

    def _read_locations(self, root):
        """Read locations from the json element tree."""
        jsonLocations = root.get('LOCATIONS')
        if jsonLocations is None:
            return

        for lcId in jsonLocations:
            self._check_id(lcId, LOCATION_PREFIX)
            self.novel.locations[lcId] = WorldElement(on_element_change=self.on_element_change)
            self.worldElementCnv.import_data(
                self.novel.locations[lcId],
                jsonLocations[lcId]
            )
            self.novel.tree.append(LC_ROOT, lcId)

    def _read_plot_lines_and_points(self, root):
        """Read plot lines and plot points from the json element tree."""
        jsonPlotLines = root.get('ARCS')
        if jsonPlotLines is None:
            return

        for plId in jsonPlotLines:
            self._check_id(plId, PLOT_LINE_PREFIX)
            self.novel.plotLines[plId] = PlotLine(on_element_change=self.on_element_change)
            self.plotLineCnv.import_data(
                self.novel.plotLines[plId],
                jsonPlotLines[plId]
            )
            self.novel.tree.append(PL_ROOT, plId)

            # Remove dead references.
            self.novel.plotLines[plId].sections = intersection(
                self.novel.plotLines[plId].sections,
                self.novel.sections
            )

            # Create back references.
            for scId in self.novel.plotLines[plId].sections:
                self.novel.sections[scId].scPlotLines.append(plId)

            jsonPlotPoints = jsonPlotLines[plId].get('POINTS', {})
            for ppId in jsonPlotPoints:
                self._check_id(ppId, PLOT_POINT_PREFIX)
                self._read_plot_point(jsonPlotPoints[ppId], ppId, plId)
                self.novel.tree.append(plId, ppId)

    def _read_plot_point(self, jsonPlotPoint, ppId, plId):
        """Read a plot point from the json element tree."""
        self.novel.plotPoints[ppId] = PlotPoint(on_element_change=self.on_element_change)
        self.plotPointCnv.import_data(
            self.novel.plotPoints[ppId],
            jsonPlotPoint
        )

        # Verify section and create back reference.
        scId = self.novel.plotPoints[ppId].sectionAssoc
        if scId in self.novel.sections:
            self.novel.sections[scId].scPlotPoints[ppId] = plId
        else:
            self.novel.plotPoints[ppId].sectionAssoc = None

    def _read_project(self, root):
        """Read data at project level from the json element tree."""
        jsonProject = root.get('PROJECT', None)
        if jsonProject is None:
            return

        self.novelCnv.import_data(
            self.novel,
            jsonProject
        )

    def _read_project_notes(self, root):
        """Read project notes from the json element tree."""
        jsonProjectNotes = root.get('PROJECTNOTES', None)
        if jsonProjectNotes is None:
            return

        for pnId in jsonProjectNotes:
            self._check_id(pnId, PRJ_NOTE_PREFIX)
            self.novel.projectNotes[pnId] = BasicElement()
            self.basicElementCnv.import_data(
                self.novel.projectNotes[pnId],
                jsonProjectNotes[pnId]
            )
            self.novel.tree.append(PN_ROOT, pnId)

    def _read_section(self, jsonSection, scId):
        """Read data at section level from the json element tree."""
        self.novel.sections[scId] = Section(on_element_change=self.on_element_change)
        self.sectionCnv.import_data(
            self.novel.sections[scId],
            jsonSection
        )

        # Remove dead references.
        self.novel.sections[scId].characters = intersection(
            self.novel.sections[scId].characters, self.novel.characters)
        self.novel.sections[scId].locations = intersection(
            self.novel.sections[scId].locations, self.novel.locations)
        self.novel.sections[scId].items = intersection(
            self.novel.sections[scId].items, self.novel.items)

    def _read_word_count_log(self, jsonRoot):
        """Read the word count log from the json element tree."""
        jsonWclog = jsonRoot.get('PROGRESS', None)
        if jsonWclog is None:
            return

        for wc in jsonWclog:
            self.wcLog[wc] = jsonWclog[wc]
