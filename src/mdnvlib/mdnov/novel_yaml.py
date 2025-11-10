"""Provide a class for mdnovel element YAML import and export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.mdnov.basic_element_yaml import BasicElementYaml
from mdnvlib.novx_globals import verified_date


class NovelYaml(BasicElementYaml):

    def import_data(self, element, yaml):
        super().import_data(element, yaml)
        element.renumberChapters = self._get_meta_value('renumberChapters', None) == '1'
        element.renumberParts = self._get_meta_value('renumberParts', None) == '1'
        element.renumberWithinParts = self._get_meta_value('renumberWithinParts', None) == '1'
        element.romanChapterNumbers = self._get_meta_value('romanChapterNumbers', None) == '1'
        element.romanPartNumbers = self._get_meta_value('romanPartNumbers', None) == '1'
        element.saveWordCount = self._get_meta_value('saveWordCount', None) == '1'
        workPhase = self._get_meta_value('workPhase', None)
        if workPhase in ('1', '2', '3', '4', '5'):
            element.workPhase = int(workPhase)
        else:
            element.workPhase = None

        # Author.
        element.authorName = self._get_meta_value('Author')

        # Chapter heading prefix/suffix.
        chapterHeadingPrefix = self._get_meta_value('ChapterHeadingPrefix')
        if chapterHeadingPrefix:
            chapterHeadingPrefix = chapterHeadingPrefix[1:-1]
        element.chapterHeadingPrefix = chapterHeadingPrefix

        chapterHeadingSuffix = self._get_meta_value('ChapterHeadingSuffix')
        if chapterHeadingSuffix:
            chapterHeadingSuffix = chapterHeadingSuffix[1:-1]
        element.chapterHeadingSuffix = chapterHeadingSuffix

        # Part heading prefix/suffix.
        partHeadingPrefix = self._get_meta_value('PartHeadingPrefix')
        if partHeadingPrefix:
            partHeadingPrefix = partHeadingPrefix[1:-1]
        element.partHeadingPrefix = partHeadingPrefix

        partHeadingSuffix = self._get_meta_value('PartHeadingSuffix')
        if partHeadingSuffix:
            partHeadingSuffix = partHeadingSuffix[1:-1]
        element.partHeadingSuffix = partHeadingSuffix

        # N/A Goal/Conflict/Outcome.
        element.customPlotProgress = self._get_meta_value('CustomPlotProgress')
        element.customCharacterization = self._get_meta_value('CustomCharacterization')
        element.customWorldBuilding = self._get_meta_value('CustomWorldBuilding')

        # Custom Goal/Conflict/Outcome.
        element.customGoal = self._get_meta_value('CustomGoal')
        element.customConflict = self._get_meta_value('CustomConflict')
        element.customOutcome = self._get_meta_value('CustomOutcome')

        # Custom Character Bio/Goals.
        element.customChrBio = self._get_meta_value('CustomChrBio')
        element.customChrGoals = self._get_meta_value('CustomChrGoals')

        # Word count start/Word target.
        ws = self._get_meta_value('WordCountStart')
        if ws is not None:
            element.wordCountStart = int(ws)
        wt = self._get_meta_value('WordTarget')
        if wt is not None:
            element.wordTarget = int(wt)

        # Reference date.
        element.referenceDate = verified_date(self._get_meta_value('ReferenceDate'))

    def export_data(self, element, yaml):
        yaml = super().export_data(element, yaml)
        if element.renumberChapters:
            yaml.append(f'renumberChapters: 1')
        if element.renumberParts:
            yaml.append(f'renumberParts: 1')
        if element.renumberWithinParts:
            yaml.append(f'renumberWithinParts: 1')
        if element.romanChapterNumbers:
            yaml.append(f'romanChapterNumbers: 1')
        if element.romanPartNumbers:
            yaml.append(f'romanPartNumbers: 1')
        if element.saveWordCount:
            yaml.append(f'saveWordCount: 1')
        if element.workPhase is not None:
            yaml.append(f'workPhase: {element.workPhase}')

        # Author.
        if element.authorName:
            yaml.append(f'Author: {element.authorName}')

        # Chapter heading prefix/suffix.
        if element.chapterHeadingPrefix:
            yaml.append(f'ChapterHeadingPrefix: "{element.chapterHeadingPrefix}"')
        if element.chapterHeadingSuffix:
            yaml.append(f'ChapterHeadingSuffix: "{element.chapterHeadingSuffix}"')

        # Part heading prefix/suffix.
        if element.partHeadingPrefix:
            yaml.append(f'PartHeadingPrefix: "{element.partHeadingPrefix}"')
        if element.partHeadingSuffix:
            yaml.append(f'PartHeadingSuffix: "{element.partHeadingSuffix}"')

        # Custom Plot progress/Characterization/World building.
        if element.customPlotProgress:
            yaml.append(f'CustomPlotProgress: {element.customPlotProgress}')
        if element.customCharacterization:
            yaml.append(f'CustomCharacterization: {element.customCharacterization}')
        if element.customWorldBuilding:
            yaml.append(f'CustomWorldBuilding: {element.customWorldBuilding}')

        # Custom Goal/Conflict/Outcome.
        if element.customGoal:
            yaml.append(f'CustomGoal: {element.customGoal}')
        if element.customConflict:
            yaml.append(f'CustomConflict: {element.customConflict}')
        if element.customOutcome:
            yaml.append(f'CustomOutcome: {element.customOutcome}')

        # Custom Character Bio/Goals.
        if element.customChrBio:
            yaml.append(f'CustomChrBio: {element.customChrBio}')
        if element.customChrGoals:
            yaml.append(f'CustomChrGoals: {element.customChrGoals}')

        # Word count start/Word target.
        if element.wordCountStart:
            yaml.append(f'WordCountStart: {element.wordCountStart}')
        if element.wordTarget:
            yaml.append(f'WordTarget: {element.wordTarget}')

        # Reference date.
        if element.referenceDate:
            yaml.append(f'ReferenceDate: {element.referenceDate}')
        return yaml

