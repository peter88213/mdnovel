"""Provide a class with key definitions for the Mac OS.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_editor
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nveditorlib.generic_keys import GenericKeys


class MacKeys(GenericKeys):

    APPLY_CHANGES = ('<Command-s>', 'Cmd-S')
    BOLD = ('<Command-b>', 'Cmd-B')
    CREATE_SCENE = ('<Command-Alt-n>', 'Cmd-Alt-N')
    ITALIC = ('<Command-i>', 'Cmd-I')
    PLAIN = ('<Command-m>', 'Cmd-M')
    QUIT_PROGRAM = ('<Command-q>', 'Cmd-Q')
    SPLIT_SCENE = ('<Command-Alt-s>', 'Cmd-Alt-S')
