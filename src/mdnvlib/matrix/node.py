"""Provide a class representing a visual matrix node.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.view.platform.platform_settings import MOUSE
import tkinter as tk


class Node(tk.Label):
    """A visual matrix node, representing a boolean value.
    
    Properties:
        state: Boolean -- Node state. Changes its value and view when clicked on.
    """
    marker = '⬛'

    def __init__(self, master, colorFalse='white', colorTrue='black', cnf={}, **kw):
        """Place the node to the master widget.
        
        Optional arguments:
            colorBg: str -- Background color.
            colorFg: str -- Marker color when status is True.
        """
        self.colorFg = colorTrue
        self.colorBg = colorFalse
        self._state = False
        super().__init__(master, cnf, **kw)
        self.config(background=self.colorBg)
        self.config(foreground=self.colorFg)
        self.bind(MOUSE.TOGGLE_STATE, self._toggle_state)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, newState):
        self._state = newState
        self._set_marker()

    def _set_marker(self):
        if self._state:
            self.config(text=self.marker)
        else:
            self.config(text='')

    def _toggle_state(self, event=None):
        self.state = not self._state
