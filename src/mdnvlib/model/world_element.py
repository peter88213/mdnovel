"""Provide a generic class for mdnovel story world element representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.model.basic_element_tags import BasicElementTags


class WorldElement(BasicElementTags):
    """Story world element representation (may be location or item)."""

    def __init__(self,
            aka=None,
            **kwargs):
        """Extends the superclass constructor"""
        super().__init__(**kwargs)
        self._aka = aka

    @property
    def aka(self):
        return self._aka

    @aka.setter
    def aka(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._aka != newVal:
            self._aka = newVal
            self.on_element_change()

