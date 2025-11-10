"""Provide a class for mdnovel element JSON import and export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.json.basic_element_json import BasicElementJson


class BasicElementNotesJson(BasicElementJson):
    """Basic element with notes."""

    def import_data(self, element, json):
        super().import_data(element, json)
        element.notes = json.get('Notes', None)

    def export_data(self, element, json):
        json = super().export_data(element, json)
        if element.notes:
            json['Notes'] = element.notes
        return json
