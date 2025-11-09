"""Provide a class for mdnovel element YAML import an export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.mdnov.basic_element_notes_yaml import BasicElementNotesYaml


class ChapterYaml(BasicElementNotesYaml):

    def import_data(self, element, yaml):
        super().import_data(element, yaml)
        typeStr = self._get_meta_value('type', '0')
        if typeStr in ('0', '1'):
            element.chType = int(typeStr)
        else:
            element.chType = 1
        chLevel = self._get_meta_value('level', None)
        if chLevel == '1':
            element.chLevel = 1
        else:
            element.chLevel = 2
        element.isTrash = self._get_meta_value('isTrash', None) == '1'
        element.noNumber = self._get_meta_value('noNumber', None) == '1'

    def export_data(self, element, yaml):
        yaml = super().export_data(element, yaml)
        if element.chType:
            yaml.append(f'type: {element.chType}')
        if element.chLevel == 1:
            yaml.append(f'level: 1')
        if element.isTrash:
            yaml.append(f'isTrash: 1')
        if element.noNumber:
            yaml.append(f'noNumber: 1')
        return yaml
