"""Provide a class with getters and factory methods for novxlib objects.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.configuration.configuration import Configuration
from mdnvlib.model.moonphase import get_moon_phase_string
from mdnvlib.model.novel import Novel
from mdnvlib.model.mdnov_service import MdnovService
from mdnvlib.model.nv_treeview import NvTreeview


class NvService(MdnovService):
    """Getters and factory methods for mdnovel objects."""

    def get_moon_phase_str(self, isoDate):
        return get_moon_phase_string(isoDate)

    def make_configuration(self, **kwargs):
        return Configuration(**kwargs)

    def make_novel(self, **kwargs):
        """Overrides the superclass method."""
        kwargs['tree'] = kwargs.get('tree', NvTreeview())
        return Novel(**kwargs)

    def make_nv_tree(self, **kwargs):
        """Overrides the superclass method."""
        return NvTreeview(**kwargs)
