"""Provide a class for mdnovel plot point representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnvlib
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.model.basic_element_notes import BasicElementNotes


class PlotPoint(BasicElementNotes):
    """Plot point representation."""

    def __init__(self,
            sectionAssoc=None,
            **kwargs):
        """Extends the superclass constructor."""
        super().__init__(**kwargs)

        self._sectionAssoc = sectionAssoc

    @property
    def sectionAssoc(self):
        # str: ID of the associated section
        return self._sectionAssoc

    @sectionAssoc.setter
    def sectionAssoc(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._sectionAssoc != newVal:
            self._sectionAssoc = newVal
            self.on_element_change()

    def from_xml(self, xmlElement):
        super().from_xml(xmlElement)
        xmlSectionAssoc = xmlElement.find('Section')
        if xmlSectionAssoc is not None:
            self.sectionAssoc = xmlSectionAssoc.get('id', None)

    def to_yaml(self, yaml):
        yaml = super().to_yaml(yaml)
        if self.sectionAssoc:
            yaml.append(f'Section: {self.sectionAssoc}')
        return yaml
