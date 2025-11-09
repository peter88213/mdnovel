"""A daily progress log view manager class for mdnovel.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from pathlib import Path

from mdnvlib.novx_globals import _
from apptk.plugin.plugin_base import PluginBase
from mdnvlib.plugin.progress.progress_viewer import ProgressViewer
from mdnvlib.view.icons.set_icon_tk import set_icon


class Progress(PluginBase):
    """mdnovel daily progress log view manager class."""
    FEATURE = _('Daily progress log')
    SETTINGS = dict(
        window_geometry='510x440',
        date_width=100,
        wordcount_width=100,
        wordcount_delta_width=100,
        totalcount_width=100,
        totalcount_delta_width=100,
    )
    OPTIONS = {}

    def __init__(self, model, view, controller):
        """Add a submenu to the 'Tools' menu.
        
        Positional arguments:
            model -- reference to the main model instance of the application.
            view -- reference to the main view instance of the application.
        """
        super().__init__(model, view, controller)
        self._progress_viewer = None

        #--- Load configuration.
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            configDir = f'{homeDir}/.mdnovel/config'
        except:
            configDir = '.'
        self.iniFile = f'{configDir}/progress.ini'
        self.configuration = self._mdl.nvService.make_configuration(
            settings=self.SETTINGS,
            options=self.OPTIONS
            )
        self.configuration.read(self.iniFile)
        self.kwargs = {}
        self.kwargs.update(self.configuration.settings)
        self.kwargs.update(self.configuration.options)

        # Create an entry in the Tools menu.
        self._ui.toolsMenu.add_command(label=self.FEATURE, command=self._start_viewer)
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='disabled')

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='normal')

    def on_close(self):
        """Close the window."""
        self.on_quit()

    def on_quit(self):
        """Write back the configuration file."""
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

        self._progress_viewer = ProgressViewer(self._mdl, self._ui, self._ctrl, self)
        self._progress_viewer.title(f'{self._mdl.novel.title} - {self.FEATURE}')
        set_icon(self._progress_viewer, icon='wLogo32', default=False)

