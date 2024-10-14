"""Provide a class for Timeline section event representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date, datetime, timedelta, MINYEAR
from mdnvlib.model.section import Section
import xml.etree.ElementTree as ET


class SectionEvent(Section):
    """Timeline section event representation.

    Public instance variables:
        contId: str -- container ID.
    """
    defaultDateTime = '1900-01-01 00:00:00'
    sectionColor = '170,240,160'

    def __init__(self, section):
        super().__init__()
        self.scType = section.scType
        self.scene = section.scene
        self.status = section.status
        self.appendToPrev = section.appendToPrev
        self.goal = section.goal
        self.conflict = section.conflict
        self.outcome = section.outcome
        self.plotlineNotes = section.plotlineNotes
        self.date = section.date
        self.time = section.time
        self.day = section.day
        self.lastsMinutes = section.lastsMinutes
        self.lastsHours = section.lastsHours
        self.lastsDays = section.lastsDays
        self.characters = section.characters
        self.locations = section.locations
        self.items = section.items

        self.title = section.title
        self.desc = section.desc
        self.sectionContent = section.sectionContent
        self.notes = section.notes
        self.tags = section.tags,
        self.wordCount = section.wordCount

        self.contId = None
        self._startDateTime = None
        self._endDateTime = None

        self.NULL_DATE = section.NULL_DATE
        self.NULL_TIME = section.NULL_TIME

    def set_date_time(self, startDateTime, endDateTime, isUnspecific):
        """Set date/time and, if applicable, duration.
        
        Positional arguments:
            startDateTime: str -- event start date/time as stored in Timeline.
            endDateTime: str -- event end date/time as stored in Timeline.
            isUnspecific: str -- if True, convert date to Day.
        
        Because mdnovel can not process years before 1, 
        they are saved for Timeline use and replaced with 
        a 'default negative date' for mdnovel use.
        """
        # Save instance variables for Timeline use.
        self._startDateTime = startDateTime
        self._endDateTime = endDateTime

        # Save instance variables for mdnovel use.
        dtIsValid = True
        # The date/time combination is within the range mdnovel can process.

        # Prevent two-figure years from becoming "completed" by mdnovel.
        dt = startDateTime.split(' ')
        if dt[0].startswith('-'):
            startYear = -1 * int(dt[0].split('-')[1])
            dtIsValid = False
            # "BC" year (mdnovel won't process it).
        else:
            startYear = int(dt[0].split('-')[0])
        if startYear < MINYEAR:
            # Substitute date/time, so mdnovel would not prefix them with '19' or '20'.
            self.date = self.NULL_DATE
            self.time = self.NULL_TIME
            dtIsValid = False
        else:
            self.date = dt[0]
            self.time = dt[1]
        if dtIsValid:
            # Calculate duration of sections that begin after 99-12-31.
            sectionStart = datetime.fromisoformat(startDateTime)
            sectionEnd = datetime.fromisoformat(endDateTime)
            sectionDuration = sectionEnd - sectionStart
            lastsHours = sectionDuration.seconds // 3600
            lastsMinutes = (sectionDuration.seconds % 3600) // 60
            self.lastsDays = str(sectionDuration.days)
            self.lastsHours = str(lastsHours)
            self.lastsMinutes = str(lastsMinutes)
            if isUnspecific:
                # Convert date to day
                try:
                    sectionDate = date.fromisoformat(self.date)
                    referenceDate = date.fromisoformat(self.defaultDateTime.split(' ')[0])
                    self.day = str((sectionDate - referenceDate).days)
                except:
                    # Do not synchronize.
                    self.day = None
                self.date = None

    def merge_date_time(self, source, defaultDay=0):
        """Set date/time related variables from a mdnovel-generated source section.
                
        Positional arguments:
            source -- Section instance with date/time to merge.
        
        Optional arguments:
            defaultDay -- The day to be set if the section does not have a date or a day.
        """
        #--- Set start date/time.
        if source.date is not None and source.date != self.NULL_DATE:
            # The date is not "BC", so synchronize it.
            if source.time:
                self._startDateTime = f'{source.date} {source.time}'
            else:
                self._startDateTime = f'{source.date} 00:00:00'
        elif source.date is None:
            # calculate startDate/startTime from day and time.
            if source.day:
                dayInt = int(source.day)
            else:
                # The section has neither date nor day.
                dayInt = defaultDay
            if source.time:
                startTime = source.time
            else:
                startTime = '00:00:00'
            sectionDelta = timedelta(days=dayInt)
            defaultDate = self.defaultDateTime.split(' ')[0]
            startDate = (date.fromisoformat(defaultDate) + sectionDelta).isoformat()
            self._startDateTime = f'{startDate} {startTime}'
        elif self._startDateTime is None:
            self._startDateTime = self.defaultDateTime
        else:
            # The date is "BC", so do not synchronize.
            pass

        #--- Set end date/time.
        if source.date is not None and source.date == self.NULL_DATE:
            # The year is two-figure, so do not synchronize.
            if self._endDateTime is None:
                self._endDateTime = self._startDateTime
        else:
            # Calculate end date from source section duration.
            if source.lastsDays:
                lastsDays = int(source.lastsDays)
            else:
                lastsDays = 0
            if source.lastsHours:
                lastsSeconds = int(source.lastsHours) * 3600
            else:
                lastsSeconds = 0
            if source.lastsMinutes:
                lastsSeconds += int(source.lastsMinutes) * 60
            sectionDuration = timedelta(days=lastsDays, seconds=lastsSeconds)
            sectionStart = datetime.fromisoformat(self._startDateTime)
            sectionEnd = sectionStart + sectionDuration
            self._endDateTime = sectionEnd.isoformat(' ')
        # Tribute to defensive programming.
        if self._startDateTime > self._endDateTime:
            self._endDateTime = self._startDateTime

    def build_branch(self, xmlEvent, scId, dtMin, dtMax):
        """Build a Timeline XML event branch.
        
        Positional arguments:
            xmlEvent: elementTree.SubElement -- Timeline event XML subtree.
            scId: str -- section ID.
            dtMin: str -- lower date/time limit.
            dtMax: str -- upper date/time limit.
            
        Return a tuple of two:  
            dtMin: str -- updated lower date/time limit.
            dtMax: str -- updated upper date/time limit.
        
        xmlEvent elements are created or updated.
        """
        scIndex = 0
        try:
            xmlEvent.find('start').text = self._startDateTime
        except(AttributeError):
            ET.SubElement(xmlEvent, 'start').text = self._startDateTime
        if (not dtMin) or (self._startDateTime < dtMin):
            dtMin = self._startDateTime
        scIndex += 1
        try:
            xmlEvent.find('end').text = self._endDateTime
        except(AttributeError):
            ET.SubElement(xmlEvent, 'end').text = self._endDateTime
        if (not dtMax) or (self._endDateTime > dtMax):
            dtMax = self._endDateTime
        scIndex += 1
        if not self.title:
            self.title = f'Unnamed section ID{scId}'
        try:
            xmlEvent.find('text').text = self.title
        except(AttributeError):
            ET.SubElement(xmlEvent, 'text').text = self.title
        scIndex += 1
        if xmlEvent.find('progress') is None:
            ET.SubElement(xmlEvent, 'progress').text = '0'
        scIndex += 1
        if xmlEvent.find('fuzzy') is None:
            ET.SubElement(xmlEvent, 'fuzzy').text = 'False'
        scIndex += 1
        if xmlEvent.find('fuzzy_start') is not None:
            scIndex += 1
        if xmlEvent.find('fuzzy_end') is not None:
            scIndex += 1
        if xmlEvent.find('locked') is None:
            ET.SubElement(xmlEvent, 'locked').text = 'False'
        scIndex += 1
        if xmlEvent.find('ends_today') is None:
            ET.SubElement(xmlEvent, 'ends_today').text = 'False'
        scIndex += 1
        if self.desc is not None:
            try:
                xmlEvent.find('description').text = self.desc
            except(AttributeError):
                if xmlEvent.find('labels') is None:
                    # Append the description.
                    ET.SubElement(xmlEvent, 'description').text = self.desc
                else:
                    # Insert the description.
                    if xmlEvent.find('category') is not None:
                        scIndex += 1
                    desc = ET.Element('description')
                    desc.text = self.desc
                    xmlEvent.insert(scIndex, desc)
        elif xmlEvent.find('description') is not None:
            xmlEvent.remove(xmlEvent.find('description'))
        if xmlEvent.find('labels') is None:
            ET.SubElement(xmlEvent, 'labels').text = scId
        if xmlEvent.find('default_color') is None:
            ET.SubElement(xmlEvent, 'default_color').text = self.sectionColor
        return dtMin, dtMax

