"""Provide a class for mdnovel element YAML import an export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.mdnov.basic_element_notes_yaml import BasicElementNotesYaml


class PlotPointYaml(BasicElementNotesYaml):

    def import_data(self, element, yaml):
        super().import_data(element, yaml)
        element.sectionAssoc = self._get_meta_value('Section')

    def export_data(self, element, yaml):
        yaml = super().export_data(element, yaml)
        if element.sectionAssoc:
            yaml.append(f'Section: {element.sectionAssoc}')
        return yaml
