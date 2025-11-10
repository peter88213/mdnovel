"""Provide a class for mdnovel element JSON import and export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.json.basic_element_notes_json import BasicElementNotesJson


class BasicElementTagsJson(BasicElementNotesJson):

    def import_data(self, element, json):
        super().import_data(element, json)
        element.tags = json.get('Tags', [])

    def export_data(self, element, json):
        json = super().export_data(element, json)
        if element.tags:
            json['Tags'] = element.tags
        return json

