"""Toolbar class for mdnovel.


Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from mdnvlib.novx_globals import CH_ROOT
from mdnvlib.novx_globals import CR_ROOT
from mdnvlib.novx_globals import IT_ROOT
from mdnvlib.novx_globals import LC_ROOT
from mdnvlib.novx_globals import PL_ROOT
from mdnvlib.novx_globals import PN_ROOT
from mdnvlib.novx_globals import _
from mdnvlib.nv_globals import prefs
from mdnvlib.view.platform.platform_settings import KEYS
from apptk.widgets.tooltip import Hovertip
import tkinter as tk
from apptk.view.view_component_base import ViewComponentBase


class Toolbar(ViewComponentBase, ttk.Frame):
    """Toolbar class."""

    def __init__(self, parent, model, view, controller):
        """Add a toolbar.
        
        Positional arguments:
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.
        """
        ViewComponentBase.__init__(self, model, view, controller)
        ttk.Frame.__init__(self, parent)

        # Add a toolbar to the editor window.
        self.buttonBar = tk.Frame(self._ui.mainWindow)

        # "Go back" button.
        self._goBackButton = ttk.Button(
            self.buttonBar,
            text=_('Back'),
            image=self._ui.icons.goBackIcon,
            command=self._ui.tv.go_back
            )
        self._goBackButton.pack(side='left')
        self._goBackButton.image = self._ui.icons.goBackIcon

        # "Go forward" button.
        self._goForwardButton = ttk.Button(
            self.buttonBar,
            text=_('Forward'),
            image=self._ui.icons.goForwardIcon,
            command=self._ui.tv.go_forward
            )
        self._goForwardButton.pack(side='left')
        self._goForwardButton.image = self._ui.icons.goForwardIcon

        # Separator.
        tk.Frame(self.buttonBar, bg='light gray', width=1).pack(side='left', fill='y', padx=4)

        # "View Book" button.
        self._viewBookButton = ttk.Button(
            self.buttonBar,
            text=_('Book'),
            image=self._ui.icons.viewBookIcon,
            command=self._ui.tv.show_book
        )
        self._viewBookButton.pack(side='left')
        self._viewBookButton.image = self._ui.icons.viewBookIcon

        # "View Characters" button.
        self._viewCharactersButton = ttk.Button(
            self.buttonBar,
            text=_('Characters'),
            image=self._ui.icons.viewCharactersIcon,
            command=self._ui.tv.show_characters
        )
        self._viewCharactersButton.pack(side='left')
        self._viewCharactersButton.image = self._ui.icons.viewCharactersIcon

        # "View Locations" button.
        self._viewLocationsButton = ttk.Button(
            self.buttonBar,
            text=_('Locations'),
            image=self._ui.icons.viewLocationsIcon,
            command=self._ui.tv.show_locations
        )
        self._viewLocationsButton.pack(side='left')
        self._viewLocationsButton.image = self._ui.icons.viewLocationsIcon

        # "View Items" button.
        self._viewItemsButton = ttk.Button(
            self.buttonBar,
            text=_('Items'),
            image=self._ui.icons.viewItemsIcon,
            command=self._ui.tv.show_items
        )
        self._viewItemsButton.pack(side='left')
        self._viewItemsButton.image = self._ui.icons.viewItemsIcon

        # "View Plot lines" button.
        self._viewPlotLinesButton = ttk.Button(
            self.buttonBar,
            text=_('Plot lines'),
            image=self._ui.icons.viewPlotLinesIcon,
            command=self._ui.tv.show_plot_lines
        )
        self._viewPlotLinesButton.pack(side='left')
        self._viewPlotLinesButton.image = self._ui.icons.viewPlotLinesIcon

        # "View Projectnotes" button.
        self._viewProjectnotesButton = ttk.Button(
            self.buttonBar,
            text=_('Project notes'),
            image=self._ui.icons.viewProjectnotesIcon,
            command=self._ui.tv.show_project_notes
        )
        self._viewProjectnotesButton.pack(side='left')
        self._viewProjectnotesButton.image = self._ui.icons.viewProjectnotesIcon

        # Separator.
        tk.Frame(self.buttonBar, bg='light gray', width=1).pack(side='left', fill='y', padx=4)

        # "Save" button.
        self._saveButton = ttk.Button(
            self.buttonBar,
            text=_('Save'),
            image=self._ui.icons.saveIcon,
            command=self._ctrl.save_project
            )
        self._saveButton.pack(side='left')
        self._saveButton.image = self._ui.icons.saveIcon

        # Separator.
        tk.Frame(self.buttonBar, bg='light gray', width=1).pack(side='left', fill='y', padx=4)

        # "Add" button.
        self._addElementButton = ttk.Button(
            self.buttonBar,
            text=_('Add'),
            image=self._ui.icons.addIcon,
            command=self._ctrl.add_element
            )
        self._addElementButton.pack(side='left')
        self._addElementButton.image = self._ui.icons.addIcon

        # "Add Child" button.
        self._addChildButton = ttk.Button(
            self.buttonBar,
            text=_('Add child'),
            image=self._ui.icons.addChildIcon,
            command=self._ctrl.add_child
            )
        self._addChildButton.pack(side='left')
        self._addChildButton.image = self._ui.icons.addChildIcon

        # "Add Parent" button.
        self._addParentButton = ttk.Button(
            self.buttonBar,
            text=_('Add parent'),
            image=self._ui.icons.addParentIcon,
            command=self._ctrl.add_parent
            )
        self._addParentButton.pack(side='left')
        self._addParentButton.image = self._ui.icons.addParentIcon

        # "Delete" button.
        self._deleteElementButton = ttk.Button(
            self.buttonBar,
            text=_('Delete'),
            image=self._ui.icons.removeIcon,
            command=self._ctrl.delete_elements
            )
        self._deleteElementButton.pack(side='left')
        self._deleteElementButton.image = self._ui.icons.removeIcon

        # Reverse order (side='right').

        # "Toggle properties" button.
        self._propertiesButton = ttk.Button(
            self.buttonBar,
            text=_('Toggle Properties'),
            image=self._ui.icons.propertiesIcon,
            command=self._ui.toggle_properties_view
            )
        self._propertiesButton.pack(side='right')
        self._propertiesButton.image = self._ui.icons.propertiesIcon

        # "Toggle content viewer" button.
        self._viewerButton = ttk.Button(
            self.buttonBar,
            text=_('Toggle Text viewer'),
            image=self._ui.icons.viewerIcon,
            command=self._ui.toggle_contents_view
            )
        self._viewerButton.pack(side='right')
        self._viewerButton.image = self._ui.icons.viewerIcon

        self.buttonBar.pack(expand=False, before=self._ui.appWindow, fill='both')
        self._set_hovertips()

    def disable_menu(self):
        """Disable toolbar buttons when no project is open."""
        self._addChildButton.config(state='disabled')
        self._addElementButton.config(state='disabled')
        self._addParentButton.config(state='disabled')
        self._goBackButton.config(state='disabled')
        self._goForwardButton.config(state='disabled')
        self._deleteElementButton.config(state='disabled')
        self._saveButton.config(state='disabled')
        self._viewBookButton.config(state='disabled')
        self._viewCharactersButton.config(state='disabled')
        self._viewItemsButton.config(state='disabled')
        self._viewLocationsButton.config(state='disabled')
        self._viewPlotLinesButton.config(state='disabled')
        self._viewProjectnotesButton.config(state='disabled')

    def enable_menu(self):
        """Enable toolbar buttons when a project is open."""
        self._addChildButton.config(state='normal')
        self._addElementButton.config(state='normal')
        self._addParentButton.config(state='normal')
        self._goBackButton.config(state='normal')
        self._goForwardButton.config(state='normal')
        self._deleteElementButton.config(state='normal')
        self._saveButton.config(state='normal')
        self._viewBookButton.config(state='normal')
        self._viewCharactersButton.config(state='normal')
        self._viewItemsButton.config(state='normal')
        self._viewLocationsButton.config(state='normal')
        self._viewPlotLinesButton.config(state='normal')
        self._viewProjectnotesButton.config(state='normal')

    def _set_hovertips(self):
        if not prefs['enable_hovertips']:
            return

        Hovertip(self._addChildButton, f"{self._addChildButton['text']} ({KEYS.ADD_CHILD[1]})")
        Hovertip(self._addElementButton, f"{self._addElementButton['text']} ({KEYS.ADD_ELEMENT[1]})")
        Hovertip(self._addParentButton, f"{self._addParentButton['text']} ({KEYS.ADD_PARENT[1]})")
        Hovertip(self._goBackButton, self._goBackButton['text'])
        Hovertip(self._goForwardButton, self._goForwardButton['text'])
        Hovertip(self._propertiesButton, f"{self._propertiesButton['text']} ({KEYS.TOGGLE_PROPERTIES[1]})")
        Hovertip(self._saveButton, f"{self._saveButton['text']} ({KEYS.SAVE_PROJECT[1]})")
        Hovertip(self._deleteElementButton, f"{self._deleteElementButton['text']} ({KEYS.DELETE[1]})")
        Hovertip(self._viewBookButton, self._viewBookButton['text'])
        Hovertip(self._viewCharactersButton, self._viewCharactersButton['text'])
        Hovertip(self._viewItemsButton, self._viewItemsButton['text'])
        Hovertip(self._viewLocationsButton, self._viewLocationsButton['text'])
        Hovertip(self._viewPlotLinesButton, self._viewPlotLinesButton['text'])
        Hovertip(self._viewProjectnotesButton, self._viewProjectnotesButton['text'])
        Hovertip(self._viewerButton, f"{self._viewerButton['text']} ({KEYS.TOGGLE_VIEWER[1]})")

