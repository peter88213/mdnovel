"""Provide a class for mdnovel element YAML import and export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.mdnov.basic_element_tags_yaml import BasicElementTagsYaml


class WorldElementYaml(BasicElementTagsYaml):
    """Story world element representation (may be location or item)."""

    def import_data(self, element, yaml):
        super().import_data(element, yaml)
        element.aka = self._get_meta_value('Aka')

    def export_data(self, element, yaml):
        yaml = super().export_data(element, yaml)
        if element.aka:
            yaml.append(f'Aka: {element.aka}')
        return yaml

