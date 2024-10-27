"""Sample application using the MVC framework.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/apptk
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from apptk.controller.controller_base import ControllerBase
from apptk.model.model_base import ModelBase
from apptk.plugin.plugin_collection import PluginCollection
from apptk.view.view_base import ViewBase


class MyModel(ModelBase):

    def __init__(self):
        super().__init__()


class MyView(ViewBase):

    def __init__(self, model, controller, title):
        super().__init__(model, controller, title)


class MyController(ControllerBase):

    def __init__(self, title):
        self._mdl = MyModel()
        self._mdl.register_client(self)
        self._ui = MyView(self._mdl, self, title)
        self.plugins = PluginCollection(self._mdl, self._ui, self)


app = MyController('Sample application')
ui = app.get_view()
ui.start()
