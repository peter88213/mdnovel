"""Provide a class for mdnovel element YAML import and export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.mdnov.basic_element_tags_yaml import BasicElementTagsYaml
from mdnvlib.novx_globals import list_to_string
from mdnvlib.novx_globals import string_to_list
from mdnvlib.novx_globals import verified_date
from mdnvlib.novx_globals import verified_int_string
from mdnvlib.novx_globals import verified_time


class SectionYaml(BasicElementTagsYaml):

    def import_data(self, element, yaml):
        super().import_data(element, yaml)

        # Attributes.
        typeStr = self._get_meta_value('type', '0')
        if typeStr in ('0', '1', '2', '3'):
            element.scType = int(typeStr)
        else:
            element.scType = 1
        status = self._get_meta_value('status', None)
        if status in ('2', '3', '4', '5'):
            element.status = int(status)
        else:
            element.status = 1
        scene = self._get_meta_value('scene', 0)
        if scene in ('1', '2', '3'):
            element.scene = int(scene)
        else:
            element.scene = 0

        element.appendToPrev = self._get_meta_value('append', None) == '1'

        # Date/Day and Time.
        element.date = verified_date(self._get_meta_value('Date'))
        if not element.date:
            element.day = verified_int_string(self._get_meta_value('Day'))

        element.time = verified_time(self._get_meta_value('Time'))

        # Duration.
        element.lastsDays = verified_int_string(self._get_meta_value('LastsDays'))
        element.lastsHours = verified_int_string(self._get_meta_value('LastsHours'))
        element.lastsMinutes = verified_int_string(self._get_meta_value('LastsMinutes'))

        # Characters references.
        scCharacters = self._get_meta_value('Characters')
        element.characters = string_to_list(scCharacters)

        # Locations references.
        scLocations = self._get_meta_value('Locations')
        element.locations = string_to_list(scLocations)

        # Items references.
        scItems = self._get_meta_value('Items')
        element.items = string_to_list(scItems)

    def export_data(self, element, yaml):
        yaml = super().export_data(element, yaml)
        if element.scType:
            yaml.append(f'type: {element.scType}')
        if element.status > 1:
            yaml.append(f'status: {element.status}')
        if element.scene > 0:
            yaml.append(f'scene: {element.scene}')
        if element.appendToPrev:
            yaml.append(f'append: 1')

        # Date/Day and Time.
        if element.date:
            yaml.append(f'Date: {element.date}')
        elif element.day:
            yaml.append(f'Day: {element.day}')
        if element.time:
            yaml.append(f'Time: {element.time}')

        # Duration.
        if element.lastsDays and element.lastsDays != '0':
            yaml.append(f'LastsDays: {element.lastsDays}')
        if element.lastsHours and element.lastsHours != '0':
            yaml.append(f'LastsHours: {element.lastsHours}')
        if element.lastsMinutes and element.lastsMinutes != '0':
            yaml.append(f'LastsMinutes: {element.lastsMinutes}')

        # Characters references.
        if element.characters:
            yaml.append(f'Characters: {list_to_string(element.characters)}')

        # Locations references.
        if element.locations:
            yaml.append(f'Locations: {list_to_string(element.locations)}')

        # Items references.
        if element.items:
            yaml.append(f'Items: {list_to_string(element.items)}')

        return yaml
