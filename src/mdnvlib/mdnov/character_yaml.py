"""Provide a class for mdnovel element YAML import an export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.mdnov.world_element_yaml import WorldElementYaml
from mdnvlib.novx_globals import verified_date


class CharacterYaml(WorldElementYaml):

    def import_data(self, element, yaml):
        super().import_data(element, yaml)
        element.isMajor = self._get_meta_value('major', None) == '1'
        element.fullName = self._get_meta_value('FullName')
        element.birthDate = verified_date(self._get_meta_value('BirthDate'))
        element.deathDate = verified_date(self._get_meta_value('DeathDate'))

    def export_data(self, element, yaml):
        yaml = super().export_data(element, yaml)
        if element.isMajor:
            yaml.append(f'major: 1')
        if element.fullName:
            yaml.append(f'FullName: {element.fullName}')
        if element.birthDate:
            yaml.append(f'BirthDate: {element.birthDate}')
        if element.deathDate:
            yaml.append(f'DeathDate: {element.deathDate}')
        return yaml

