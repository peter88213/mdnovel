"""Provide a class for yWriter 7 file import and export.

yWriter file importers and exporters inherit from this class.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from datetime import datetime
from html import unescape
import os
import re

from mdnvlib.file.file import File
from mdnvlib.model.id_generator import create_id
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
from mdnvlib.novx_globals import list_to_string
from mdnvlib.novx_globals import norm_path
from mdnvlib.novx_globals import string_to_list
from mdnvlib.xml.xml_filter import strip_illegal_characters
from mdnvlib.xml.xml_fixer import XmlFixer
from mdnvlib.xml.xml_indent import indent
import xml.etree.ElementTree as ET


class Yw7File(File):
    """yWriter 7 project file representation."""
    DESCRIPTION = _('yWriter 7 project')
    EXTENSION = '.yw7'

    PRJ_KWVAR_YW7 = [
        'Field_WorkPhase',
        'Field_RenumberChapters',
        'Field_RenumberParts',
        'Field_RenumberWithinParts',
        'Field_RomanChapterNumbers',
        'Field_RomanPartNumbers',
        'Field_ChapterHeadingPrefix',
        'Field_ChapterHeadingSuffix',
        'Field_PartHeadingPrefix',
        'Field_PartHeadingSuffix',
        'Field_CustomGoal',
        'Field_CustomConflict',
        'Field_CustomOutcome',
        'Field_CustomChrBio',
        'Field_CustomChrGoals',
        'Field_SaveWordCount',
        'Field_LanguageCode',
        'Field_CountryCode',
        ]
    # list of the names of the project keyword variables

    CHP_KWVAR_YW7 = [
        'Field_NoNumber',
        'Field_ArcDefinition',
        'Field_Arc_Definition',
        ]
    # list of the names of the chapter keyword variables

    SCN_KWVAR_YW7 = [
        'Field_SceneArcs',
        'Field_SceneAssoc',
        'Field_CustomAR',
        'Field_SceneMode',
        ]
    # list of the names of the scene keyword variables

    CRT_KWVAR_YW7 = [
        'Field_Link',
        'Field_BirthDate',
        'Field_DeathDate',
        ]
    # list of the names of the character keyword variables

    LOC_KWVAR_YW7 = [
        'Field_Link',
        ]
    # list of the names of the location keyword variables

    ITM_KWVAR_YW7 = [
        'Field_Link',
        ]
    # list of the names of the item keyword variables

    _CDATA_TAGS = [
        'Title',
        'AuthorName',
        'Bio',
        'Desc',
        'FieldTitle1',
        'FieldTitle2',
        'FieldTitle3',
        'FieldTitle4',
        'LaTeXHeaderFile',
        'Tags',
        'AKA',
        'ImageFile',
        'FullName',
        'Goals',
        'Notes',
        'RTFFile',
        'SceneContent',
        'Outcome',
        'Goal',
        'Conflict'
        'Field_ChapterHeadingPrefix',
        'Field_ChapterHeadingSuffix',
        'Field_PartHeadingPrefix',
        'Field_PartHeadingSuffix',
        'Field_CustomGoal',
        'Field_CustomConflict',
        'Field_CustomOutcome',
        'Field_CustomChrBio',
        'Field_CustomChrGoals',
        'Field_ArcDefinition',
        'Field_SceneArcs',
        'Field_CustomAR',
        ]
    # Names of xml elements containing CDATA.
    # ElementTree.write omits CDATA tags, so they have to be inserted afterwards.

    STAGE_MARKER = 'stage'

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.
        
        Positional arguments:
            filePath: str -- path to the yw7 file.
            
        Optional arguments:
            kwargs -- keyword arguments (not used here).            
        
        Extends the superclass constructor.
        """
        super().__init__(filePath)
        self._nvSvc = kwargs['nv_service']
        self.tree = None
        # xml element tree of the yWriter project
        self.wcLog = {}
        self._ywApIds = None

    def is_locked(self):
        """Check whether the yw7 file is locked by yWriter.
        
        Return True if a .lock file placed by yWriter exists.
        Otherwise, return False. 
        """
        return os.path.isfile(f'{self.filePath}.lock')

    def read(self):
        """Parse the yWriter xml file and get the instance variables.
        
        Raise the "Error" exception in case of error. 
        Overrides the superclass method.
        """
        if self.is_locked():
            raise Error(f'{_("yWriter seems to be open. Please close first")}.')

        self._noteCounter = 0
        self._noteNumber = 0
        try:
            try:
                with open(self.filePath, 'r', encoding='utf-8') as f:
                    xmlText = f.read()
            except:
                # yw7 file may be UTF-16 encoded, with a wrong XML header (yWriter for iOS)
                with open(self.filePath, 'r', encoding='utf-16') as f:
                    xmlText = f.read()
        except:
            try:
                self.tree = ET.parse(self.filePath)
            except Exception as ex:
                raise Error(f'{_("Can not process file")} - {str(ex)}')

        xmlText = strip_illegal_characters(xmlText)
        root = ET.fromstring(xmlText)
        del xmlText
        # saving memory

        self._ywApIds = []
        self.wcLog = {}
        self._read_project(root)
        self._read_locations(root)
        self._read_items(root)
        self._read_characters(root)
        self._read_chapters(root)
        self._read_scenes(root)
        self._read_project_notes(root)

        #--- Read the word count log.
        xmlWclog = root.find('WCLog')
        if xmlWclog is not None:
            for xmlWc in xmlWclog.iterfind('WC'):
                wcDate = xmlWc.find('Date').text
                wcCount = xmlWc.find('Count').text
                wcTotalCount = xmlWc.find('TotalCount').text
                self.wcLog[wcDate] = [wcCount, wcTotalCount]

        #--- Initialize empty scene character/location/item lists.
        # This helps deleting orphaned XML list items when saving the file.
        # Also fix missing scene status as a tribute to defensive programming.
        for scId in self.novel.sections:
            if self.novel.sections[scId].characters is None:
                self.novel.sections[scId].characters = []
            if self.novel.sections[scId].locations is None:
                self.novel.sections[scId].locations = []
            if self.novel.sections[scId].items is None:
                self.novel.sections[scId].items = []
            if self.novel.sections[scId].status is None:
                self.novel.sections[scId].status = 1

    def write(self):
        """Write instance variables to the yWriter xml file.
        
        Open the yWriter xml file located at filePath and replace the instance variables 
        not being None. Create new XML elements if necessary.
        Raise the "Error" exception in case of error. 
        Overrides the superclass method.
        """
        if self.is_locked():
            raise Error(f'{_("yWriter seems to be open. Please close first")}.')

        self._noteCounter = 0
        self._noteNumber = 0
        self._build_element_tree()
        self._write_element_tree(self)
        self._postprocess_xml_file(self.filePath)

    def _build_element_tree(self):
        """Modify the yWriter project attributes of an existing xml element tree."""

        def isTrue(value):
            if value:
                return '1'

        def set_element(parent, tag, text, index):
            if text is not None:
                subelement = ET.Element(tag)
                parent.insert(index, subelement)
                subelement.text = text
                index += 1
            return index

        def build_scene_subtree(xmlScene, prjScn, plotPoint=False):
            i = 1
            i = set_element(xmlScene, 'Title', prjScn.title, i)
            if prjScn.desc is not None:
                ET.SubElement(xmlScene, 'Desc').text = prjScn.desc

            if not plotPoint:
                scTags = prjScn.tags
                # copy of the scene's property

            #--- Write scene type.
            #
            # This is how yWriter 7.1.3.0 writes the scene type:
            #
            # Type   |<Unused>|Field_SceneType>|scType
            # -------+--------+----------------+------
            # Normal | N/A    | N/A            | 0
            # Notes  | -1     | 1              | 1
            # Todo   | -1     | 2              | 2
            # Unused | -1     | 0              | 3

            scTypeEncoding = (
                (False, None),
                (True, '1'),
                (True, '2'),
                (True, '0'),
                )
            if plotPoint:
                scType = 2
            elif prjScn.scType in (0, None):
                scType = 0
            elif prjScn.scType > 1:
                scType = 2
                if not scTags:
                    scTags = [self.STAGE_MARKER]
                elif not self.STAGE_MARKER in scTags:
                    scTags.append(self.STAGE_MARKER)
            else:
                scType = 3
            yUnused, ySceneType = scTypeEncoding[scType]
            if yUnused:
                ET.SubElement(xmlScene, 'Unused').text = '-1'
            if ySceneType is not None:
                ET.SubElement(xmlSceneFields[scId], 'Field_SceneType').text = ySceneType
            if plotPoint:
                ET.SubElement(xmlScene, 'Status').text = '1'
            elif prjScn.status is not None:
                ET.SubElement(xmlScene, 'Status').text = str(prjScn.status)

            if plotPoint:
                ET.SubElement(xmlScene, 'SceneContent')
                return

            ET.SubElement(xmlScene, 'SceneContent').text = self._to_yw(prjScn.sectionContent)
            if prjScn.notes:
                ET.SubElement(xmlScene, 'Notes').text = prjScn.notes
            if scTags:
                ET.SubElement(xmlScene, 'Tags').text = list_to_string(scTags)
            if prjScn.appendToPrev:
                ET.SubElement(xmlScene, 'AppendToPrev').text = '-1'

            #--- Write scene start.
            if (prjScn.date) and (prjScn.time):
                separator = ' '
                dateTime = f'{prjScn.date}{separator}{prjScn.time}'
                ET.SubElement(xmlScene, 'SpecificDateTime').text = dateTime
                ET.SubElement(xmlScene, 'SpecificDateMode').text = '-1'
            elif (prjScn.day) or (prjScn.time):
                if prjScn.day:
                    ET.SubElement(xmlScene, 'Day').text = prjScn.day
                if prjScn.time:
                    hours, minutes, __ = prjScn.time.split(':')
                    ET.SubElement(xmlScene, 'Hour').text = hours
                    ET.SubElement(xmlScene, 'Minute').text = minutes

            #--- Write scene duration.
            if prjScn.lastsDays:
                ET.SubElement(xmlScene, 'LastsDays').text = prjScn.lastsDays
            if prjScn.lastsHours:
                ET.SubElement(xmlScene, 'LastsHours').text = prjScn.lastsHours
            if prjScn.lastsMinutes:
                ET.SubElement(xmlScene, 'LastsMinutes').text = prjScn.lastsMinutes

            # Plot related information
            if prjScn.scene == 2:
                ET.SubElement(xmlScene, 'ReactionScene').text = '-1'
            if prjScn.goal:
                ET.SubElement(xmlScene, 'Goal').text = prjScn.goal
            if prjScn.conflict:
                ET.SubElement(xmlScene, 'Conflict').text = prjScn.conflict
            if prjScn.outcome:
                ET.SubElement(xmlScene, 'Outcome').text = prjScn.outcome

            #--- Characters/locations/items
            if prjScn.characters:
                xmlCharacters = ET.SubElement(xmlScene, 'Characters')
                for crId in prjScn.characters:
                    ET.SubElement(xmlCharacters, 'CharID').text = crId[2:]
            if prjScn.locations:
                xmlLocations = ET.SubElement(xmlScene, 'Locations')
                for lcId in prjScn.locations:
                    ET.SubElement(xmlLocations, 'LocID').text = lcId[2:]
            if prjScn.items:
                xmlItems = ET.SubElement(xmlScene, 'Items')
                for itId in prjScn.items:
                    ET.SubElement(xmlItems, 'ItemID').text = itId[2:]

        def build_chapter_subtree(xmlChapter, prjChp, plId=None, chType=None):
            # This is how yWriter 7.1.3.0 writes the chapter type:
            #
            # Type   |<Unused>|<Type>|<ChapterType>|chType
            #--------+--------+------+-------------+------
            # Normal | N/A    | 0    | 0           | 0
            # Notes  | -1     | 1    | 1           | 1
            # Todo   | -1     | 1    | 2           | 2
            # Unused | -1     | 1    | 0           | 3

            chTypeEncoding = (
                (False, '0', '0'),
                (True, '1', '1'),
                (True, '1', '2'),
                (True, '1', '0'),
                )
            if chType is None:
                if plId is not None:
                    chType = 2
                elif prjChp.chType in (0, None):
                    chType = 0
                else:
                    chType = 3
            yUnused, yType, yChapterType = chTypeEncoding[chType]

            i = 1
            i = set_element(xmlChapter, 'Title', prjChp.title, i)
            i = set_element(xmlChapter, 'Desc', prjChp.desc, i)

            if yUnused:
                elem = ET.Element('Unused')
                elem.text = '-1'
                xmlChapter.insert(i, elem)
                i += 1

            #--- Write chapter fields.
            xmlChapterFields = ET.SubElement(xmlChapter, 'Fields')
            i += 1
            if plId is None and prjChp.isTrash:
                ET.SubElement(xmlChapterFields, 'Field_IsTrash').text = '1'

            #--- Write chapter custom fields.
            if plId is None:
                fields = { 'Field_NoNumber': isTrue(prjChp.noNumber)}
            else:
                fields = {'Field_ArcDefinition': self.novel.plotLines[plId].shortName}
            for field in fields:
                if fields[field]:
                    ET.SubElement(xmlChapterFields, field).text = fields[field]
            if plId is None and prjChp.chLevel == 1:
                ET.SubElement(xmlChapter, 'SectionStart').text = '-1'
                i += 1
            i = set_element(xmlChapter, 'Type', yType, i)
            i = set_element(xmlChapter, 'ChapterType', yChapterType, i)

        def build_location_subtree(xmlLoc, prjLoc):
            if prjLoc.title:
                ET.SubElement(xmlLoc, 'Title').text = prjLoc.title
            # if prjLoc.image:
            #    ET.SubElement(xmlLoc, 'ImageFile').text = prjLoc.image
            if prjLoc.desc:
                ET.SubElement(xmlLoc, 'Desc').text = prjLoc.desc
            if prjLoc.aka:
                ET.SubElement(xmlLoc, 'AKA').text = prjLoc.aka
            if prjLoc.tags:
                ET.SubElement(xmlLoc, 'Tags').text = list_to_string(prjLoc.tags)

        def build_item_subtree(xmlItm, prjItm):
            if prjItm.title:
                ET.SubElement(xmlItm, 'Title').text = prjItm.title
            # if prjItm.image:
            #     ET.SubElement(xmlItm, 'ImageFile').text = prjItm.image
            if prjItm.desc:
                ET.SubElement(xmlItm, 'Desc').text = prjItm.desc
            if prjItm.aka:
                ET.SubElement(xmlItm, 'AKA').text = prjItm.aka
            if prjItm.tags:
                ET.SubElement(xmlItm, 'Tags').text = list_to_string(prjItm.tags)

        def build_character_subtree(xmlCrt, prjCrt):
            if prjCrt.title:
                ET.SubElement(xmlCrt, 'Title').text = prjCrt.title
            if prjCrt.desc:
                ET.SubElement(xmlCrt, 'Desc').text = prjCrt.desc
            # if prjCrt.image:
            #    ET.SubElement(xmlCrt, 'ImageFile').text = prjCrt.image
            if prjCrt.notes:
                ET.SubElement(xmlCrt, 'Notes').text = prjCrt.notes
            if prjCrt.aka:
                ET.SubElement(xmlCrt, 'AKA').text = prjCrt.aka
            if prjCrt.tags:
                ET.SubElement(xmlCrt, 'Tags').text = list_to_string(prjCrt.tags)
            if prjCrt.bio:
                ET.SubElement(xmlCrt, 'Bio').text = prjCrt.bio
            if prjCrt.goals:
                ET.SubElement(xmlCrt, 'Goals').text = prjCrt.goals
            if prjCrt.fullName:
                ET.SubElement(xmlCrt, 'FullName').text = prjCrt.fullName
            if prjCrt.isMajor:
                ET.SubElement(xmlCrt, 'Major').text = '-1'
            fields = {
                'Field_BirthDate': prjCrt.birthDate,
                'Field_DeathDate': prjCrt.deathDate,
                }
            xmlCrtFields = None
            for field in fields:
                if fields[field]:
                    if xmlCrtFields is None:
                        xmlCrtFields = ET.SubElement(xmlCrt, 'Fields')
                    ET.SubElement(xmlCrtFields, field).text = fields[field]

        def build_project_subtree(xmlProject):
            ET.SubElement(xmlProject, 'Ver').text = '7'
            if self.novel.title:
                ET.SubElement(xmlProject, 'Title').text = self.novel.title
            if self.novel.desc:
                ET.SubElement(xmlProject, 'Desc').text = self.novel.desc
            if self.novel.authorName:
                ET.SubElement(xmlProject, 'AuthorName').text = self.novel.authorName
            if self.novel.wordCountStart is not None:
                ET.SubElement(xmlProject, 'WordCountStart').text = str(self.novel.wordCountStart)
            if self.novel.wordTarget is not None:
                ET.SubElement(xmlProject, 'WordTarget').text = str(self.novel.wordTarget)

            # Write project custom fields.
            workPhase = self.novel.workPhase
            if workPhase is not None:
                workPhase = str(workPhase)
            fields = {
                'Field_WorkPhase': workPhase,
                'Field_RenumberChapters': isTrue(self.novel.renumberChapters),
                'Field_RenumberParts': isTrue(self.novel.renumberParts),
                'Field_RenumberWithinParts': isTrue(self.novel.renumberWithinParts),
                'Field_RomanChapterNumbers': isTrue(self.novel.romanChapterNumbers),
                'Field_RomanPartNumbers': isTrue(self.novel.romanPartNumbers),
                'Field_ChapterHeadingPrefix': self.novel.chapterHeadingPrefix,
                'Field_ChapterHeadingSuffix': self.novel.chapterHeadingSuffix,
                'Field_PartHeadingPrefix': self.novel.partHeadingPrefix,
                'Field_PartHeadingSuffix': self.novel.partHeadingSuffix,
                'Field_CustomGoal': self.novel.customGoal,
                'Field_CustomConflict': self.novel.customConflict,
                'Field_CustomOutcome': self.novel.customOutcome,
                'Field_CustomChrBio': self.novel.customChrBio,
                'Field_CustomChrGoals': self.novel.customChrGoals,
                'Field_SaveWordCount': isTrue(self.novel.saveWordCount),
                'Field_ReferenceDate': self.novel.referenceDate,
                }
            xmlProjectFields = ET.SubElement(xmlProject, 'Fields')
            for field in fields:
                if fields[field]:
                    ET.SubElement(xmlProjectFields, field).text = fields[field]

        def build_prjNote_subtree(xmlProjectnote, projectNote):
            if projectNote.title is not None:
                ET.SubElement(xmlProjectnote, 'Title').text = projectNote.title

            if projectNote.desc is not None:
                ET.SubElement(xmlProjectnote, 'Desc').text = projectNote.desc

        #--- Build a new tree.
        root = ET.Element('YWRITER7')
        xmlProject = ET.SubElement(root, 'PROJECT')
        xmlLocations = ET.SubElement(root, 'LOCATIONS')
        xmlItems = ET.SubElement(root, 'ITEMS')
        xmlCharacters = ET.SubElement(root, 'CHARACTERS')
        xmlScenes = ET.SubElement(root, 'SCENES')
        xmlChapters = ET.SubElement(root, 'CHAPTERS')

        #--- Process project.
        build_project_subtree(xmlProject)

        #--- Process locations.
        for lcId in self.novel.tree.get_children(LC_ROOT):
            xmlLoc = ET.SubElement(xmlLocations, 'LOCATION')
            ET.SubElement(xmlLoc, 'ID').text = lcId[2:]
            build_location_subtree(xmlLoc, self.novel.locations[lcId])

        #--- Process items.
        for itId in self.novel.tree.get_children(IT_ROOT):
            xmlItm = ET.SubElement(xmlItems, 'ITEM')
            ET.SubElement(xmlItm, 'ID').text = itId[2:]
            build_item_subtree(xmlItm, self.novel.items[itId])

        #--- Process characters.
        for crId in self.novel.tree.get_children(CR_ROOT):
            xmlCrt = ET.SubElement(xmlCharacters, 'CHARACTER')
            ET.SubElement(xmlCrt, 'ID').text = crId[2:]
            build_character_subtree(xmlCrt, self.novel.characters[crId])

        #--- Process scenes.
        xmlSceneFields = {}
        scIds = list(self.novel.sections)
        for scId in scIds:
            xmlScene = ET.SubElement(xmlScenes, 'SCENE')
            ET.SubElement(xmlScene, 'ID').text = scId[2:]
            xmlSceneFields[scId] = ET.SubElement(xmlScene, 'Fields')
            build_scene_subtree(xmlScene, self.novel.sections[scId])

        #--- Process plot points.
        newScIds = {}
        # new scene IDs by plot point ID
        for ppId in self.novel.plotPoints:
            scId = create_id(scIds, prefix=SECTION_PREFIX)
            scIds.append(scId)
            newScIds[ppId] = scId
            xmlScene = ET.SubElement(xmlScenes, 'SCENE')
            ET.SubElement(xmlScene, 'ID').text = scId[2:]
            xmlSceneFields[scId] = ET.SubElement(xmlScene, 'Fields')
            build_scene_subtree(xmlScene, self.novel.plotPoints[ppId], plotPoint=True)

        #--- Process chapters.
        chIds = list(self.novel.tree.get_children(CH_ROOT))
        for chId in chIds:
            xmlChapter = ET.SubElement(xmlChapters, 'CHAPTER')
            ET.SubElement(xmlChapter, 'ID').text = chId[2:]
            build_chapter_subtree(xmlChapter, self.novel.chapters[chId])
            srtScenes = self.novel.tree.get_children(chId)
            if srtScenes:
                xmlScnList = ET.SubElement(xmlChapter, 'Scenes')
                for scId in self.novel.tree.get_children(chId):
                    ET.SubElement(xmlScnList, 'ScID').text = scId[2:]

        #--- Process plot lines.
        chId = create_id(chIds, prefix=CHAPTER_PREFIX)
        chIds.append(chId)
        xmlChapter = ET.SubElement(xmlChapters, 'CHAPTER')
        ET.SubElement(xmlChapter, 'ID').text = chId[2:]
        arcPart = self._nvSvc.make_chapter(title=_('Plot lines'), chLevel=1)
        build_chapter_subtree(xmlChapter, arcPart, chType=2)
        for plId in self.novel.tree.get_children(PL_ROOT):
            chId = create_id(chIds, prefix=CHAPTER_PREFIX)
            chIds.append(chId)
            xmlChapter = ET.SubElement(xmlChapters, 'CHAPTER')
            ET.SubElement(xmlChapter, 'ID').text = chId[2:]
            build_chapter_subtree(xmlChapter, self.novel.plotLines[plId], plId=plId)
            srtScenes = self.novel.tree.get_children(plId)
            if srtScenes:
                xmlScnList = ET.SubElement(xmlChapter, 'Scenes')
                for ppId in srtScenes:
                    ET.SubElement(xmlScnList, 'ScID').text = newScIds[ppId][2:]

        #--- Process project notes.
        if self.novel.tree.get_children(PN_ROOT):
            xmlProjectnotes = ET.SubElement(root, 'PROJECTNOTES')
            for pnId in self.novel.tree.get_children(PN_ROOT):
                xmlProjectnote = ET.SubElement(xmlProjectnotes, 'PROJECTNOTE')
                ET.SubElement(xmlProjectnote, 'ID').text = pnId[2:]
                build_prjNote_subtree(xmlProjectnote, self.novel.projectNotes[pnId])

        #--- Add plot line/scene references.
        scPlotLines = {}
        sectionAssoc = {}
        for scId in scIds:
            scPlotLines[scId] = []
            sectionAssoc[scId] = []
        for plId in self.novel.plotLines:
            for scId in self.novel.plotLines[plId].sections:
                scPlotLines[scId].append(self.novel.plotLines[plId].shortName)
            for ppId in self.novel.tree.get_children(plId):
                scPlotLines[newScIds[ppId]].append(self.novel.plotLines[plId].shortName)
        for ppId in self.novel.plotPoints:
            if self.novel.plotPoints[ppId].sectionAssoc:
                sectionAssoc[self.novel.plotPoints[ppId].sectionAssoc].append(newScIds[ppId][2:])
                sectionAssoc[newScIds[ppId]].append(self.novel.plotPoints[ppId].sectionAssoc[2:])
        for scId in scIds:
            fields = {
                'Field_SceneArcs': list_to_string(scPlotLines[scId]),
                'Field_SceneAssoc': list_to_string(sectionAssoc[scId]),
                }
            for field in fields:
                if fields[field]:
                    ET.SubElement(xmlSceneFields[scId], field).text = fields[field]

        #--- Build the word count log.
        if self.wcLog:
            xmlWcLog = ET.SubElement(root, 'WCLog')
            wcLastCount = None
            wcLastTotalCount = None
            for wc in self.wcLog:
                if self.novel.saveWordCount:
                    # Discard entries with unchanged word count.
                    if self.wcLog[wc][0] == wcLastCount and self.wcLog[wc][1] == wcLastTotalCount:
                        continue

                    wcLastCount = self.wcLog[wc][0]
                    wcLastTotalCount = self.wcLog[wc][1]
                xmlWc = ET.SubElement(xmlWcLog, 'WC')
                ET.SubElement(xmlWc, 'Date').text = wc
                ET.SubElement(xmlWc, 'Count').text = self.wcLog[wc][0]
                ET.SubElement(xmlWc, 'TotalCount').text = self.wcLog[wc][1]

        #--- Prepare the XML tree for saving.
        indent(root)
        self.tree = ET.ElementTree(root)

    def _from_yw(self, text, quick=False):
        """Return text, converted from yw7 markup to Markdown.
        
        Positional arguments:
            text -- string to convert.
        
        Optional arguments:
            quick -- bool: if True, apply a conversion mode for one-liners without formatting. 
        """
        if quick:
            # Just clean up a one-liner without sophisticated formatting.
            if text is None:
                return ''
            else:
                return text

        MD_REPLACEMENTS = [
            ('\n', '\n\n'),
            ('[i] ', ' [i]'),
            ('[b] ', ' [b]'),
            ('[s] ', ' [s]'),
            ('[i]', '*'),
            ('[/i]', '*'),
            ('[b]', '**'),
            ('[/b]', '**'),
            ('/*', '<!---'),
            ('*/', '--->'),
            ('  ', ' '),
        ]
        try:
            for yw, md in MD_REPLACEMENTS:
                text = text.replace(yw, md)
            text = re.sub(r'\[\/*[h|c|r|s|u]\d*\]', '', text)
            # Remove highlighting, alignment, and underline tags
        except AttributeError:
            text = ''
        return text

    def _postprocess_xml_file(self, filePath):
        """Postprocess an xml file created by ElementTree.
        
        Positional argument:
            filePath: str -- path to xml file.
        
        Read the xml file, put a header on top, insert the missing CDATA tags,
        and replace xml entities by plain text (unescape). Overwrite the .yw7 xml file.
        Raise the "Error" exception in case of error. 
        
        Note: The path is given as an argument rather than using self.filePath. 
        So this routine can be used for yWriter-generated xml files other than .yw7 as well. 
        """
        with open(filePath, 'r', encoding='utf-8') as f:
            text = f.read()
        lines = text.split('\n')
        newlines = ['<?xml version="1.0" encoding="utf-8"?>']
        for line in lines:
            for tag in self._CDATA_TAGS:
                line = re.sub(fr'\<{tag}\>', f'<{tag}><![CDATA[', line)
                line = re.sub(fr'\<\/{tag}\>', f']]></{tag}>', line)
            newlines.append(line)
        text = '\n'.join(newlines)
        text = text.replace('[CDATA[ \n', '[CDATA[')
        text = text.replace('\n]]', ']]')
        if not self.novel.chapters:
            text = text.replace('<CHAPTERS />', '<CHAPTERS></CHAPTERS>')
            # otherwise, yWriter fails to parse the file if there are no chapters.
        text = unescape(text)
        try:
            with open(filePath, 'w', encoding='utf-8') as f:
                f.write(text)
        except:
            raise Error(f'{_("Cannot write file")}: "{norm_path(filePath)}".')

    def _read_locations(self, root):
        """Read locations from the xml element tree."""
        self.novel.tree.delete_children(LC_ROOT)
        # This is necessary for re-reading.
        for xmlLocation in root.find('LOCATIONS'):
            lcId = f"{LOCATION_PREFIX}{xmlLocation.find('ID').text}"
            self.novel.tree.append(LC_ROOT, lcId)
            self.novel.locations[lcId] = self._nvSvc.make_world_element()

            if xmlLocation.find('Title') is not None:
                self.novel.locations[lcId].title = xmlLocation.find('Title').text

            # if xmlLocation.find('ImageFile') is not None:
            #    self.novel.locations[lcId].image = xmlLocation.find('ImageFile').text

            if xmlLocation.find('Desc') is not None:
                self.novel.locations[lcId].desc = xmlLocation.find('Desc').text

            if xmlLocation.find('AKA') is not None:
                self.novel.locations[lcId].aka = xmlLocation.find('AKA').text

            if xmlLocation.find('Tags') is not None:
                if xmlLocation.find('Tags').text is not None:
                    tags = string_to_list(xmlLocation.find('Tags').text)
                    self.novel.locations[lcId].tags = self._strip_spaces(tags)

    def _read_items(self, root):
        """Read items from the xml element tree."""
        self.novel.tree.delete_children(IT_ROOT)
        # This is necessary for re-reading.
        for xmlItem in root.find('ITEMS'):
            itId = f"{ITEM_PREFIX}{xmlItem.find('ID').text}"
            self.novel.tree.append(IT_ROOT, itId)
            self.novel.items[itId] = self._nvSvc.make_world_element()

            if xmlItem.find('Title') is not None:
                self.novel.items[itId].title = xmlItem.find('Title').text

            # if xmlItem.find('ImageFile') is not None:
            #    self.novel.items[itId].image = xmlItem.find('ImageFile').text

            if xmlItem.find('Desc') is not None:
                self.novel.items[itId].desc = xmlItem.find('Desc').text

            if xmlItem.find('AKA') is not None:
                self.novel.items[itId].aka = xmlItem.find('AKA').text

            if xmlItem.find('Tags') is not None:
                if xmlItem.find('Tags').text is not None:
                    tags = string_to_list(xmlItem.find('Tags').text)
                    self.novel.items[itId].tags = self._strip_spaces(tags)

    def _read_chapters(self, root):
        """Read attributes at chapter level from the xml element tree."""
        self.novel.tree.delete_children(CH_ROOT)
        self.novel.tree.delete_children(PL_ROOT)
        # This is necessary for re-reading.
        for xmlChapter in root.find('CHAPTERS'):
            prjChapter = self._nvSvc.make_chapter()

            if xmlChapter.find('Title') is not None:
                prjChapter.title = xmlChapter.find('Title').text

            if xmlChapter.find('Desc') is not None:
                prjChapter.desc = xmlChapter.find('Desc').text

            if xmlChapter.find('SectionStart') is not None:
                prjChapter.chLevel = 1
            else:
                prjChapter.chLevel = 2

            # This is how yWriter 7.1.3.0 reads the chapter type:
            #
            # Type   |<Unused>|<Type>|<ChapterType>|chType
            # -------+--------+------+--------------------
            # Normal | N/A    | N/A  | N/A         | 0
            # Normal | N/A    | 0    | N/A         | 0
            # Notes  | x      | 1    | N/A         | 1
            # Unused | -1     | 0    | N/A         | 1
            # Normal | N/A    | x    | 0           | 0
            # Notes  | x      | x    | 1           | 1
            # Todo   | x      | x    | 2           | 1
            # Unused | -1     | x    | x           | 1

            prjChapter.chType = 0
            if xmlChapter.find('Unused') is not None:
                yUnused = True
            else:
                yUnused = False
            if xmlChapter.find('ChapterType') is not None:
                # The file may be created with yWriter version 7.0.7.2+
                yChapterType = xmlChapter.find('ChapterType').text
                if yChapterType == '2':
                    prjChapter.chType = 1
                elif yChapterType == '1':
                    prjChapter.chType = 1
                elif yUnused:
                    prjChapter.chType = 1
            else:
                # The file may be created with a yWriter version prior to 7.0.7.2
                if xmlChapter.find('Type') is not None:
                    yType = xmlChapter.find('Type').text
                    if yType == '1':
                        prjChapter.chType = 1
                    elif yUnused:
                        prjChapter.chType = 1

            #--- Read chapter fields.
            kwVarYw7 = {}
            for xmlChapterFields in xmlChapter.iterfind('Fields'):
                prjChapter.isTrash = False
                if xmlChapterFields.find('Field_IsTrash') is not None:
                    if xmlChapterFields.find('Field_IsTrash').text == '1':
                        prjChapter.isTrash = True

                #--- Read chapter custom fields.
                for fieldName in self.CHP_KWVAR_YW7:
                    xmlField = xmlChapterFields.find(fieldName)
                    if xmlField  is not None:
                        kwVarYw7[fieldName] = xmlField .text
            prjChapter.noNumber = kwVarYw7.get('Field_NoNumber', False) == '1'
            shortName = kwVarYw7.get('Field_ArcDefinition', '')

            # This is for projects written with novelibre v4.3:
            field = kwVarYw7.get('Field_Arc_Definition', None)
            if field is not None:
                shortName = field

            #--- Read chapter's scene list.
            scenes = []
            if xmlChapter.find('Scenes') is not None:
                for scn in xmlChapter.find('Scenes').iterfind('ScID'):
                    scId = scn.text
                    scenes.append(scId)

            if shortName:
                plId = f"{PLOT_LINE_PREFIX}{xmlChapter.find('ID').text}"
                self.novel.plotLines[plId] = self._nvSvc.make_plot_line()
                self.novel.plotLines[plId].title = prjChapter.title
                self.novel.plotLines[plId].desc = prjChapter.desc
                self.novel.plotLines[plId].shortName = shortName
                self.novel.tree.append(PL_ROOT, plId)
                for scId in scenes:
                    self.novel.tree.append(plId, f'{PLOT_POINT_PREFIX}{scId}')
                    self._ywApIds.append(scId)
                    # this is necessary for turning yWriter scenes into mdnovel turning points
            else:
                chId = f"{CHAPTER_PREFIX}{xmlChapter.find('ID').text}"
                self.novel.chapters[chId] = prjChapter
                self.novel.tree.append(CH_ROOT, chId)
                for scId in scenes:
                    self.novel.tree.append(chId, f'{SECTION_PREFIX}{scId}')

    def _read_characters(self, root):
        """Read characters from the xml element tree."""
        self.novel.tree.delete_children(CR_ROOT)
        # This is necessary for re-reading.
        for xmlCharacter in root.find('CHARACTERS'):
            crId = f"{CHARACTER_PREFIX}{xmlCharacter.find('ID').text}"
            self.novel.tree.append(CR_ROOT, crId)
            self.novel.characters[crId] = self._nvSvc.make_character()

            if xmlCharacter.find('Title') is not None:
                self.novel.characters[crId].title = xmlCharacter.find('Title').text

            # if xmlCharacter.find('ImageFile') is not None:
            #    self.novel.characters[crId].image = xmlCharacter.find('ImageFile').text
            # TODO: read link

            if xmlCharacter.find('Desc') is not None:
                self.novel.characters[crId].desc = xmlCharacter.find('Desc').text

            if xmlCharacter.find('AKA') is not None:
                self.novel.characters[crId].aka = xmlCharacter.find('AKA').text

            if xmlCharacter.find('Tags') is not None:
                if xmlCharacter.find('Tags').text is not None:
                    tags = string_to_list(xmlCharacter.find('Tags').text)
                    self.novel.characters[crId].tags = self._strip_spaces(tags)

            if xmlCharacter.find('Notes') is not None:
                self.novel.characters[crId].notes = xmlCharacter.find('Notes').text

            if xmlCharacter.find('Bio') is not None:
                self.novel.characters[crId].bio = xmlCharacter.find('Bio').text

            if xmlCharacter.find('Goals') is not None:
                self.novel.characters[crId].goals = xmlCharacter.find('Goals').text

            if xmlCharacter.find('FullName') is not None:
                self.novel.characters[crId].fullName = xmlCharacter.find('FullName').text

            if xmlCharacter.find('Major') is not None:
                self.novel.characters[crId].isMajor = True
            else:
                self.novel.characters[crId].isMajor = False
                #--- Read scene custom fields.

            kwVarYw7 = {}
            xmlCharacterFields = xmlCharacter.find('Fields')
            if xmlCharacterFields is not None:
                for fieldName in self.CRT_KWVAR_YW7:
                    xmlField = xmlCharacterFields.find(fieldName)
                    if xmlField  is not None:
                        kwVarYw7[fieldName] = xmlField.text
            self.novel.characters[crId].birthDate = kwVarYw7.get('Field_BirthDate', '')
            self.novel.characters[crId].deathDate = kwVarYw7.get('Field_DeathDate', '')

    def _read_project(self, root):
        """Read attributes at project level from the xml element tree."""
        xmlProject = root.find('PROJECT')

        if xmlProject.find('Title') is not None:
            self.novel.title = xmlProject.find('Title').text

        if xmlProject.find('AuthorName') is not None:
            self.novel.authorName = xmlProject.find('AuthorName').text

        if xmlProject.find('Desc') is not None:
            self.novel.desc = xmlProject.find('Desc').text

        #--- Read word target data.
        if xmlProject.find('WordCountStart') is not None:
            try:
                self.novel.wordCountStart = int(xmlProject.find('WordCountStart').text)
            except:
                pass
        if xmlProject.find('WordTarget') is not None:
            try:
                self.novel.wordTarget = int(xmlProject.find('WordTarget').text)
            except:
                pass

        #--- Read project custom fields.
        kwVarYw7 = {}
        for xmlProjectFields in xmlProject.iterfind('Fields'):
            for fieldName in self.PRJ_KWVAR_YW7:
                xmlField = xmlProjectFields.find(fieldName)
                if xmlField  is not None:
                    if xmlField.text:
                        kwVarYw7[fieldName] = xmlField.text
        try:
            self.novel.workPhase = int(kwVarYw7.get('Field_WorkPhase', None))
        except:
            self.novel.workPhase = None
        self.novel.renumberChapters = kwVarYw7.get('Field_RenumberChapters', False) == '1'
        self.novel.renumberParts = kwVarYw7.get('Field_RenumberParts', False) == '1'
        self.novel.renumberWithinParts = kwVarYw7.get('Field_RenumberWithinParts', False) == '1'
        self.novel.romanChapterNumbers = kwVarYw7.get('Field_RomanChapterNumbers', False) == '1'
        self.novel.romanPartNumbers = kwVarYw7.get('Field_RomanPartNumbers', False) == '1'
        self.novel.chapterHeadingPrefix = kwVarYw7.get('Field_ChapterHeadingPrefix', '')
        self.novel.chapterHeadingSuffix = kwVarYw7.get('Field_ChapterHeadingSuffix', '')
        self.novel.partHeadingPrefix = kwVarYw7.get('Field_PartHeadingPrefix', '')
        self.novel.partHeadingSuffix = kwVarYw7.get('Field_PartHeadingSuffix', '')
        self.novel.customGoal = kwVarYw7.get('Field_CustomGoal', '')
        self.novel.customConflict = kwVarYw7.get('Field_CustomConflict', '')
        self.novel.customOutcome = kwVarYw7.get('Field_CustomOutcome', '')
        self.novel.customChrBio = kwVarYw7.get('Field_CustomChrBio', '')
        self.novel.customChrGoals = kwVarYw7.get('Field_CustomChrGoals', '')
        self.novel.saveWordCount = kwVarYw7.get('Field_SaveWordCount', False) == '1'

    def _read_project_notes(self, root):
        """Read project notes from the xml element tree.
        
        If any, create "Notes" scenes in the "Project notes" chapter.
        """
        if root.find('PROJECTNOTES') is not None:
            for xmlProjectnote in root.find('PROJECTNOTES'):
                if xmlProjectnote.find('ID') is not None:
                    pnId = f"{PRJ_NOTE_PREFIX}{xmlProjectnote.find('ID').text}"
                    self.novel.tree.append(PN_ROOT, pnId)
                    self.novel.projectNotes[pnId] = self._nvSvc.make_basic_element()
                    if xmlProjectnote.find('Title') is not None:
                        self.novel.projectNotes[pnId].title = xmlProjectnote.find('Title').text
                    if xmlProjectnote.find('Desc') is not None:
                        self.novel.projectNotes[pnId].desc = xmlProjectnote.find('Desc').text

    def _read_scenes(self, root):
        """ Read attributes at scene level from the xml element tree."""
        for xmlScene in root.find('SCENES'):
            prjScn = self._nvSvc.make_section()

            if xmlScene.find('Title') is not None:
                prjScn.title = xmlScene.find('Title').text

            if xmlScene.find('Desc') is not None:
                prjScn.desc = xmlScene.find('Desc').text

            if xmlScene.find('SceneContent') is not None:
                sceneContent = xmlScene.find('SceneContent').text
                if sceneContent is not None:
                    prjScn.sectionContent = self._from_yw(sceneContent)

            #--- Read scene type.

            # This is how yWriter 7.1.3.0 reads the scene type:
            #
            # Type   |<Unused>|Field_SceneType>|scType
            #--------+--------+----------------+------
            # Notes  | x      | 1              | 1
            # Todo   | x      | 2              | 1
            # Unused | -1     | N/A            | 1
            # Unused | -1     | 0              | 1
            # Normal | N/A    | N/A            | 0
            # Normal | N/A    | 0              | 0

            prjScn.scType = 0
            kwVarYw7 = {}
            for xmlSceneFields in xmlScene.iterfind('Fields'):
                # Read scene type, if any.
                if xmlSceneFields.find('Field_SceneType') is not None:
                    if xmlSceneFields.find('Field_SceneType').text == '1':
                        prjScn.scType = 1
                    elif xmlSceneFields.find('Field_SceneType').text == '2':
                        prjScn.scType = 1

                #--- Read scene custom fields.
                for fieldName in self.SCN_KWVAR_YW7:
                    xmlField = xmlSceneFields.find(fieldName)
                    if xmlField  is not None:
                        kwVarYw7[fieldName] = xmlField.text

            ywScnArcs = string_to_list(kwVarYw7.get('Field_SceneArcs', ''))
            for shortName in ywScnArcs:
                for plId in self.novel.plotLines:
                    if self.novel.plotLines[plId].shortName == shortName:
                        if prjScn.scType == 0:
                            arcSections = self.novel.plotLines[plId].sections
                            if not arcSections:
                                arcSections = [f"{SECTION_PREFIX}{xmlScene.find('ID').text}"]
                            else:
                                arcSections.append(f"{SECTION_PREFIX}{xmlScene.find('ID').text}")
                            self.novel.plotLines[plId].sections = arcSections
                        break

            ywScnAssocs = string_to_list(kwVarYw7.get('Field_SceneAssoc', ''))
            prjScn.plotPoints = [f'{PLOT_POINT_PREFIX}{plotPoint}' for plotPoint in ywScnAssocs]

            if xmlScene.find('Goal') is not None:
                prjScn.goal = xmlScene.find('Goal').text

            if xmlScene.find('Conflict') is not None:
                prjScn.conflict = xmlScene.find('Conflict').text

            if xmlScene.find('Outcome') is not None:
                prjScn.outcome = xmlScene.find('Outcome').text

            if kwVarYw7.get('Field_CustomAR', None) is not None:
                prjScn.scene = 3
            elif xmlScene.find('ReactionScene') is not None:
                prjScn.scene = 2
            elif prjScn.goal or prjScn.conflict or prjScn.outcome:
                prjScn.scene = 1
            else:
                prjScn.scene = 0

            # Unused.
            if xmlScene.find('Unused') is not None:
                if prjScn.scType == 0:
                    prjScn.scType = 1

            if xmlScene.find('Status') is not None:
                prjScn.status = int(xmlScene.find('Status').text)

            if xmlScene.find('Notes') is not None:
                prjScn.notes = xmlScene.find('Notes').text

            if xmlScene.find('Tags') is not None:
                if xmlScene.find('Tags').text is not None:
                    tags = string_to_list(xmlScene.find('Tags').text)
                    prjScn.tags = self._strip_spaces(tags)

            if xmlScene.find('AppendToPrev') is not None:
                prjScn.appendToPrev = True
            else:
                prjScn.appendToPrev = False

            #--- Scene start.
            if xmlScene.find('SpecificDateTime') is not None:
                dateTimeStr = xmlScene.find('SpecificDateTime').text

                # Check SpecificDateTime for ISO compliance.
                try:
                    dateTime = datetime.fromisoformat(dateTimeStr)
                except:
                    prjScn.date = ''
                    prjScn.time = ''
                else:
                    startDateTime = dateTime.isoformat().split('T')
                    prjScn.date = startDateTime[0]
                    prjScn.time = startDateTime[1]
            else:
                if xmlScene.find('Day') is not None:
                    day = xmlScene.find('Day').text

                    # Check if Day represents an integer.
                    try:
                        int(day)
                    except ValueError:
                        day = ''
                    prjScn.day = day

                hasUnspecificTime = False
                if xmlScene.find('Hour') is not None:
                    hour = xmlScene.find('Hour').text.zfill(2)
                    hasUnspecificTime = True
                else:
                    hour = '00'
                if xmlScene.find('Minute') is not None:
                    minute = xmlScene.find('Minute').text.zfill(2)
                    hasUnspecificTime = True
                else:
                    minute = '00'
                if hasUnspecificTime:
                    prjScn.time = f'{hour}:{minute}:00'

            #--- Scene duration.
            if xmlScene.find('LastsDays') is not None:
                prjScn.lastsDays = xmlScene.find('LastsDays').text

            if xmlScene.find('LastsHours') is not None:
                prjScn.lastsHours = xmlScene.find('LastsHours').text

            if xmlScene.find('LastsMinutes') is not None:
                prjScn.lastsMinutes = xmlScene.find('LastsMinutes').text

            # if xmlScene.find('ImageFile') is not None:
            #    prjScn.image = xmlScene.find('ImageFile').text

            #--- Characters associated with the scene.
            scCharacters = []
            if xmlScene.find('Characters') is not None:
                for character in xmlScene.find('Characters').iter('CharID'):
                    crId = f"{CHARACTER_PREFIX}{character.text}"
                    if crId in self.novel.tree.get_children(CR_ROOT):
                        scCharacters.append(crId)
            prjScn.characters = scCharacters

            #--- Locations associated with the scene.
            scLocations = []
            if xmlScene.find('Locations') is not None:
                for location in xmlScene.find('Locations').iter('LocID'):
                    lcId = f"{LOCATION_PREFIX}{location.text}"
                    if lcId in self.novel.tree.get_children(LC_ROOT):
                        scLocations.append(lcId)
            prjScn.locations = scLocations

            #--- Items associated with the scene.
            scItems = []
            if xmlScene.find('Items') is not None:
                for item in xmlScene.find('Items').iter('ItemID'):
                    itId = f"{ITEM_PREFIX}{item.text}"
                    if itId in self.novel.tree.get_children(IT_ROOT):
                        scItems.append(itId)
            prjScn.items = scItems

            ywScId = xmlScene.find('ID').text
            if ywScId in self._ywApIds:
                # it's a plot point
                ppId = f"{PLOT_POINT_PREFIX}{ywScId}"
                self.novel.plotPoints[ppId] = self._nvSvc.make_plot_point(title=prjScn.title,
                                                      desc=prjScn.desc
                                                      )
                if ywScnAssocs:
                    self.novel.plotPoints[ppId].sectionAssoc = f'{SECTION_PREFIX}{ywScnAssocs[0]}'
            else:
                # it's a scene
                if prjScn.tags and self.STAGE_MARKER in prjScn.tags:
                    # no, it's a stage
                    prjScn.scType = 3
                    prjScn.tags = prjScn.tags.remove(self.STAGE_MARKER)
                scId = f"{SECTION_PREFIX}{ywScId}"
                self.novel.sections[scId] = prjScn

    def _strip_spaces(self, lines):
        """Local helper method.

        Positional argument:
            lines -- list of strings

        Return lines with leading and trailing spaces removed.
        """
        stripped = []
        for line in lines:
            stripped.append(line.strip())
        return stripped

    def _to_yw(self, text):
        """Convert Markdown to yWriter 7 markup.
        
        Positional arguments:
            text -- string to convert.
        
        Return a yw7 markup string.
        """
        if not text:
            return ''

        while '\n\n' in text:
            text = text.replace('\n\n', '@%&').strip()
        while '***' in text:
            text = text.replace('***', '§%§')
        text = re.sub(r'([^\*])\*\*(.+?)\*\*', '\\1[b]\\2[/b]', text)
        text = re.sub(r'([^\*])\*(.+?)\*', '\\1[i]\\2[/i]', text)
        while '§%§' in text:
            text = text.replace('§%§', '***')
        newlines = []
        for line in text.split('@%&'):
            newlines.append(line)
        text = '\n'.join(newlines)
        text = re.sub(r'\*\*(.+?)\*\*', '[b]\\1[/b]', text)
        text = re.sub(r'\*([^ ].+?[^ ])\*', '[i]\\1[/i]', text)
        MD_REPLACEMENTS = [
            ('\n\n', '\n'),
            ('<!---', '/*'),
            ('--->', '*/'),
        ]
        try:
            for md, yw in MD_REPLACEMENTS:
                text = text.replace(md, yw)
        except AttributeError:
            text = ''
        return text

    def _write_element_tree(self, ywProject):
        """Write back the xml element tree to a .yw7 xml file located at filePath.
        
        Raise the "Error" exception in case of error. 
        """
        backedUp = False
        if os.path.isfile(ywProject.filePath):
            try:
                os.replace(ywProject.filePath, f'{ywProject.filePath}.bak')
            except:
                raise Error(f'{_("Cannot overwrite file")}: "{norm_path(ywProject.filePath)}".')
            else:
                backedUp = True
        try:
            ywProject.tree.write(ywProject.filePath, xml_declaration=False, encoding='utf-8')
        except:
            if backedUp:
                os.replace(f'{ywProject.filePath}.bak', ywProject.filePath)
            raise Error(f'{_("Cannot write file")}: "{norm_path(ywProject.filePath)}".')

