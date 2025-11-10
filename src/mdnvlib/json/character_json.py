"""Provide a class for mdnovel element JSON import and export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.json.world_element_json import WorldElementJson
from mdnvlib.novx_globals import verified_date


class CharacterJson(WorldElementJson):

    def import_data(self, element, json):
        super().import_data(element, json)
        element.isMajor = json.get('major', False)
        element.fullName = json.get('FullName')
        element.birthDate = verified_date(json.get('BirthDate', None))
        element.deathDate = verified_date(json.get('DeathDate', None))

    def export_data(self, element, json):
        json = super().export_data(element, json)
        if element.isMajor:
            json['major'] = True
        if element.fullName:
            json['FullName'] = element.fullName
        if element.birthDate:
            json['BirthDate'] = element.birthDate
        if element.deathDate:
            json['DeathDate'] = element.deathDate
        return json

