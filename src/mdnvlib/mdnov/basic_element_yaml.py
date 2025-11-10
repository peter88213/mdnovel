"""Provide a base class for mdnovel element YAML import and export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class BasicElementYaml:

    def import_data(self, element, yaml):
        self._metaDict = {}
        for entry in yaml:
            try:
                metaData = entry.split(':', maxsplit=1)
                metaKey = metaData[0].strip()
                metaValue = metaData[1].strip()
                self._metaDict[metaKey] = metaValue
            except:
                pass

        element.title = self._get_meta_value('Title')

    def export_data(self, element, yaml):
        if element.title:
            yaml.append(f'Title: {element.title}')
        return yaml

    def _get_meta_value(self, key, default=None):
        text = self._metaDict.get(key, None)
        if text is not None:
            return text
        else:
            return default

