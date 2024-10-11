"""Provide a class for a novel representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnvlib
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date
import locale

from mdnvlib.model.basic_element import BasicElement
from mdnvlib.novx_globals import verified_date


class Novel(BasicElement):
    """Novel representation."""

    def __init__(self,
            authorName=None,
            wordTarget=None,
            wordCountStart=None,
            languageCode=None,
            countryCode=None,
            renumberChapters=None,
            renumberParts=None,
            renumberWithinParts=None,
            romanChapterNumbers=None,
            romanPartNumbers=None,
            saveWordCount=None,
            workPhase=None,
            chapterHeadingPrefix=None,
            chapterHeadingSuffix=None,
            partHeadingPrefix=None,
            partHeadingSuffix=None,
            customPlotProgress=None,
            customCharacterization=None,
            customWorldBuilding=None,
            customGoal=None,
            customConflict=None,
            customOutcome=None,
            customChrBio=None,
            customChrGoals=None,
            referenceDate=None,
            tree=None,
            **kwargs):
        """Extends the superclass constructor."""
        super().__init__(**kwargs)
        self._authorName = authorName
        self._wordTarget = wordTarget
        self._wordCountStart = wordCountStart
        self._languageCode = languageCode
        self._countryCode = countryCode
        self._renumberChapters = renumberChapters
        self._renumberParts = renumberParts
        self._renumberWithinParts = renumberWithinParts
        self._romanChapterNumbers = romanChapterNumbers
        self._romanPartNumbers = romanPartNumbers
        self._saveWordCount = saveWordCount
        self._workPhase = workPhase
        self._chapterHeadingPrefix = chapterHeadingPrefix
        self._chapterHeadingSuffix = chapterHeadingSuffix
        self._partHeadingPrefix = partHeadingPrefix
        self._partHeadingSuffix = partHeadingSuffix
        self._customPlotProgress = customPlotProgress
        self._customCharacterization = customCharacterization
        self._customWorldBuilding = customWorldBuilding
        self._customGoal = customGoal
        self._customConflict = customConflict
        self._customOutcome = customOutcome
        self._customChrBio = customChrBio
        self._customChrGoals = customChrGoals

        self.chapters = {}
        # key = chapter ID, value = Chapter instance.
        self.sections = {}
        # key = section ID, value = Section instance.
        self.plotPoints = {}
        # key = section ID, value = PlotPoint instance.
        self.languages = None
        # List of non-document languages occurring as section markup.
        # Format: ll-CC, where ll is the language code, and CC is the country code.
        self.plotLines = {}
        # key = plot line ID, value = PlotLine instance.
        self.locations = {}
        # key = location ID, value = WorldElement instance.
        self.items = {}
        # key = item ID, value = WorldElement instance.
        self.characters = {}
        # key = character ID, value = Character instance.
        self.projectNotes = {}
        # key = note ID, value = note instance.
        try:
            self.referenceWeekDay = date.fromisoformat(referenceDate).weekday()
            self._referenceDate = referenceDate
            # YYYY-MM-DD
        except:
            self.referenceWeekDay = None
            self._referenceDate = None
        self.tree = tree

    @property
    def authorName(self):
        return self._authorName

    @authorName.setter
    def authorName(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._authorName != newVal:
            self._authorName = newVal
            self.on_element_change()

    @property
    def wordTarget(self):
        return self._wordTarget

    @wordTarget.setter
    def wordTarget(self, newVal):
        if newVal is not None:
            assert type(newVal) == int
        if self._wordTarget != newVal:
            self._wordTarget = newVal
            self.on_element_change()

    @property
    def wordCountStart(self):
        return self._wordCountStart

    @wordCountStart.setter
    def wordCountStart(self, newVal):
        if newVal is not None:
            assert type(newVal) == int
        if self._wordCountStart != newVal:
            self._wordCountStart = newVal
            self.on_element_change()

    @property
    def languageCode(self):
        # Language code acc. to ISO 639-1.
        return self._languageCode

    @languageCode.setter
    def languageCode(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._languageCode != newVal:
            self._languageCode = newVal
            self.on_element_change()

    @property
    def countryCode(self):
        # Country code acc. to ISO 3166-2.
        return self._countryCode

    @countryCode.setter
    def countryCode(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._countryCode != newVal:
            self._countryCode = newVal
            self.on_element_change()

    @property
    def renumberChapters(self):
        # True: Auto-number chapters
        # False: Do not auto-number chapters
        return self._renumberChapters

    @renumberChapters.setter
    def renumberChapters(self, newVal):
        if newVal is not None:
            assert type(newVal) == bool
        if self._renumberChapters != newVal:
            self._renumberChapters = newVal
            self.on_element_change()

    @property
    def renumberParts(self):
        # True: Auto-number parts
        # False: Do not auto-number parts
        return self._renumberParts

    @renumberParts.setter
    def renumberParts(self, newVal):
        if newVal is not None:
            assert type(newVal) == bool
        if self._renumberParts != newVal:
            self._renumberParts = newVal
            self.on_element_change()

    @property
    def renumberWithinParts(self):
        # True: When auto-numbering chapters, start with 1 at each part beginning
        # False: When auto-numbering chapters, ignore parts
        return self._renumberWithinParts

    @renumberWithinParts.setter
    def renumberWithinParts(self, newVal):
        if newVal is not None:
            assert type(newVal) == bool
        if self._renumberWithinParts != newVal:
            self._renumberWithinParts = newVal
            self.on_element_change()

    @property
    def romanChapterNumbers(self):
        # True: Use Roman chapter numbers when auto-numbering
        # False: Use Arabic chapter numbers when auto-numbering
        return self._romanChapterNumbers

    @romanChapterNumbers.setter
    def romanChapterNumbers(self, newVal):
        if newVal is not None:
            assert type(newVal) == bool
        if self._romanChapterNumbers != newVal:
            self._romanChapterNumbers = newVal
            self.on_element_change()

    @property
    def romanPartNumbers(self):
        # True: Use Roman part numbers when auto-numbering
        # False: Use Arabic part numbers when auto-numbering
        return self._romanPartNumbers

    @romanPartNumbers.setter
    def romanPartNumbers(self, newVal):
        if newVal is not None:
            assert type(newVal) == bool
        if self._romanPartNumbers != newVal:
            self._romanPartNumbers = newVal
            self.on_element_change()

    @property
    def saveWordCount(self):
        # True: Save daily word count log
        # False: Do not save daily word count log
        return self._saveWordCount

    @saveWordCount.setter
    def saveWordCount(self, newVal):
        if newVal is not None:
            assert type(newVal) == bool
        if self._saveWordCount != newVal:
            self._saveWordCount = newVal
            self.on_element_change()

    @property
    def workPhase(self):
        # None - Undefined
        # 1 - Outline
        # 2 - Draft
        # 3 - 1st Edit
        # 4 - 2nd Edit
        # 5 - Done
        return self._workPhase

    @workPhase.setter
    def workPhase(self, newVal):
        if newVal is not None:
            assert type(newVal) == int
        if self._workPhase != newVal:
            self._workPhase = newVal
            self.on_element_change()

    @property
    def chapterHeadingPrefix(self):
        return self._chapterHeadingPrefix

    @chapterHeadingPrefix.setter
    def chapterHeadingPrefix(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._chapterHeadingPrefix != newVal:
            self._chapterHeadingPrefix = newVal
            self.on_element_change()

    @property
    def chapterHeadingSuffix(self):
        return self._chapterHeadingSuffix

    @chapterHeadingSuffix.setter
    def chapterHeadingSuffix(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._chapterHeadingSuffix != newVal:
            self._chapterHeadingSuffix = newVal
            self.on_element_change()

    @property
    def partHeadingPrefix(self):
        return self._partHeadingPrefix

    @partHeadingPrefix.setter
    def partHeadingPrefix(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._partHeadingPrefix != newVal:
            self._partHeadingPrefix = newVal
            self.on_element_change()

    @property
    def partHeadingSuffix(self):
        return self._partHeadingSuffix

    @partHeadingSuffix.setter
    def partHeadingSuffix(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._partHeadingSuffix != newVal:
            self._partHeadingSuffix = newVal
            self.on_element_change()

    @property
    def customPlotProgress(self):
        return self._customPlotProgress

    @customPlotProgress.setter
    def customPlotProgress(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._customPlotProgress != newVal:
            self._customPlotProgress = newVal
            self.on_element_change()

    @property
    def customCharacterization(self):
        return self._customCharacterization

    @customCharacterization.setter
    def customCharacterization(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._customCharacterization != newVal:
            self._customCharacterization = newVal
            self.on_element_change()

    @property
    def customWorldBuilding(self):
        return self._customWorldBuilding

    @customWorldBuilding.setter
    def customWorldBuilding(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._customWorldBuilding != newVal:
            self._customWorldBuilding = newVal
            self.on_element_change()

    @property
    def customGoal(self):
        return self._customGoal

    @customGoal.setter
    def customGoal(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._customGoal != newVal:
            self._customGoal = newVal
            self.on_element_change()

    @property
    def customConflict(self):
        return self._customConflict

    @customConflict.setter
    def customConflict(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._customConflict != newVal:
            self._customConflict = newVal
            self.on_element_change()

    @property
    def customOutcome(self):
        return self._customOutcome

    @customOutcome.setter
    def customOutcome(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._customOutcome != newVal:
            self._customOutcome = newVal
            self.on_element_change()

    @property
    def customChrBio(self):
        return self._customChrBio

    @customChrBio.setter
    def customChrBio(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._customChrBio != newVal:
            self._customChrBio = newVal
            self.on_element_change()

    @property
    def customChrGoals(self):
        return self._customChrGoals

    @customChrGoals.setter
    def customChrGoals(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._customChrGoals != newVal:
            self._customChrGoals = newVal
            self.on_element_change()

    @property
    def referenceDate(self):
        return self._referenceDate

    @referenceDate.setter
    def referenceDate(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._referenceDate != newVal:
            if not newVal:
                self._referenceDate = None
                self.referenceWeekDay = None
                self.on_element_change()
            else:
                try:
                    self.referenceWeekDay = date.fromisoformat(newVal).weekday()
                except:
                    pass
                    # date and week day remain unchanged
                else:
                    self._referenceDate = newVal
                    self.on_element_change()

    def check_locale(self):
        """Check the document's locale (language code and country code).
        
        If the locale is missing, set the system locale.  
        If the locale doesn't look plausible, set "no language".      
        """
        if not self._languageCode or self._languageCode == 'None':
            # Language isn't set.
            try:
                sysLng, sysCtr = locale.getlocale()[0].split('_')
            except:
                # Fallback for old Windows versions.
                sysLng, sysCtr = locale.getdefaultlocale()[0].split('_')
            self._languageCode = sysLng
            self._countryCode = sysCtr
            self.on_element_change()
            return

        try:
            # Plausibility check: code must have two characters.
            if len(self._languageCode) == 2:
                if len(self._countryCode) == 2:
                    return
                    # keep the setting
        except:
            # code isn't a string
            pass
        # Existing language or country field looks not plausible
        self._languageCode = 'zxx'
        self._countryCode = 'none'
        self.on_element_change()

    def from_yaml(self, yaml):
        super().from_yaml(yaml)
        self.renumberChapters = self._get_meta_value('renumberChapters', None) == '1'
        self.renumberParts = self._get_meta_value('renumberParts', None) == '1'
        self.renumberWithinParts = self._get_meta_value('renumberWithinParts', None) == '1'
        self.romanChapterNumbers = self._get_meta_value('romanChapterNumbers', None) == '1'
        self.romanPartNumbers = self._get_meta_value('romanPartNumbers', None) == '1'
        self.saveWordCount = self._get_meta_value('saveWordCount', None) == '1'
        workPhase = self._get_meta_value('workPhase', None)
        if workPhase in ('1', '2', '3', '4', '5'):
            self.workPhase = int(workPhase)
        else:
            self.workPhase = None

        # Author.
        self.authorName = self._get_meta_value('Author')

        # Chapter heading prefix/suffix.
        chapterHeadingPrefix = self._get_meta_value('ChapterHeadingPrefix')
        if chapterHeadingPrefix:
            chapterHeadingPrefix = chapterHeadingPrefix[1:-1]
        self.chapterHeadingPrefix = chapterHeadingPrefix

        chapterHeadingSuffix = self._get_meta_value('ChapterHeadingSuffix')
        if chapterHeadingSuffix:
            chapterHeadingSuffix = chapterHeadingSuffix[1:-1]
        self.chapterHeadingSuffix = chapterHeadingSuffix

        # Part heading prefix/suffix.
        partHeadingPrefix = self._get_meta_value('PartHeadingPrefix')
        if partHeadingPrefix:
            partHeadingPrefix = partHeadingPrefix[1:-1]
        self.partHeadingPrefix = partHeadingPrefix

        partHeadingSuffix = self._get_meta_value('PartHeadingSuffix')
        if partHeadingSuffix:
            partHeadingSuffix = partHeadingSuffix[1:-1]
        self.partHeadingSuffix = partHeadingSuffix

        # N/A Goal/Conflict/Outcome.
        self.customPlotProgress = self._get_meta_value('CustomPlotProgress')
        self.customCharacterization = self._get_meta_value('CustomCharacterization')
        self.customWorldBuilding = self._get_meta_value('CustomWorldBuilding')

        # Custom Goal/Conflict/Outcome.
        self.customGoal = self._get_meta_value('CustomGoal')
        self.customConflict = self._get_meta_value('CustomConflict')
        self.customOutcome = self._get_meta_value('CustomOutcome')

        # Custom Character Bio/Goals.
        self.customChrBio = self._get_meta_value('CustomChrBio')
        self.customChrGoals = self._get_meta_value('CustomChrGoals')

        # Word count start/Word target.
        ws = self._get_meta_value('WordCountStart')
        if ws is not None:
            self.wordCountStart = int(ws)
        wt = self._get_meta_value('WordTarget')
        if wt is not None:
            self.wordTarget = int(wt)

        # Reference date.
        self.referenceDate = verified_date(self._get_meta_value('ReferenceDate'))

    def to_yaml(self, yaml):
        yaml = super().to_yaml(yaml)
        if self.renumberChapters:
            yaml.append(f'renumberChapters: 1')
        if self.renumberParts:
            yaml.append(f'renumberParts: 1')
        if self.renumberWithinParts:
            yaml.append(f'renumberWithinParts: 1')
        if self.romanChapterNumbers:
            yaml.append(f'romanChapterNumbers: 1')
        if self.romanPartNumbers:
            yaml.append(f'romanPartNumbers: 1')
        if self.saveWordCount:
            yaml.append(f'saveWordCount: 1')
        if self.workPhase is not None:
            yaml.append(f'workPhase: {self.workPhase}')

        # Author.
        if self.authorName:
            yaml.append(f'Author: {self.authorName}')

        # Chapter heading prefix/suffix.
        if self.chapterHeadingPrefix:
            yaml.append(f'ChapterHeadingPrefix: "{self.chapterHeadingPrefix}"')
        if self.chapterHeadingSuffix:
            yaml.append(f'ChapterHeadingSuffix: "{self.chapterHeadingSuffix}"')

        # Part heading prefix/suffix.
        if self.partHeadingPrefix:
            yaml.append(f'PartHeadingPrefix: "{self.partHeadingPrefix}"')
        if self.partHeadingSuffix:
            yaml.append(f'PartHeadingSuffix: "{self.partHeadingSuffix}"')

        # Custom Plot progress/Characterization/World building.
        if self.customPlotProgress:
            yaml.append(f'CustomPlotProgress: {self.customPlotProgress}')
        if self.customCharacterization:
            yaml.append(f'CustomCharacterization: {self.customCharacterization}')
        if self.customWorldBuilding:
            yaml.append(f'CustomWorldBuilding: {self.customWorldBuilding}')

        # Custom Goal/Conflict/Outcome.
        if self.customGoal:
            yaml.append(f'CustomGoal: {self.customGoal}')
        if self.customConflict:
            yaml.append(f'CustomConflict: {self.customConflict}')
        if self.customOutcome:
            yaml.append(f'CustomOutcome: {self.customOutcome}')

        # Custom Character Bio/Goals.
        if self.customChrBio:
            yaml.append(f'CustomChrBio: {self.customChrBio}')
        if self.customChrGoals:
            yaml.append(f'CustomChrGoals: {self.customChrGoals}')

        # Word count start/Word target.
        if self.wordCountStart:
            yaml.append(f'WordCountStart: {self.wordCountStart}')
        if self.wordTarget:
            yaml.append(f'WordTarget: {self.wordTarget}')

        # Reference date.
        if self.referenceDate:
            yaml.append(f'ReferenceDate: {self.referenceDate}')
        return yaml

    def update_plot_lines(self):
        """Set section back references to PlotLine.sections and PlotPoint.sectionAssoc. """
        for scId in self.sections:
            self.sections[scId].scPlotPoints = {}
            self.sections[scId].scPlotLines = []
            for plId in self.plotLines:
                if scId in self.plotLines[plId].sections:
                    self.sections[scId].scPlotLines.append(plId)
                    for ppId in self.tree.get_children(plId):
                        if self.plotPoints[ppId].sectionAssoc == scId:
                            self.sections[scId].scPlotPoints[ppId] = plId
                            break

