"""A daily progress log viewer for m.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from pathlib import Path

from mdnvlib.novx_globals import _
from mdnvlib.view.icons.set_icon_tk import set_icon
from mdnvlib.progress.progress_viewer import ProgressViewer

APPLICATION = _('Daily progress log')

WC_SETTINGS = dict(
    wc_win_geomety='510x440',
    wc_date_width=100,
    wc_wordcount_width=100,
    wc_wordcount_delta_width=100,
    wc_totalcount_width=100,
    wc_totalcount_delta_width=100,
)
WC_OPTIONS = {}


class WordcountLogView:
    """novelibre daily progress log viewer plugin class."""

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(APPLICATION, state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(APPLICATION, state='normal')

    def __init__(self, model, view, controller, prefs=None):
        """Add a submenu to the 'Tools' menu.
        
        Positional arguments:
            model -- reference to the main model instance of the application.
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.

        Optional arguments:
            prefs -- deprecated. Please use controller.get_preferences() instead.
        
        Overrides the superclass method.
        """
        self._mdl = model
        self._ui = view
        self._progress_viewer = None

        #--- Load configuration.
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            configDir = f'{homeDir}/.mdnovel/config'
        except:
            configDir = '.'
        self.iniFile = f'{configDir}/progress.ini'
        self.configuration = self._mdl.nvService.make_configuration(
            settings=WC_SETTINGS,
            options=WC_OPTIONS
            )
        self.configuration.read(self.iniFile)
        self.kwargs = {}
        self.kwargs.update(self.configuration.settings)
        self.kwargs.update(self.configuration.options)

        # Create an entry in the Tools menu.
        self._ui.toolsMenu.add_command(label=APPLICATION, command=self._start_viewer)
        self._ui.toolsMenu.entryconfig(APPLICATION, state='disabled')

    def on_close(self):
        """Close the window.
        
        Overrides the superclass method.
        """
        self.on_quit()

    def on_quit(self):
        """Write back the configuration file.
        
        Overrides the superclass method.
        """
        if self._progress_viewer:
            if self._progress_viewer.isOpen:
                self._progress_viewer.on_quit()

        #--- Save configuration
        for keyword in self.kwargs:
            if keyword in self.configuration.options:
                self.configuration.options[keyword] = self.kwargs[keyword]
            elif keyword in self.configuration.settings:
                self.configuration.settings[keyword] = self.kwargs[keyword]
        self.configuration.write(self.iniFile)

    def _start_viewer(self):
        if self._progress_viewer:
            if self._progress_viewer.isOpen:
                if self._progress_viewer.state() == 'iconic':
                    self._progress_viewer.state('normal')
                self._progress_viewer.lift()
                self._progress_viewer.focus()
                self._progress_viewer.build_tree()
                return

        self._progress_viewer = ProgressViewer(self, self._mdl)
        self._progress_viewer.title(f'{self._mdl.novel.title} - {APPLICATION}')
        set_icon(self._progress_viewer, icon='wLogo32', default=False)

