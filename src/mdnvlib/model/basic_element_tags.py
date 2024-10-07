"""Provide a class for a mdnovel element with notes and tags.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnvlib
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.model.basic_element_notes import BasicElementNotes
from mdnvlib.novx_globals import list_to_string
from mdnvlib.novx_globals import string_to_list


class BasicElementTags(BasicElementNotes):
    """Basic element with notes and tags."""

    def __init__(self,
            tags=None,
            **kwargs):
        """Extends the superclass constructor"""
        super().__init__(**kwargs)
        self._tags = tags

    @property
    def tags(self):
        # str: semicolon-separated tags
        return self._tags

    @tags.setter
    def tags(self, newVal):
        if newVal is not None:
            for elem in newVal:
                if elem is not None:
                    assert type(elem) == str
        if self._tags != newVal:
            self._tags = newVal
            self.on_element_change()

    def from_yaml(self, yaml):
        super().from_yaml(yaml)
        tags = string_to_list(self._get_meta_value('Tags'))
        strippedTags = []
        for tag in tags:
            strippedTags.append(tag.strip())
        self.tags = strippedTags

    def to_yaml(self, yaml):
        yaml = super().to_yaml(yaml)
        if self.tags:
            yaml.append(f'Tags: {list_to_string(self.tags)}')
        return yaml

