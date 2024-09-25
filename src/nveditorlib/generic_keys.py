"""Provide a class with key definitions.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_editor
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nveditorlib.nveditor_globals import _


class GenericKeys:

    APPLY_CHANGES = ('<Control-s>', f'{_("Ctrl")}-S')
    BOLD = ('<Control-b>', f'{_("Ctrl")}-B')
    COPY = ('<Control-c>', f'{_("Ctrl")}-C')
    CREATE_SCENE = ('<Control-Alt-n>', f'{_("Ctrl")}-Alt-N')
    CUT = ('<Control-x>', f'{_("Ctrl")}-X')
    PASTE = ('<Control-v>', f'{_("Ctrl")}-V')
    ITALIC = ('<Control-i>', f'{_("Ctrl")}-I')
    OPEN_HELP = ('<F1>', 'F1')
    PLAIN = ('<Control-m>', f'{_("Ctrl")}-M')
    QUIT_PROGRAM = ('<Control-q>', f'{_("Ctrl")}-Q')
    SPLIT_SCENE = ('<Control-Alt-s>', f'{_("Ctrl")}-Alt-S')
    UPDATE_WORDCOUNT = ('<F5>', 'F5')
