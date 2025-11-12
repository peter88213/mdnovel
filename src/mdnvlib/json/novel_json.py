"""Provide a class for mdnovel element JSON import and export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.json.basic_element_json import BasicElementJson
from mdnvlib.novx_globals import verified_date


class NovelJson(BasicElementJson):

    def import_data(self, element, json):
        super().import_data(element, json)
        element.renumberChapters = json.get('renumberChapters', False)
        element.renumberParts = json.get('renumberParts', False)
        element.renumberWithinParts = json.get('renumberWithinParts', False)
        element.romanChapterNumbers = json.get('romanChapterNumbers', False)
        element.romanPartNumbers = json.get('romanPartNumbers', False)
        element.saveWordCount = json.get('saveWordCount', False)
        workPhase = json.get('workPhase', None)
        if workPhase in (1, 2, 3, 4, 5):
            element.workPhase = workPhase
        else:
            element.workPhase = None
        element.authorName = json.get('Author')
        element.chapterHeadingPrefix = json.get('ChapterHeadingPrefix', None)
        element.chapterHeadingSuffix = json.get('ChapterHeadingSuffix', None)
        element.partHeadingPrefix = json.get('PartHeadingPrefix', None)
        element.partHeadingSuffix = json.get('PartHeadingSuffix', None)
        element.noSceneField1 = json.get('CustomPlotProgress', None)
        element.noSceneField2 = json.get('CustomCharacterization', None)
        element.noSceneField3 = json.get('CustomWorldBuilding', None)
        element.otherSceneField1 = json.get('CustomGoal', None)
        element.otherSceneField2 = json.get('CustomConflict', None)
        element.otherSceneField3 = json.get('CustomOutcome', None)
        element.crField1 = json.get('CustomChrBio', None)
        element.crField2 = json.get('CustomChrGoals', None)
        element.wordCountStart = json.get('WordCountStart', None)
        element.wordTarget = json.get('WordTarget', None)
        element.referenceDate = verified_date(json.get('ReferenceDate', None))

    def export_data(self, element, json):
        json = super().export_data(element, json)
        if element.renumberChapters:
            json['renumberChapters'] = True
        if element.renumberParts:
            json['renumberParts'] = True
        if element.renumberWithinParts:
            json['renumberWithinParts'] = True
        if element.romanChapterNumbers:
            json['romanChapterNumbers'] = True
        if element.romanPartNumbers:
            json['romanPartNumbers'] = True
        if element.saveWordCount:
            json['saveWordCount'] = True
        if element.workPhase is not None:
            json['workPhase'] = element.workPhase

        # Author.
        if element.authorName:
            json['Author'] = element.authorName

        # Chapter heading prefix/suffix.
        if element.chapterHeadingPrefix:
            json['ChapterHeadingPrefix'] = element.chapterHeadingPrefix
        if element.chapterHeadingSuffix:
            json['ChapterHeadingSuffix'] = element.chapterHeadingSuffix

        # Part heading prefix/suffix.
        if element.partHeadingPrefix:
            json['PartHeadingPrefix'] = element.partHeadingPrefix
        if element.partHeadingSuffix:
            json['PartHeadingSuffix'] = element.partHeadingSuffix

        # Custom Plot progress/Characterization/World building.
        if element.noSceneField1:
            json['CustomPlotProgress'] = element.noSceneField1
        if element.noSceneField2:
            json['CustomCharacterization'] = element.noSceneField2
        if element.noSceneField3:
            json['CustomWorldBuilding'] = element.noSceneField3

        # Custom Goal/Conflict/Outcome.
        if element.otherSceneField1:
            json['CustomGoal'] = element.otherSceneField1
        if element.otherSceneField2:
            json['CustomConflict'] = element.otherSceneField2
        if element.otherSceneField3:
            json['CustomOutcome'] = element.otherSceneField3

        # Custom Character Bio/Goals.
        if element.crField1:
            json['CustomChrBio'] = element.crField1
        if element.crField2:
            json['CustomChrGoals'] = element.crField2

        # Word count start/Word target.
        if element.wordCountStart:
            json['WordCountStart'] = element.wordCountStart
        if element.wordTarget:
            json['WordTarget'] = element.wordTarget

        # Reference date.
        if element.referenceDate:
            json['ReferenceDate'] = element.referenceDate
        return json

