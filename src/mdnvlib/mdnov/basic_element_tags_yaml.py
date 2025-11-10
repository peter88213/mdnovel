"""Provide a class for mdnovel element YAML import and export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.mdnov.basic_element_notes_yaml import BasicElementNotesYaml
from mdnvlib.novx_globals import list_to_string
from mdnvlib.novx_globals import string_to_list


class BasicElementTagsYaml(BasicElementNotesYaml):

    def import_data(self, element, yaml):
        super().import_data(element, yaml)
        tags = string_to_list(self._get_meta_value('Tags'))
        strippedTags = []
        for tag in tags:
            strippedTags.append(tag.strip())
        element.tags = strippedTags

    def export_data(self, element, yaml):
        yaml = super().export_data(element, yaml)
        if element.tags:
            yaml.append(f'Tags: {list_to_string(element.tags)}')
        return yaml

