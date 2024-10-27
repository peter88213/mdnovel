"""Provide a view base class for a MVC framework.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/apptk
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from abc import ABC, abstractmethod
from tkinter import messagebox

import tkinter as tk


class ViewBase(ABC):

    @abstractmethod
    def __init__(self, model, controller, title):
        """Create a composite structure for view components."""
        self._mdl = model
        self._ctrl = controller
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self._ctrl.on_quit)
        self.root.title(title)
        self.title = title
        self._mdl.register_client(self)
        self._viewComponents = []

    def ask_yes_no(self, text, title=None):
        """Query yes or no with a pop-up box.
        
        Positional arguments:
            text -- question to be asked in the pop-up box. 
            
        Optional arguments:
            title -- title to be displayed on the window frame.            
        """
        if title is None:
            title = self.title
        return messagebox.askyesno(title, text)

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        for viewComponent in self._viewComponents:
            viewComponent.disable_menu()

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        for viewComponent in self._viewComponents:
            viewComponent.enable_menu()

    def on_quit(self):
        """Gracefully close the user interface."""
        self.root.quit()

    def refresh(self):
        """Update view components."""
        for viewComponent in self._viewComponents:
            viewComponent.refresh()

    def register_view(self, viewComponent):
        """Add a view object to the composite list."""
        if not viewComponent in self._viewComponents:
            self._viewComponents.append(viewComponent)

    def show_error(self, message, title=None):
        """Display an error message box.
        
        Optional arguments:
            title -- title to be displayed on the window frame.
        """
        if title is None:
            title = self.title
        messagebox.showerror(title, message)

    def show_info(self, message, title=None):
        """Display an informational message box.
        
        Optional arguments:
            title -- title to be displayed on the window frame.
        """
        if title is None:
            title = self.title
        messagebox.showinfo(title, message)

    def show_warning(self, message, title=None):
        """Display a warning message box.
        
        Optional arguments:
            title -- title to be displayed on the window frame.
        """
        if title is None:
            title = self.title
        messagebox.showwarning(title, message)

    def start(self):
        """Start the Tk main loop.
        
        Note: This can not be done in the constructor method.
        """
        self.root.mainloop()

    def unregister_view(self, viewComponent):
        """Revove a view object from the composite list."""
        if viewComponent in self._viewComponents:
            self._viewComponents.remove(viewComponent)

