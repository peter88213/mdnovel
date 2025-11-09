"""Provide a class for mdnovel element YAML import an export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.mdnov.basic_element_notes_yaml import BasicElementNotesYaml
from mdnvlib.novx_globals import string_to_list
from mdnvlib.novx_globals import list_to_string


class PlotLineYaml(BasicElementNotesYaml):

    def import_data(self, element, yaml):
        super().import_data(element, yaml)
        element.shortName = self._get_meta_value('ShortName')
        plSections = self._get_meta_value('Sections')
        element.sections = string_to_list(plSections)

    def export_data(self, element, yaml):
        yaml = super().export_data(element, yaml)
        if element.shortName:
            yaml.append(f'ShortName: {element.shortName}')
        if element.sections:
            yaml.append(f'Sections: {list_to_string(element.sections)}')
        return yaml
