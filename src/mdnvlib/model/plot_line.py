"""Provide a class for mdnovel plot line representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.model.basic_element_notes import BasicElementNotes
from mdnvlib.novx_globals import string_to_list
from mdnvlib.novx_globals import list_to_string


class PlotLine(BasicElementNotes):
    """Plot line representation."""

    def __init__(self,
            shortName=None,
            sections=None,
            **kwargs):
        """Extends the superclass constructor."""
        super().__init__(**kwargs)

        self._shortName = shortName
        self._sections = sections

    @property
    def shortName(self):
        # str: name of the plot line
        return self._shortName

    @shortName.setter
    def shortName(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._shortName != newVal:
            self._shortName = newVal
            self.on_element_change()

    @property
    def sections(self):
        # List of str: IDs of the sections associated with the plot line.
        try:
            return self._sections[:]
        except TypeError:
            return None

    @sections.setter
    def sections(self, newVal):
        if newVal is not None:
            for elem in newVal:
                if elem is not None:
                    assert type(elem) == str
        if self._sections != newVal:
            self._sections = newVal
            self.on_element_change()

