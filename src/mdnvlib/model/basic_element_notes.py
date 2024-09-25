"""Provide a class for a mdnovel element with notes.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnvlib
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from mdnvlib.model.basic_element import BasicElement


class BasicElementNotes(BasicElement):
    """Basic element with notes."""

    def __init__(self,
            notes=None,
            **kwargs):
        """Extends the superclass constructor."""
        super().__init__(**kwargs)
        self._notes = notes

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._notes != newVal:
            self._notes = newVal
            self.on_element_change()

    def from_xml(self, xmlElement):
        super().from_xml(xmlElement)
        self.notes = self._xml_element_to_text(xmlElement.find('Notes'))

    def to_xml(self, xmlElement):
        super().to_xml(xmlElement)
        if self.notes:
            xmlElement.append(self._text_to_xml_element('Notes', self.notes))

