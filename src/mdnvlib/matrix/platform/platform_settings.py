"""Provide platform specific key definitions for the mdnovel plugin.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.matrix.platform.generic_keys import GenericKeys
from mdnvlib.matrix.platform.generic_mouse import GenericMouse
from mdnvlib.matrix.platform.mac_keys import MacKeys
from mdnvlib.matrix.platform.mac_mouse import MacMouse
from mdnvlib.matrix.platform.windows_keys import WindowsKeys

import platform

if platform.system() == 'Windows':
    PLATFORM = 'win'
    KEYS = WindowsKeys()
    MOUSE = GenericMouse
elif platform.system() in ('Linux', 'FreeBSD'):
    PLATFORM = 'ix'
    KEYS = GenericKeys()
    MOUSE = GenericMouse
elif platform.system() == 'Darwin':
    PLATFORM = 'mac'
    KEYS = MacKeys()
    MOUSE = MacMouse
else:
    PLATFORM = ''
    KEYS = GenericKeys()
    MOUSE = GenericMouse

