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
from apptk.plugin.plugin_base import PluginBase
from mdnvlib.plugin.themes.settings_window import SettingsWindow

try:
    from ttkthemes import ThemedStyle
    extraThemes = True
except ModuleNotFoundError:
    extraThemes = False


class Themes(PluginBase):
    """A 'Theme Changer' class."""

    def __init__(self, model, view, controller):
        """Add a submenu to the 'Tools' menu.
        
        Positional arguments:
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.

        """
        super().__init__(model, view, controller)
        prefs = self._ctrl.get_preferences()
        __, x, y = self._ui.root.geometry().split('+')
        offset = 300
        windowGeometry = f'+{int(x)+offset}+{int(y)+offset}'
        if extraThemes:
            self._ui.guiStyle = ThemedStyle(self._ui.root)
        if not prefs.get('gui_theme', ''):
            prefs['gui_theme'] = self._ui.guiStyle.theme_use()

        if not prefs['gui_theme'] in self._ui.guiStyle.theme_names():
            prefs['gui_theme'] = self._ui.guiStyle.theme_use()
        if extraThemes:
            self._ui.guiStyle.set_theme(prefs['gui_theme'])
        else:
            self._ui.guiStyle.theme_use(prefs['gui_theme'])

        # Create a submenu
        self._ui.viewMenu.insert_command(
            _('Options'),
            label=_('Change theme'),
            command=lambda: SettingsWindow(view, prefs, extraThemes, windowGeometry)
            )
        self._ui.viewMenu.insert_separator(_('Options'))

