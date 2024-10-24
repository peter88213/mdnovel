"""A 'Theme Changer' for mdnovel.

Adds a 'Theme Changer' entry to the 'Tools' menu to open a window
with a combobox that lists all available themes. 
The selected theme will be persistently applied.  

To have a wider choice, you may want to install the ttkthemes package:

pip install ttkthemes

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from mdnvlib.novx_globals import _
from mdnvlib.plugin.themes.settings_window import SettingsWindow

try:
    from ttkthemes import ThemedStyle
    extraThemes = True
except ModuleNotFoundError:
    extraThemes = False


class ThemeManager:
    """A 'Theme Changer' class."""

    def __init__(self, view, controller):
        """Add a submenu to the 'Tools' menu.
        
        Positional arguments:
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.

        """
        prefs = controller.get_preferences()
        __, x, y = view.root.geometry().split('+')
        offset = 300
        windowGeometry = f'+{int(x)+offset}+{int(y)+offset}'
        if extraThemes:
            view.guiStyle = ThemedStyle(view.root)
        if not prefs.get('gui_theme', ''):
            prefs['gui_theme'] = view.guiStyle.theme_use()

        if not prefs['gui_theme'] in view.guiStyle.theme_names():
            prefs['gui_theme'] = view.guiStyle.theme_use()
        if extraThemes:
            view.guiStyle.set_theme(prefs['gui_theme'])
        else:
            view.guiStyle.theme_use(prefs['gui_theme'])

        # Create a submenu
        view.viewMenu.insert_command(
            _('Options'),
            label=_('Change theme'),
            command=lambda: SettingsWindow(view, prefs, extraThemes, windowGeometry)
            )
        view.viewMenu.insert_separator(_('Options'))

