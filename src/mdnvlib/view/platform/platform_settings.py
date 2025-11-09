"""Provide platform specific settings for the mdnovel application.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import platform

from mdnvlib.view.platform.generic_keys import GenericKeys
from mdnvlib.view.platform.generic_mouse import GenericMouse
from mdnvlib.view.platform.mac_keys import MacKeys
from mdnvlib.view.platform.mac_mouse import MacMouse
from mdnvlib.view.platform.windows_keys import WindowsKeys
from mdnvlib.view.platform.windows_mouse import WindowsMouse

if platform.system() == 'Windows':
    PLATFORM = 'win'
    KEYS = WindowsKeys()
    MOUSE = WindowsMouse()
elif platform.system() in ('Linux', 'FreeBSD'):
    PLATFORM = 'ix'
    KEYS = GenericKeys()
    MOUSE = GenericMouse()
elif platform.system() == 'Darwin':
    PLATFORM = 'mac'
    KEYS = MacKeys()
    MOUSE = MacMouse()
else:
    PLATFORM = ''
    KEYS = GenericKeys()
    MOUSE = GenericMouse()

