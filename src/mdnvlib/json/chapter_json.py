"""Provide a class for mdnovel element JSON import and export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.json.basic_element_notes_json import BasicElementNotesJson


class ChapterJson(BasicElementNotesJson):

    def import_data(self, element, json):
        super().import_data(element, json)
        chType = json.get('type', 0)
        if chType in (0, 1):
            element.chType = chType
        else:
            element.chType = 1
        chLevel = json.get('level', 2)
        if chLevel in (1, 2):
            element.chLevel = chLevel
        else:
            element.chLevel = 2
        element.isTrash = json.get('isTrash', False)
        element.noNumber = json.get('noNumber', False)

    def export_data(self, element, json):
        json = super().export_data(element, json)
        if element.chType:
            json['type'] = element.chType
        if element.chLevel == 1:
            json['level'] = 1
        if element.isTrash:
            json['isTrash'] = True
        if element.noNumber:
            json['noNumber'] = True
        return json
