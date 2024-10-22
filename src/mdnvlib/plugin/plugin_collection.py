"""Provide a plugin collection class.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.plugin.editor.edit_manager import EditManager
from mdnvlib.plugin.matrix.matrix_view_manager import MatrixViewManager
from mdnvlib.plugin.progress.progress_view_manager import ProgressViewManager
from mdnvlib.plugin.templates.template_manager import TemplateManager
from mdnvlib.plugin.timeline.timeline_manager import TimelineManager


class PluginCollection(list):

    PLUGINS = [
        EditManager,
        TemplateManager,
        TimelineManager,
        MatrixViewManager,
        ProgressViewManager,
    ]

    def __init__(self, model, view, controller):
        super().__init__()
        for plugin in self.PLUGINS:
            self.append(plugin(model, view, controller))

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        for plugin in self:
            try:
                plugin.disable_menu()
            except:
                pass

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        for plugin in self:
            try:
                plugin.enable_menu()
            except:
                pass

    def on_quit(self):
        """Perform actions before the application is closed."""
        for plugin in self:
            try:
                plugin.on_quit()
            except:
                pass

    def on_close(self):
        """Perform actions before a project is closed."""
        for plugin in self:
            try:
                plugin.on_close()
            except:
                pass

