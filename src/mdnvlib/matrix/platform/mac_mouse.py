"""Provide a class with mouse opersion definitions for the Mac OS.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.matrix.platform.generic_mouse import GenericMouse


class MacMouse(GenericMouse):

    TOGGLE_STATE = '<Command-Button-1>'
