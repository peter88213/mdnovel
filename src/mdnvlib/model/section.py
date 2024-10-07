"""Provide a class for mdnovel section representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnvlib
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
import re

from mdnvlib.model.basic_element_tags import BasicElementTags
from mdnvlib.model.date_time_tools import get_specific_date
from mdnvlib.model.date_time_tools import get_unspecific_date
from mdnvlib.novx_globals import _
from mdnvlib.novx_globals import list_to_string
from mdnvlib.novx_globals import string_to_list
from mdnvlib.novx_globals import verified_date
from mdnvlib.novx_globals import verified_int_string
from mdnvlib.novx_globals import verified_time

# Regular expressions for counting words and characters like in LibreOffice.
# See: https://help.libreoffice.org/latest/en-GB/text/swriter/guide/words_count.html
ADDITIONAL_WORD_LIMITS = re.compile(r'--|—|–|\<\/p\>')
# this is to be replaced by spaces when counting words

NO_WORD_LIMITS = re.compile(r'\<note\>.*?\<\/note\>|\<comment\>.*?\<\/comment\>|\<.+?\>')
# this is to be replaced by empty strings when counting words


class Section(BasicElementTags):
    """mdnovel section representation."""

    SCENE = ['-', 'A', 'R', 'x']
    # emulating an enumeration for the scene Action/Reaction/Other type

    STATUS = [
        None,
        _('Outline'),
        _('Draft'),
        _('1st Edit'),
        _('2nd Edit'),
        _('Done')
    ]
    # emulating an enumeration for the section completion status

    NULL_DATE = '0001-01-01'
    NULL_TIME = '00:00:00'

    def __init__(self,
            scType=None,
            scene=None,
            status=None,
            appendToPrev=None,
            goal=None,
            conflict=None,
            outcome=None,
            plotNotes=None,
            scDate=None,
            scTime=None,
            day=None,
            lastsMinutes=None,
            lastsHours=None,
            lastsDays=None,
            characters=None,
            locations=None,
            items=None,
            **kwargs):
        """Extends the superclass constructor."""
        super().__init__(**kwargs)
        self._sectionContent = None
        self.wordCount = 0
        # To be updated by the sectionContent setter

        # Initialize properties.
        self._scType = scType
        self._scene = scene
        self._status = status
        self._appendToPrev = appendToPrev
        self._goal = goal
        self._conflict = conflict
        self._outcome = outcome
        self._plotlineNotes = plotNotes
        try:
            newDate = date.fromisoformat(scDate)
            self._weekDay = newDate.weekday()
            self._localeDate = newDate.strftime('%x')
            self._date = scDate
        except:
            self._weekDay = None
            self._localeDate = None
            self._date = None
        self._time = scTime
        self._day = day
        self._lastsMinutes = lastsMinutes
        self._lastsHours = lastsHours
        self._lastsDays = lastsDays
        self._characters = characters
        self._locations = locations
        self._items = items

        self.scPlotLines = []
        # Back references to PlotLine.sections
        self.scPlotPoints = {}
        # Back references to TurningPoint.sectionAssoc
        # key: plot point ID, value: plot line ID

    @property
    def sectionContent(self):
        return self._sectionContent

    @sectionContent.setter
    def sectionContent(self, text):
        """Set sectionContent updating word count and letter count."""
        if text is not None:
            assert type(text) == str
        if self._sectionContent != text:
            self._sectionContent = text
            if text is not None:
                text = ADDITIONAL_WORD_LIMITS.sub(' ', text)
                text = NO_WORD_LIMITS.sub('', text)
                wordList = text.split()
                self.wordCount = len(wordList)
            else:
                self.wordCount = 0
            self.on_element_change()

    @property
    def scType(self):
        # 0 = Normal
        # 1 = Unused
        # 2 = Level 1 stage
        # 3 = Level 2 stage
        return self._scType

    @scType.setter
    def scType(self, newVal):
        if newVal is not None:
            assert type(newVal) == int
        if self._scType != newVal:
            self._scType = newVal
            self.on_element_change()

    @property
    def scene(self):
        # 0 = not a scene
        # 1 = action scene
        # 2 = reaction scene
        # 3 = other scene
        return self._scene

    @scene.setter
    def scene(self, newVal):
        if newVal is not None:
            assert type(newVal) == int
        if self._scene != newVal:
            self._scene = newVal
            self.on_element_change()

    @property
    def status(self):
        # 1 - Outline
        # 2 - Draft
        # 3 - 1st Edit
        # 4 - 2nd Edit
        # 5 - Done
        return self._status

    @status.setter
    def status(self, newVal):
        if newVal is not None:
            assert type(newVal) == int
        if self._status != newVal:
            self._status = newVal
            self.on_element_change()

    @property
    def appendToPrev(self):
        # True - append this section to the previous one without a section separator
        # False - put a section separator between this section and the previous one
        return self._appendToPrev

    @appendToPrev.setter
    def appendToPrev(self, newVal):
        if newVal is not None:
            assert type(newVal) == bool
        if self._appendToPrev != newVal:
            self._appendToPrev = newVal
            self.on_element_change()

    @property
    def goal(self):
        return self._goal

    @goal.setter
    def goal(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._goal != newVal:
            self._goal = newVal
            self.on_element_change()

    @property
    def conflict(self):
        return self._conflict

    @conflict.setter
    def conflict(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._conflict != newVal:
            self._conflict = newVal
            self.on_element_change()

    @property
    def outcome(self):
        return self._outcome

    @outcome.setter
    def outcome(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._outcome != newVal:
            self._outcome = newVal
            self.on_element_change()

    @property
    def plotlineNotes(self):
        # Dict of {plot line ID: text}
        try:
            return dict(self._plotlineNotes)
        except TypeError:
            return None

    @plotlineNotes.setter
    def plotlineNotes(self, newVal):
        if newVal is not None:
            for elem in newVal:
                val = newVal[elem]
                if val is not None:
                    assert type(val) == str
        if self._plotlineNotes != newVal:
            self._plotlineNotes = newVal
            self.on_element_change()

    @property
    def date(self):
        # YYYY-MM-DD
        return self._date

    @date.setter
    def date(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._date != newVal:
            if not newVal:
                self._date = None
                self._weekDay = None
                self._localeDate = None
                self.on_element_change()
                return

            try:
                newDate = date.fromisoformat(newVal)
                self._weekDay = newDate.weekday()
            except:
                return
                # date and week day remain unchanged

            try:
                self._localeDate = newDate.strftime('%x')
            except:
                self._localeDate = newVal
            self._date = newVal
            self.on_element_change()

    @property
    def weekDay(self):
        # the number of the day ot the week
        return self._weekDay

    @property
    def localeDate(self):
        # the preferred date representation for the current locale
        return self._localeDate

    @property
    def time(self):
        # hh:mm:ss
        return self._time

    @time.setter
    def time(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._time != newVal:
            self._time = newVal
            self.on_element_change()

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._day != newVal:
            self._day = newVal
            self.on_element_change()

    @property
    def lastsMinutes(self):
        return self._lastsMinutes

    @lastsMinutes.setter
    def lastsMinutes(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._lastsMinutes != newVal:
            self._lastsMinutes = newVal
            self.on_element_change()

    @property
    def lastsHours(self):
        return self._lastsHours

    @lastsHours.setter
    def lastsHours(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._lastsHours != newVal:
            self._lastsHours = newVal
            self.on_element_change()

    @property
    def lastsDays(self):
        return self._lastsDays

    @lastsDays.setter
    def lastsDays(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._lastsDays != newVal:
            self._lastsDays = newVal
            self.on_element_change()

    @property
    def characters(self):
        # list of character IDs
        try:
            return self._characters[:]
        except TypeError:
            return None

    @characters.setter
    def characters(self, newVal):
        if newVal is not None:
            for elem in newVal:
                if elem is not None:
                    assert type(elem) == str
        if self._characters != newVal:
            self._characters = newVal
            self.on_element_change()

    @property
    def locations(self):
        # List of location IDs
        try:
            return self._locations[:]
        except TypeError:
            return None

    @locations.setter
    def locations(self, newVal):
        if newVal is not None:
            for elem in newVal:
                if elem is not None:
                    assert type(elem) == str
        if self._locations != newVal:
            self._locations = newVal
            self.on_element_change()

    @property
    def items(self):
        # List of Item IDs
        try:
            return self._items[:]
        except TypeError:
            return None

    @items.setter
    def items(self, newVal):
        if newVal is not None:
            for elem in newVal:
                if elem is not None:
                    assert type(elem) == str
        if self._items != newVal:
            self._items = newVal
            self.on_element_change()

    def day_to_date(self, referenceDate):
        """Convert day to specific date.
        
        Positional argument:
        referenceDate: str -- reference date in isoformat.

        On success, return True. Otherwise return False. 
        """
        if self._date:
            return True

        try:
            self.date = get_specific_date(self._day, referenceDate)
            self._day = None
            return True

        except:
            self.date = None
            return False

    def date_to_day(self, referenceDate):
        """Convert specific date to day.
        
        Positional argument:
        referenceDate: str -- reference date in isoformat.
        
        On success, return True. Otherwise return False. 
        """
        if self._day:
            return True

        try:
            self._day = get_unspecific_date(self._date, referenceDate)
            self.date = None
            return True

        except:
            self._day = None
            return False

    def from_yaml(self, yaml):
        super().from_yaml(yaml)

        # Attributes.
        typeStr = self._get_meta_value('type', '0')
        if typeStr in ('0', '1', '2', '3'):
            self.scType = int(typeStr)
        else:
            self.scType = 1
        status = self._get_meta_value('status', None)
        if status in ('2', '3', '4', '5'):
            self.status = int(status)
        else:
            self.status = 1
        scene = self._get_meta_value('scene', 0)
        if scene in ('1', '2', '3'):
            self.scene = int(scene)
        else:
            self.scene = 0

        if not self.scene:
            # looking for deprecated attribute from DTD 1.3
            sceneKind = self._get_meta_value('pacing', None)
            if sceneKind in ('1', '2'):
                self.scene = int(sceneKind) + 1

        self.appendToPrev = self._get_meta_value('append', None) == '1'

        # Date/Day and Time.
        self.date = verified_date(self._get_meta_value('Date'))
        if not self.date:
            self.day = verified_int_string(self._get_meta_value('Day'))

        self.time = verified_time(self._get_meta_value('Time'))

        # Duration.
        self.lastsDays = verified_int_string(self._get_meta_value('LastsDays'))
        self.lastsHours = verified_int_string(self._get_meta_value('LastsHours'))
        self.lastsMinutes = verified_int_string(self._get_meta_value('LastsMinutes'))

        # Characters references.
        scCharacters = self._get_meta_value('Characters')
        self.characters = string_to_list(scCharacters)

        # Locations references.
        scLocations = self._get_meta_value('Locations')
        self.locations = string_to_list(scLocations)

        # Items references.
        scItems = self._get_meta_value('Items')
        self.items = string_to_list(scItems)

    def get_end_date_time(self):
        """Return the end (date, time, day) tuple calculated from start and duration."""
        endDate = None
        endTime = None
        endDay = None
        if self.lastsDays:
            lastsDays = int(self.lastsDays)
        else:
            lastsDays = 0
        if self.lastsHours:
            lastsSeconds = int(self.lastsHours) * 3600
        else:
            lastsSeconds = 0
        if self.lastsMinutes:
            lastsSeconds += int(self.lastsMinutes) * 60
        sectionDuration = timedelta(days=lastsDays, seconds=lastsSeconds)
        if self.time:
            if self.date:
                try:
                    sectionStart = datetime.fromisoformat(f'{self.date} {self.time}')
                    sectionEnd = sectionStart + sectionDuration
                    endDate, endTime = sectionEnd.isoformat().split('T')
                except:
                    pass
            else:
                try:
                    if self.day:
                        dayInt = int(self.day)
                    else:
                        dayInt = 0
                    startDate = (date.min + timedelta(days=dayInt)).isoformat()
                    sectionStart = datetime.fromisoformat(f'{startDate} {self.time}')
                    sectionEnd = sectionStart + sectionDuration
                    endDate, endTime = sectionEnd.isoformat().split('T')
                    endDay = str((date.fromisoformat(endDate) - date.min).days)
                    endDate = None
                except:
                    pass
        return endDate, endTime, endDay

    def to_yaml(self, yaml):
        yaml = super().to_yaml(yaml)
        if self.scType:
            yaml.append(f'type: {self.scType}')
        if self.status > 1:
            yaml.append(f'status: {self.status}')
        if self.scene > 0:
            yaml.append(f'scene: {self.scene}')
        if self.appendToPrev:
            yaml.append(f'append: 1')

        # Date/Day and Time.
        if self.date:
            yaml.append(f'Date: {self.date}')
        elif self.day:
            yaml.append(f'Day: {self.day}')
        if self.time:
            yaml.append(f'Time: {self.time}')

        # Duration.
        if self.lastsDays and self.lastsDays != '0':
            yaml.append(f'LastsDays: {self.lastsDays}')
        if self.lastsHours and self.lastsHours != '0':
            yaml.append(f'LastsHours: {self.lastsHours}')
        if self.lastsMinutes and self.lastsMinutes != '0':
            yaml.append(f'LastsMinutes: {self.lastsMinutes}')

        # Characters references.
        if self.characters:
            yaml.append(f'Characters: {list_to_string(self.characters)}')

        # Locations references.
        if self.locations:
            yaml.append(f'Locations: {list_to_string(self.locations)}')

        # Items references.
        if self.items:
            yaml.append(f'Items: {list_to_string(self.items)}')

        return yaml
