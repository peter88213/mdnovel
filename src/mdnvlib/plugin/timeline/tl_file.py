"""Provide a class for Timeline project file representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
from datetime import timedelta
import os
import re

from mdnvlib.file.file import File
from mdnvlib.novx_globals import CHAPTER_PREFIX
from mdnvlib.novx_globals import CH_ROOT
from mdnvlib.novx_globals import Error
from mdnvlib.novx_globals import SECTION_PREFIX
from mdnvlib.novx_globals import _
from mdnvlib.novx_globals import norm_path
from mdnvlib.plugin.timeline.dt_helper import fix_iso_dt
from mdnvlib.plugin.timeline.section_event import SectionEvent
import xml.etree.ElementTree as ET


class TlFile(File):
    """Timeline project file representation.

    This class represents a file containing a timeline with additional 
    attributes and structural information (a full set or a subset
    of the information included in an Timeline project file).
    """
    DESCRIPTION = 'Timeline'
    EXTENSION = '.timeline'
    SUFFIX = None

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables and SectionEvent class variables.

        Positional arguments:
            filePath: str -- path to the file represented by the Novel instance.
            
        Required keyword arguments:
            section_label: str -- event label marking "section" events.
            section_color: str -- color for events imported as sections from mdnovel.
            new_event_spacing: str -- Days between events with automatically generated dates.  
        
        Extends the superclass constructor.
        """
        super().__init__(filePath, **kwargs)
        self._nvSvc = kwargs['nv_service']
        self._xmlTree = None
        self._sectionMarker = kwargs['section_label']
        SectionEvent.sectionColor = kwargs['section_color']

        try:
            self._newEventSpacing = int(kwargs['new_event_spacing'])
        except:
            self._newEventSpacing = 0

    def read(self):
        """Parse the file and get the instance variables.
        
        Raise the "Error" exception in case of error. 
        Overrides the superclass method.
        """

        def remove_contId(event, text):
            """Separate container ID from event title.
            
            Positional arguments:
                event -- SectionEvent to update.
                text: str -- event title.         
            
            If text comes with a Container ID, remove it 
            and store it in the event.contId instance variable.
            Return the stripped string.
            """
            if text:
                match = re.match(r'([\(\[][0-9]+[\)\]])', text)
                if match:
                    contId = match.group()
                    event.contId = contId
                    text = text.split(contId, 1)[1]
            return text

        #--- Parse the Timeline file.
        if self.novel.referenceDate:
            SectionEvent.defaultDateTime = f'{self.novel.referenceDate} 00:00:00'
        else:
            SectionEvent.defaultDateTime = datetime.today().isoformat(' ', 'seconds')

        if not self.novel.sections:
            isOutline = True
        else:
            isOutline = False

        try:
            self._xmlTree = ET.parse(self.filePath)
        except:
            raise Error(f'{_("Can not process file")}: "{norm_path(self.filePath)}".')
        root = self._xmlTree.getroot()
        sectionCount = 0
        scIdsByDate = {}
        for event in root.iter('event'):
            scId = None
            sectionMatch = None
            if event.find('labels') is not None:
                labels = event.find('labels').text
                sectionMatch = re.search(fr'{SECTION_PREFIX}[0-9]+', labels)
                if isOutline and sectionMatch is None:
                    sectionMatch = re.search(self._sectionMarker, labels)
            if sectionMatch is None:
                continue

            # The event is labeled as a section.
            sectionDate = None
            if isOutline:
                sectionCount += 1
                sectionMarker = sectionMatch.group()
                scId = f'{SECTION_PREFIX}{sectionCount}'
                event.find('labels').text = labels.replace(sectionMarker, scId)
                self.novel.sections[scId] = SectionEvent(
                        self._nvSvc.make_section(
                            status=1,
                            scType=0,
                            scene=0,
                        )
                    )

            else:
                try:
                    scId = sectionMatch.group()
                    self.novel.sections[scId] = SectionEvent(self.novel.sections[scId])
                except:
                    continue

            try:
                title = event.find('text').text
                title = remove_contId(self.novel.sections[scId], title)
                title = self._convert_to_mdnov(title)
                self.novel.sections[scId].title = title
            except:
                self.novel.sections[scId].title = f'Section {scId}'
            try:
                self.novel.sections[scId].desc = event.find('description').text
            except:
                pass

            #--- Set date/time/duration.
            startDateTime = fix_iso_dt(event.find('start').text)
            endDateTime = fix_iso_dt(event.find('end').text)

            # Consider unspecific date/time in the target file.
            if isOutline:
                isUnspecific = False
            else:
                if self.novel.sections[scId].day is not None:
                    isUnspecific = True
                else:
                    isUnspecific = False
            self.novel.sections[scId].set_date_time(startDateTime, endDateTime, isUnspecific)
            if not startDateTime in scIdsByDate:
                scIdsByDate[startDateTime] = []
            scIdsByDate[startDateTime].append(scId)

        # Sort sections by date/time
        srtSections = sorted(scIdsByDate.items())
        if isOutline:
            # Create a single chapter and assign all sections to it.
            chId = f'{CHAPTER_PREFIX}1'
            self.novel.chapters[chId] = self._nvSvc.make_chapter(
                chType=0,
                title=f'{_("Chapter")} 1'
                )
            self.novel.tree.append(CH_ROOT, chId)
            for __, scList in srtSections:
                for scId in scList:
                    self.novel.tree.append(chId, scId)
            # Rewrite the timeline with section IDs inserted.
            os.replace(self.filePath, f'{self.filePath}.bak')
            try:
                self._xmlTree.write(self.filePath, xml_declaration=True, encoding='utf-8')
            except:
                os.replace(f'{self.filePath}.bak', self.filePath)
                raise Error(f'{_("Cannot write file")}: "{norm_path(self.filePath)}".')

    def write(self, source):
        """Write instance variables to the file.
        
        Raise the "Error" exception in case of error. 
        Overrides the superclass method.
        """

        def add_contId(event, text):
            """If event has a container ID, add it to text."""
            if event.contId is not None:
                return f'{event.contId}{text}'
            return text

        def indent(elem, level=0):
            """xml pretty printer based on a code example by Fredrik Lundh.
            
            Although there is an ElementTree.indent() method from Python 3.9 on,
            this routine is needed to be compatible with Python 3.6.
            """
            i = f'\n{level * "  "}'
            if len(elem):
                if not elem.text or not elem.text.strip():
                    elem.text = f'{i}  '
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
                for elem in elem:
                    indent(elem, level + 1)
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
            else:
                if level and (not elem.tail or not elem.tail.strip()):
                    elem.tail = i

        def set_view_range(dtMin, dtMax):
            """Return maximum/minimum timestamp defining the view range in Timeline.
            
            Positional arguments:
                dtMin: str -- lower date/time limit.
                dtMax: str -- upper date/time limit.
            """
            if dtMin is None:
                dtMin = SectionEvent.defaultDateTime
            if dtMax is None:
                dtMax = dtMin
            TIME_LIMIT = '0100-01-01 00:00:00'
            # This is used to create a time interval outsides the processible time range.
            SEC_PER_DAY = 24 * 3600
            dt = dtMin.split(' ')
            if dt[0].startswith('-'):
                startYear = -1 * int(dt[0].split('-')[1])
                # "BC" year.
            else:
                startYear = int(dt[0].split('-')[0])
            if startYear < 100:
                if dtMax == dtMin:
                    dtMax = TIME_LIMIT
                return dtMin, dtMax
            # dtMin and dtMax are within the processible range.
            vrMax = datetime.fromisoformat(dtMax)
            vrMin = datetime.fromisoformat(dtMin)
            viewRange = (vrMax - vrMin).total_seconds()

            # Calculate a margin added to the (dtMin dtMax) interval.
            if viewRange > SEC_PER_DAY:
                margin = viewRange / 10
            else:
                margin = 3600
            dtMargin = timedelta(seconds=margin)
            try:
                vrMin -= dtMargin
                dtMin = vrMin.isoformat(' ', 'seconds')
            except OverflowError:
                pass
            try:
                vrMax += dtMargin
                dtMax = vrMax.isoformat(' ', 'seconds')
            except OverflowError:
                pass
            return dtMin, dtMax

        #--- Merge first.
        self.novel.chapters = {}
        self.novel.tree = self._nvSvc.make_nv_tree()
        # resetting the target structure, just keeping the sections

        if source.referenceDate:
            SectionEvent.defaultDateTime = f'{source.referenceDate} 00:00:00'
            ignoreUnspecific = False
        else:
            SectionEvent.defaultDateTime = datetime.today().isoformat(' ', 'seconds')
            ignoreUnspecific = True

        defaultDay = 0
        for chId in source.tree.get_children(CH_ROOT):
            self.novel.chapters[chId] = self._nvSvc.make_chapter()
            self.novel.tree.append(CH_ROOT, chId)
            for scId in source.tree.get_children(chId):
                if ignoreUnspecific and source.sections[scId].date is None:
                    # Skip sections without specific date information.
                    continue

                if not scId in self.novel.sections:
                    self.novel.sections[scId] = SectionEvent(self._nvSvc.make_section())
                self.novel.tree.append(chId, scId)
                if source.sections[scId].title:
                    title = source.sections[scId].title
                    title = self._convert_from_mdnov(title)
                    title = add_contId(self.novel.sections[scId], title)
                    self.novel.sections[scId].title = title
                self.novel.sections[scId].desc = source.sections[scId].desc
                defaultDay += self._newEventSpacing
                self.novel.sections[scId].merge_date_time(source.sections[scId], defaultDay=defaultDay)
                self.novel.sections[scId].scType = source.sections[scId].scType
        sections = list(self.novel.sections)
        for scId in sections:
            if not scId in source.sections:
                del self.novel.sections[scId]

        #--- Begin writing
        dtMin = None
        dtMax = None

        # List all sections to be exported.
        # Note: self.novel.sections may also contain orphaned ones.
        srtSections = []
        for chId in self.novel.tree.get_children(CH_ROOT):
            for scId in self.novel.tree.get_children(chId):
                if self.novel.sections[scId].scType == 0:
                    srtSections.append(scId)
        if self._xmlTree is not None:
            #--- Update an existing XML _xmlTree.
            root = self._xmlTree.getroot()
            events = root.find('events')
            trash = []
            scIds = []

            # Update events that are assigned to sections.
            for event in events.iter('event'):
                if event.find('labels') is not None:
                    labels = event.find('labels').text
                    sectionMatch = re.search(fr'{SECTION_PREFIX}[0-9]+', labels)
                else:
                    continue

                if sectionMatch is not None:
                    scId = sectionMatch.group()
                    if scId in srtSections:
                        scIds.append(scId)
                        dtMin, dtMax = self.novel.sections[scId].build_branch(event, scId, dtMin, dtMax)
                    else:
                        trash.append(event)

            # Add new events.
            for scId in srtSections:
                if not scId in scIds:
                    event = ET.SubElement(events, 'event')
                    dtMin, dtMax = self.novel.sections[scId].build_branch(event, scId, dtMin, dtMax)
            # Remove events that are assigned to missing sections.
            for event in trash:
                events.remove(event)

            # Set the view range.
            dtMin, dtMax = set_view_range(dtMin, dtMax)
            view = root.find('view')
            period = view.find('displayed_period')
            period.find('start').text = dtMin
            period.find('end').text = dtMax
        else:
            #--- Create a new XML _xmlTree.
            root = ET.Element('timeline')
            ET.SubElement(root, 'version').text = '2.4.0 (3f207fbb63f0 2021-04-07)'
            ET.SubElement(root, 'timetype').text = 'gregoriantime'
            ET.SubElement(root, 'categories')
            events = ET.SubElement(root, 'events')
            for scId in srtSections:
                event = ET.SubElement(events, 'event')
                dtMin, dtMax = self.novel.sections[scId].build_branch(event, scId, dtMin, dtMax)

            # Set the view range.
            dtMin, dtMax = set_view_range(dtMin, dtMax)
            view = ET.SubElement(root, 'view')
            period = ET.SubElement(view, 'displayed_period')
            ET.SubElement(period, 'start').text = dtMin
            ET.SubElement(period, 'end').text = dtMax
        indent(root)
        self._xmlTree = ET.ElementTree(root)

        #--- Back up the old timeline and write a new file.
        backedUp = False
        if os.path.isfile(self.filePath):
            try:
                os.replace(self.filePath, f'{self.filePath}.bak')
            except:
                raise Error(f'{_("Cannot overwrite file")}: "{norm_path(self.filePath)}".')
            else:
                backedUp = True
        try:
            self._xmlTree.write(self.filePath, xml_declaration=True, encoding='utf-8')
        except:
            if backedUp:
                os.replace(f'{self.filePath}.bak', self.filePath)
            raise Error(f'{_("Cannot write file")}: "{norm_path(self.filePath)}".')

    def _convert_to_mdnov(self, text):
        """Unmask brackets in novx section titles.
        
        Positional arguments:
            text -- string to convert.
        
        Return a string.
        Overrides the superclass method.
        """
        if text is not None:
            if text.startswith(' ('):
                text = text.lstrip()
            elif text.startswith(' ['):
                text = text.lstrip()
        return text

    def _convert_from_mdnov(self, text, **kwargs):
        """Mask brackets in novx section titles.
        
        Positional arguments:
            text -- string to convert.
        
        Optional arguments:
            quick: bool -- not used here.
        
        Return a string.
        Overrides the superclass method.
        """
        if text is not None:
            if text.startswith('('):
                text = f' {text}'
            elif text.startswith('['):
                text = f' {text}'
        return text

