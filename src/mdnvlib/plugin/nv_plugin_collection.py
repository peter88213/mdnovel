"""Provide a plugin collection class.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from apptk.plugin.plugin_collection import PluginCollection
from mdnvlib.plugin.editor.editor import Editor
from mdnvlib.plugin.matrix.matrix import Matrix
from mdnvlib.plugin.progress.progress import Progress
from mdnvlib.plugin.templates.templates import Templates
from mdnvlib.plugin.themes.themes import Themes
from mdnvlib.plugin.timeline.timeline import Timeline


class NvPluginCollection(PluginCollection):

    PLUGINS = [
        Editor,
        Templates,
        Timeline,
        Matrix,
        Progress,
        Themes,
    ]

