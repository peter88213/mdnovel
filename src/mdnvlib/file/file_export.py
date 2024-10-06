"""Provide a generic class for template-based file export.

All file representations with template-based write methods inherit from this class.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnvlib
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from string import Template

from mdnvlib.file.file import File
from mdnvlib.file.filter import Filter
from mdnvlib.model.character import Character
from mdnvlib.model.section import Section
from mdnvlib.novx_globals import CHARACTERS_SUFFIX
from mdnvlib.novx_globals import CH_ROOT
from mdnvlib.novx_globals import CR_ROOT
from mdnvlib.novx_globals import Error
from mdnvlib.novx_globals import ITEMS_SUFFIX
from mdnvlib.novx_globals import IT_ROOT
from mdnvlib.novx_globals import LC_ROOT
from mdnvlib.novx_globals import LOCATIONS_SUFFIX
from mdnvlib.novx_globals import MONTHS
from mdnvlib.novx_globals import PL_ROOT
from mdnvlib.novx_globals import PN_ROOT
from mdnvlib.novx_globals import SECTIONS_SUFFIX
from mdnvlib.novx_globals import WEEKDAYS
from mdnvlib.novx_globals import _
from mdnvlib.novx_globals import list_to_string
from mdnvlib.novx_globals import norm_path


class FileExport(File):
    """Abstract novelibre project file exporter representation.
    
    This class is generic and contains no conversion algorithm and no templates.
    """
    SUFFIX = ''
    _fileHeader = ''
    _partTemplate = ''
    _chapterTemplate = ''
    _unusedChapterTemplate = ''
    _sectionTemplate = ''
    _firstSectionTemplate = ''
    _unusedSectionTemplate = ''
    _stage1Template = ''
    _stage2Template = ''
    _sectionDivider = ''
    _chapterEndTemplate = ''
    _unusedChapterEndTemplate = ''
    _characterSectionHeading = ''
    _characterTemplate = ''
    _locationSectionHeading = ''
    _locationTemplate = ''
    _itemSectionHeading = ''
    _itemTemplate = ''
    _fileFooter = ''
    _projectNoteTemplate = ''
    _arcTemplate = ''

    _DIVIDER = ', '

    def __init__(self, filePath, **kwargs):
        """Initialize filter strategy class instances.
        
        Positional arguments:
            filePath: str -- path to the file represented by the File instance.
            
        Optional arguments:
            kwargs -- keyword arguments to be used by subclasses.            

        Extends the superclass constructor.
        """
        super().__init__(filePath, **kwargs)
        self.sectionFilter = Filter()
        self.chapterFilter = Filter()
        self.characterFilter = Filter()
        self.locationFilter = Filter()
        self.itemFilter = Filter()
        self.arcFilter = Filter()
        self.turningPointFilter = Filter()

    def write(self):
        """Write instance variables to the export file.
        
        Create a template-based output file. 
        Return a message in case of success.
        Raise the "Error" exception in case of error. 
        """
        text = self._get_text()
        backedUp = False
        if os.path.isfile(self.filePath):
            try:
                os.replace(self.filePath, f'{self.filePath}.bak')
            except:
                raise Error(f'{_("Cannot overwrite file")}: "{norm_path(self.filePath)}".')
            else:
                backedUp = True
        try:
            with open(self.filePath, 'w', encoding='utf-8') as f:
                f.write(text)
        except:
            if backedUp:
                os.replace(f'{self.filePath}.bak', self.filePath)
            raise Error(f'{_("Cannot write file")}: "{norm_path(self.filePath)}".')

    def _convert_from_novx(self, text, **kwargs):
        """Return text without markup, converted to target format.
        
        Positional arguments:
            text -- string to convert.
        
        Optional arguments:
            quick: bool -- if True, apply a conversion mode for one-liners without formatting.
            append: bool -- if True, indent the first paragraph.
            firstInChapter: bool: -- if True, the section begins a chapter.
            xml: bool -- if True, parse XML content. 
        
        Overrides the superclass method.
        """
        if text is None:
            text = ''
        return(text)

    def _get_arcMapping(self, plId):
        """Return a mapping dictionary for a plot line section.
        
        Positional arguments:
            plId: str -- plot line ID.
        
        This is a template method that can be extended or overridden by subclasses.
        """
        arcMapping = dict(
            ID=plId,
            Title=self._convert_from_novx(self.novel.plotLines[plId].title, quick=True),
            Desc=self._convert_from_novx(self.novel.plotLines[plId].desc),
            Notes=self._convert_from_novx(self.novel.plotLines[plId].notes),
            ProjectName=self._convert_from_novx(self.projectName, quick=True),
            ProjectPath=self.projectPath,
            Language=self.novel.languageCode,
            Country=self.novel.countryCode,
        )
        return arcMapping

    def _get_arcs(self):
        """Process the plot lines. 
        
        Iterate through the sorted plot line list and apply the template, 
        substituting placeholders according to the plot line mapping dictionary.
        Skip plot lines not accepted by the plot line filter.
        Return a list of strings.
        This is a template method that can be extended or overridden by subclasses.
        """
        lines = []
        for plId in self.novel.tree.get_children(PL_ROOT):
            if self.arcFilter.accept(self, plId):
                if self._arcTemplate:
                    template = Template(self._arcTemplate)
                    lines.append(template.safe_substitute(self._get_arcMapping(plId)))
        return lines

    def _get_chapterMapping(self, chId, chapterNumber):
        """Return a mapping dictionary for a chapter section.
        
        Positional arguments:
            chId: str -- chapter ID.
            chapterNumber: int -- chapter number.
        
        This is a template method that can be extended or overridden by subclasses.
        """
        if chapterNumber == 0:
            chapterNumber = ''

        chapterMapping = dict(
            ID=chId,
            ChapterNumber=chapterNumber,
            Title=self._convert_from_novx(self.novel.chapters[chId].title, quick=True),
            Desc=self._convert_from_novx(self.novel.chapters[chId].desc),
            Notes=self._convert_from_novx(self.novel.chapters[chId].notes),
            ProjectName=self._convert_from_novx(self.projectName, quick=True),
            ProjectPath=self.projectPath,
            Language=self.novel.languageCode,
            Country=self.novel.countryCode,
        )
        return chapterMapping

    def _get_chapters(self):
        """Process the chapters and nested sections.
        
        Iterate through the sorted chapter list and apply the templates, 
        substituting placeholders according to the chapter mapping dictionary.
        For each chapter call the processing of its included sections.
        Skip chapters not accepted by the chapter filter.
        Return a list of strings.
        This is a template method that can be extended or overridden by subclasses.
        """
        lines = []
        chapterNumber = 0
        sectionNumber = 0
        wordsTotal = 0
        for chId in self.novel.tree.get_children(CH_ROOT):
            dispNumber = 0
            if not self.chapterFilter.accept(self, chId):
                continue

            # The order counts; be aware that "Todo" and "Notes" chapters are
            # always unused.
            # Has the chapter only sections not to be exported?
            template = None
            if self.novel.chapters[chId].chType == 1:
                # Chapter is "unused" type.
                if self._unusedChapterTemplate:
                    template = Template(self._unusedChapterTemplate)
            elif self.novel.chapters[chId].chLevel == 1 and self._partTemplate:
                template = Template(self._partTemplate)
            else:
                template = Template(self._chapterTemplate)
                chapterNumber += 1
                dispNumber = chapterNumber
            if template is not None:
                lines.append(template.safe_substitute(self._get_chapterMapping(chId, dispNumber)))

            #--- Process sections.
            sectionLines, sectionNumber, wordsTotal = self._get_sections(chId, sectionNumber, wordsTotal)
            lines.extend(sectionLines)

            #--- Process chapter ending.
            template = None
            if self.novel.chapters[chId].chType == 1:
                if self._unusedChapterEndTemplate:
                    template = Template(self._unusedChapterEndTemplate)
            elif self._chapterEndTemplate:
                template = Template(self._chapterEndTemplate)
            if template is not None:
                lines.append(template.safe_substitute(self._get_chapterMapping(chId, dispNumber)))
        return lines

    def _get_characterMapping(self, crId):
        """Return a mapping dictionary for a character section.
        
        Positional arguments:
            crId: str -- character ID.
        
        This is a template method that can be extended or overridden by subclasses.
        """
        if self.novel.characters[crId].tags is not None:
            tags = list_to_string(self.novel.characters[crId].tags, divider=self._DIVIDER)
        else:
            tags = ''
        if self.novel.characters[crId].isMajor:
            characterStatus = Character.MAJOR_MARKER
        else:
            characterStatus = Character.MINOR_MARKER

        __, __, __, __, __, __, chrBio, chrGls = self._get_renamings()

        characterMapping = dict(
            ID=crId,
            Title=self._convert_from_novx(self.novel.characters[crId].title, quick=True),
            Desc=self._convert_from_novx(self.novel.characters[crId].desc),
            Tags=self._convert_from_novx(tags),
            AKA=self._convert_from_novx(self.novel.characters[crId].aka, quick=True),
            Notes=self._convert_from_novx(self.novel.characters[crId].notes),
            Bio=self._convert_from_novx(self.novel.characters[crId].bio),
            Goals=self._convert_from_novx(self.novel.characters[crId].goals),
            FullName=self._convert_from_novx(self.novel.characters[crId].fullName, quick=True),
            Status=characterStatus,
            ProjectName=self._convert_from_novx(self.projectName, quick=True),
            ProjectPath=self.projectPath,
            CharactersSuffix=CHARACTERS_SUFFIX,
            CustomChrBio=chrBio,
            CustomChrGoals=chrGls
        )
        return characterMapping

    def _get_characters(self):
        """Process the characters.
        
        Iterate through the sorted character list and apply the template, 
        substituting placeholders according to the character mapping dictionary.
        Skip characters not accepted by the character filter.
        Return a list of strings.
        This is a template method that can be extended or overridden by subclasses.
        """
        if self._characterSectionHeading:
            lines = [self._characterSectionHeading]
        else:
            lines = []
        template = Template(self._characterTemplate)
        for crId in self.novel.tree.get_children(CR_ROOT):
            if self.characterFilter.accept(self, crId):
                lines.append(template.safe_substitute(self._get_characterMapping(crId)))
        return lines

    def _get_fileFooter(self):
        lines = []
        template = Template(self._fileFooter)
        lines.append(template.safe_substitute(self._get_fileFooterMapping()))
        return lines

    def _get_fileFooterMapping(self):
        return []

    def _get_fileHeader(self):
        """Process the file header.
        
        Apply the file header template, substituting placeholders 
        according to the file header mapping dictionary.
        Return a list of strings.
        
        This is a template method that can be extended or overridden by subclasses.
        """
        lines = []
        template = Template(self._fileHeader)
        lines.append(template.safe_substitute(self._get_fileHeaderMapping()))
        return lines

    def _get_fileHeaderMapping(self):
        """Return a mapping dictionary for the project section.
        
        This is a template method that can be extended or overridden by subclasses.
        """
        filterMessages = []
        expFilters = [
            self.chapterFilter,
            self.sectionFilter,
            self.characterFilter,
            self.locationFilter,
            self.itemFilter,
            self.arcFilter,
            self.turningPointFilter,
            ]
        for expFilter in expFilters:
            message = expFilter.get_message(self)
            if message:
                filterMessages.append(message)
            if filterMessages:
                filters = self._convert_from_novx('\n'.join(filterMessages))
            else:
                filters = ''
            pltPrgs, chrczn, wrldbld, goal, cflct, outcm, chrBio, chrGls = self._get_renamings()

        fileHeaderMapping = dict(
            Title=self._convert_from_novx(self.novel.title, quick=True),
            Filters=filters,
            Desc=self._convert_from_novx(self.novel.desc),
            AuthorName=self._convert_from_novx(self.novel.authorName, quick=True),
            Language=self.novel.languageCode,
            Country=self.novel.countryCode,
            CustomPlotProgress=pltPrgs,
            CustomCharacterization=chrczn,
            CustomWorldBuilding=wrldbld,
            CustomGoal=goal,
            CustomConflict=cflct,
            CustomOutcome=outcm,
            CustomChrBio=chrBio,
            CustomChrGoals=chrGls
        )
        return fileHeaderMapping

    def _get_itemMapping(self, itId):
        """Return a mapping dictionary for an item section.
        
        Positional arguments:
            itId: str -- item ID.
        
        This is a template method that can be extended or overridden by subclasses.
        """
        if self.novel.items[itId].tags is not None:
            tags = list_to_string(self.novel.items[itId].tags, divider=self._DIVIDER)
        else:
            tags = ''

        itemMapping = dict(
            ID=itId,
            Title=self._convert_from_novx(self.novel.items[itId].title, quick=True),
            Desc=self._convert_from_novx(self.novel.items[itId].desc),
            Notes=self._convert_from_novx(self.novel.items[itId].notes),
            Tags=self._convert_from_novx(tags, quick=True),
            AKA=self._convert_from_novx(self.novel.items[itId].aka, quick=True),
            ProjectName=self._convert_from_novx(self.projectName, quick=True),
            ProjectPath=self.projectPath,
            ItemsSuffix=ITEMS_SUFFIX,
        )
        return itemMapping

    def _get_items(self):
        """Process the items. 
        
        Iterate through the sorted item list and apply the template, 
        substituting placeholders according to the item mapping dictionary.
        Skip items not accepted by the item filter.
        Return a list of strings.
        This is a template method that can be extended or overridden by subclasses.
        """
        if self._itemSectionHeading:
            lines = [self._itemSectionHeading]
        else:
            lines = []
        template = Template(self._itemTemplate)
        for itId in self.novel.tree.get_children(IT_ROOT):
            if self.itemFilter.accept(self, itId):
                lines.append(template.safe_substitute(self._get_itemMapping(itId)))
        return lines

    def _get_locationMapping(self, lcId):
        """Return a mapping dictionary for a location section.
        
        Positional arguments:
            lcId: str -- location ID.
        
        This is a template method that can be extended or overridden by subclasses.
        """
        if self.novel.locations[lcId].tags is not None:
            tags = list_to_string(self.novel.locations[lcId].tags, divider=self._DIVIDER)
        else:
            tags = ''

        locationMapping = dict(
            ID=lcId,
            Title=self._convert_from_novx(self.novel.locations[lcId].title, quick=True),
            Desc=self._convert_from_novx(self.novel.locations[lcId].desc),
            Notes=self._convert_from_novx(self.novel.locations[lcId].notes),
            Tags=self._convert_from_novx(tags, quick=True),
            AKA=self._convert_from_novx(self.novel.locations[lcId].aka, quick=True),
            ProjectName=self._convert_from_novx(self.projectName, quick=True),
            ProjectPath=self.projectPath,
            LocationsSuffix=LOCATIONS_SUFFIX,
        )
        return locationMapping

    def _get_locations(self):
        """Process the locations.
        
        Iterate through the sorted location list and apply the template, 
        substituting placeholders according to the location mapping dictionary.
        Skip locations not accepted by the location filter.
        Return a list of strings.
        This is a template method that can be extended or overridden by subclasses.
        """
        if self._locationSectionHeading:
            lines = [self._locationSectionHeading]
        else:
            lines = []
        template = Template(self._locationTemplate)
        for lcId in self.novel.tree.get_children(LC_ROOT):
            if self.locationFilter.accept(self, lcId):
                lines.append(template.safe_substitute(self._get_locationMapping(lcId)))
        return lines

    def _get_renamings(self):
        if self.novel.customPlotProgress:
            pltPrgs = self.novel.customPlotProgress
        else:
            pltPrgs = _('Plot progress')
        if self.novel.customCharacterization:
            chrczn = self.novel.customCharacterization
        else:
            chrczn = _('Characterization')
        if self.novel.customWorldBuilding:
            wrldbld = self.novel.customWorldBuilding
        else:
            wrldbld = _('World building')
        if self.novel.customGoal:
            goal = self.novel.customGoal
        else:
            goal = _('Opening')
        if self.novel.customConflict:
            cflct = self.novel.customConflict
        else:
            cflct = _('Peak em. moment')
        if self.novel.customOutcome:
            outcm = self.novel.customOutcome
        else:
            outcm = _('Ending')
        if self.novel.customChrBio:
            chrBio = self.novel.customChrBio
        else:
            chrBio = _('Bio')
        if self.novel.customChrGoals:
            chrGls = self.novel.customChrGoals
        else:
            chrGls = _('Goals')
        return pltPrgs, chrczn, wrldbld, goal, cflct, outcm, chrBio, chrGls

    def _get_sectionMapping(self, scId, sectionNumber, wordsTotal, firstInChapter=False):
        """Return a mapping dictionary for a section section.
        
        Positional arguments:
            scId: str -- section ID.
            sectionNumber: int -- section number to be displayed.
            wordsTotal: int -- accumulated wordcount.
        Optional arguments:
            firstInChapter: bool: -- if True, the section begins a chapter.
        
        This is a template method that can be extended or overridden by subclasses.
        """

        #--- Create a comma separated tag list.
        if sectionNumber == 0:
            sectionNumber = ''
        if self.novel.sections[scId].tags is not None:
            tags = list_to_string(self.novel.sections[scId].tags, divider=self._DIVIDER)
        else:
            tags = ''

        #--- Create a comma separated character list.
        if self.novel.sections[scId].characters is not None:
            sChList = []
            for crId in self.novel.sections[scId].characters:
                sChList.append(self.novel.characters[crId].title)
            sectionChars = list_to_string(sChList, divider=self._DIVIDER)

            if sChList:
                viewpointChar = sChList[0]
            else:
                viewpointChar = ''
        else:
            sectionChars = ''
            viewpointChar = ''

        #--- Create a comma separated location list.
        if self.novel.sections[scId].locations is not None:
            sLcList = []
            for lcId in self.novel.sections[scId].locations:
                sLcList.append(self.novel.locations[lcId].title)
            sectionLocs = list_to_string(sLcList, divider=self._DIVIDER)
        else:
            sectionLocs = ''

        #--- Create a comma separated item list.
        if self.novel.sections[scId].items is not None:
            sItList = []
            for itId in self.novel.sections[scId].items:
                sItList.append(self.novel.items[itId].title)
            sectionItems = list_to_string(sItList, divider=self._DIVIDER)
        else:
            sectionItems = ''

        #--- Date or day.
        if self.novel.sections[scId].date is not None and self.novel.sections[scId].date != Section.NULL_DATE:
            scDay = ''
            isoDate = self.novel.sections[scId].date
            cmbDate = self.novel.sections[scId].localeDate
            yearStr, monthStr, dayStr = isoDate.split('-')
            dtMonth = MONTHS[int(monthStr) - 1]
            dtWeekday = WEEKDAYS[self.novel.sections[scId].weekDay]
        else:
            isoDate = ''
            yearStr = ''
            monthStr = ''
            dayStr = ''
            dtMonth = ''
            dtWeekday = ''
            if self.novel.sections[scId].day is not None:
                scDay = self.novel.sections[scId].day
                cmbDate = f'{_("Day")} {self.novel.sections[scId].day}'
            else:
                scDay = ''
                cmbDate = ''

        #--- Time.
        if self.novel.sections[scId].time is not None:
            h, m, s = self.novel.sections[scId].time.split(':')
            scTime = f'{h}:{m}'
            odsTime = f'PT{h}H{m}M{s}S'
            # removing seconds
        else:
            scTime = ''
            odsTime = ''

        #--- Create a combined duration information.
        if self.novel.sections[scId].lastsDays is not None and self.novel.sections[scId].lastsDays != '0':
            lastsDays = self.novel.sections[scId].lastsDays
            days = f'{self.novel.sections[scId].lastsDays}d '
        else:
            lastsDays = ''
            days = ''

        if self.novel.sections[scId].lastsHours is not None and self.novel.sections[scId].lastsHours != '0':
            lastsHours = self.novel.sections[scId].lastsHours
            hours = f'{self.novel.sections[scId].lastsHours}h '
        else:
            lastsHours = ''
            hours = ''

        if self.novel.sections[scId].lastsMinutes is not None and self.novel.sections[scId].lastsMinutes != '0':
            lastsMinutes = self.novel.sections[scId].lastsMinutes
            minutes = f'{self.novel.sections[scId].lastsMinutes}min'
        else:
            lastsMinutes = ''
            minutes = ''

        duration = f'{days}{hours}{minutes}'

        pltPrgs, chrczn, wrldbld, goal, cflct, outcm, __, __ = self._get_renamings()
        sectionMapping = dict(
            ID=scId,
            SectionNumber=sectionNumber,
            Title=self._convert_from_novx(
                self.novel.sections[scId].title,
                quick=True
                ),
            Desc=self._convert_from_novx(
                self.novel.sections[scId].desc,
                append=self.novel.sections[scId].appendToPrev
                ),
            WordCount=str(self.novel.sections[scId].wordCount),
            WordsTotal=wordsTotal,
            Status=int(self.novel.sections[scId].status),
            SectionContent=self._convert_from_novx(
                        self.novel.sections[scId].sectionContent,
                        append=self.novel.sections[scId].appendToPrev,
                        firstInChapter=firstInChapter,
                        xml=True
                        ),
            Date=isoDate,
            Time=scTime,
            OdsTime=odsTime,
            Day=scDay,
            ScDate=cmbDate,
            DateYear=yearStr,
            DateMonth=monthStr,
            DateDay=dayStr,
            DateWeekday=dtWeekday,
            MonthName=dtMonth,
            LastsDays=lastsDays,
            LastsHours=lastsHours,
            LastsMinutes=lastsMinutes,
            Duration=duration,
            Scene=Section.SCENE[self.novel.sections[scId].scene],
            Goal=self._convert_from_novx(self.novel.sections[scId].goal),
            Conflict=self._convert_from_novx(self.novel.sections[scId].conflict),
            Outcome=self._convert_from_novx(self.novel.sections[scId].outcome),
            Tags=self._convert_from_novx(tags, quick=True),
            Characters=sectionChars,
            Viewpoint=viewpointChar,
            Locations=sectionLocs,
            Items=sectionItems,
            Notes=self._convert_from_novx(self.novel.sections[scId].notes),
            ProjectName=self._convert_from_novx(self.projectName, quick=True),
            ProjectPath=self.projectPath,
            Language=self.novel.languageCode,
            Country=self.novel.countryCode,
            SectionsSuffix=SECTIONS_SUFFIX,
            CustomPlotProgress=pltPrgs,
            CustomCharacterization=chrczn,
            CustomWorldBuilding=wrldbld,
            CustomGoal=goal,
            CustomConflict=cflct,
            CustomOutcome=outcm
        )
        return sectionMapping

    def _get_sections(self, chId, sectionNumber, wordsTotal):
        """Process the sections.
        
        Positional arguments:
            chId: str -- chapter ID.
            sectionNumber: int -- number of previously processed sections.
            wordsTotal: int -- accumulated wordcount of the previous sections.
        
        Iterate through a sorted section list and apply the templates, 
        substituting placeholders according to the section mapping dictionary.
        Skip sections not accepted by the section filter.
        
        Return a tuple:
            lines: list of strings -- the lines of the processed section.
            sectionNumber: int -- number of all processed sections.
            wordsTotal: int -- accumulated wordcount of all processed sections.
        
        This is a template method that can be extended or overridden by subclasses.
        """
        lines = []
        firstSectionInChapter = True
        for scId in self.novel.tree.get_children(chId):
            template = None
            dispNumber = 0
            if not self.sectionFilter.accept(self, scId):
                continue

            sectionContent = self.novel.sections[scId].sectionContent
            if sectionContent is None:
                sectionContent = ''

            if self.novel.sections[scId].scType == 2:
                if self._stage1Template:
                    template = Template(self._stage1Template)
                else:
                    continue

            elif self.novel.sections[scId].scType == 3:
                if self._stage2Template:
                    template = Template(self._stage2Template)
                else:
                    continue

            elif self.novel.sections[scId].scType == 1 or self.novel.chapters[chId].chType == 1:
                if self._unusedSectionTemplate:
                    template = Template(self._unusedSectionTemplate)
                else:
                    continue

            else:
                sectionNumber += 1
                dispNumber = sectionNumber
                wordsTotal += self.novel.sections[scId].wordCount
                template = Template(self._sectionTemplate)
                if firstSectionInChapter and self._firstSectionTemplate:
                    template = Template(self._firstSectionTemplate)
            if not (firstSectionInChapter or self.novel.sections[scId].appendToPrev or self.novel.sections[scId].scType > 1):
                lines.append(self._sectionDivider)
            if template is not None:
                lines.append(
                    template.safe_substitute(
                        self._get_sectionMapping(
                            scId, dispNumber,
                            wordsTotal,
                            firstInChapter=firstSectionInChapter,
                            )
                        )
                    )
            if self.novel.sections[scId].scType < 2:
                firstSectionInChapter = False
        return lines, sectionNumber, wordsTotal

    def _get_prjNoteMapping(self, pnId):
        """Return a mapping dictionary for a project note.
        
        Positional arguments:
            pnId: str -- project note ID.
        
        This is a template method that can be extended or overridden by subclasses.
        """
        noteMapping = dict(
            ID=pnId,
            Title=self._convert_from_novx(self.novel.projectNotes[pnId].title, quick=True),
            Desc=self._convert_from_novx(self.novel.projectNotes[pnId].desc),
            ProjectName=self._convert_from_novx(self.projectName, quick=True),
            ProjectPath=self.projectPath,
        )
        return noteMapping

    def _get_projectNotes(self):
        """Process the project notes. 
        
        Iterate through the sorted project note list and apply the template, 
        substituting placeholders according to the item mapping dictionary.
        Skip items not accepted by the item filter.
        Return a list of strings.
        This is a template method that can be extended or overridden by subclasses.
        """
        lines = []
        template = Template(self._projectNoteTemplate)
        for pnId in self.novel.tree.get_children(PN_ROOT):
            pnMap = self._get_prjNoteMapping(pnId)
            lines.append(template.safe_substitute(pnMap))
        return lines

    def _get_text(self):
        """Call all processing methods.
        
        Return a string to be written to the output file.
        This is a template method that can be extended or overridden by subclasses.
        """
        lines = self._get_fileHeader()
        lines.extend(self._get_chapters())
        lines.extend(self._get_characters())
        lines.extend(self._get_locations())
        lines.extend(self._get_items())
        lines.extend(self._get_arcs())
        lines.extend(self._get_projectNotes())
        lines.extend(self._get_fileFooter())
        return ''.join(lines)

