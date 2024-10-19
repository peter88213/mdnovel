"""Provide a class with key definitions.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.nv_globals import _


class GenericKeys:

    ADD_CHILD = ('<Control-Alt-n>', f'{_("Ctrl")}-Alt-N')
    ADD_ELEMENT = ('<Control-n>', f'{_("Ctrl")}-N')
    ADD_PARENT = ('<Control-Alt-N>', f'{_("Ctrl")}-Alt-{_("Shift")}-N')
    APPLY_CHANGES = ('<Control-s>', f'{_("Ctrl")}-S')
    BOLD = ('<Control-b>', f'{_("Ctrl")}-B')
    CHAPTER_LEVEL = ('<Control-Alt-c>', f'{_("Ctrl")}-Alt-C')
    COPY = ('<Control-c>', f'{_("Ctrl")}-C')
    CREATE_SCENE = ('<Control-Alt-n>', f'{_("Ctrl")}-Alt-N')
    CUT = ('<Control-x>', f'{_("Ctrl")}-X')
    DELETE = ('<Delete>', _('Del'))
    DETACH_PROPERTIES = ('<Control-Alt-d>', f'{_("Ctrl")}-Alt-D')
    END_FULLSCREEN = ('<Escape>', 'Esc')
    FOLDER = ('<Control-p>', f'{_("Ctrl")}-P')
    ITALIC = ('<Control-i>', f'{_("Ctrl")}-I')
    LOCK_PROJECT = ('<Control-l>', f'{_("Ctrl")}-L')
    OPEN_HELP = ('<F1>', 'F1')
    OPEN_PROJECT = ('<Control-o>', f'{_("Ctrl")}-O')
    PASTE = ('<Control-v>', f'{_("Ctrl")}-V')
    PLAIN = ('<Control-m>', f'{_("Ctrl")}-M')
    QUIT_PROGRAM = ('<Control-q>', f'{_("Ctrl")}-Q')
    REFRESH_TREE = ('<F5>', 'F5')
    RELOAD_PROJECT = ('<Control-r>', f'{_("Ctrl")}-R')
    RESTORE_BACKUP = ('<Control-b>', f'{_("Ctrl")}-B')
    RESTORE_STATUS = ('<Escape>', 'Esc')
    SAVE_AS = ('<Control-S>', f'{_("Ctrl")}-{_("Shift")}-S')
    SAVE_PROJECT = ('<Control-s>', f'{_("Ctrl")}-S')
    SPLIT_SCENE = ('<Control-Alt-s>', f'{_("Ctrl")}-Alt-S')
    TOGGLE_PROPERTIES = ('<Control-Alt-t>', f'{_("Ctrl")}-Alt-T')
    TOGGLE_VIEWER = ('<Control-t>', f'{_("Ctrl")}-T')
    TOGGLE_FULLSCREEN = ('<F11>', 'F11')
    UNLOCK_PROJECT = ('<Control-u>', f'{_("Ctrl")}-U')
    UPDATE_WORDCOUNT = ('<F5>', 'F5')
