"""Provide a class for a mdnovel element with notes and tags.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
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
        # list of str
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

