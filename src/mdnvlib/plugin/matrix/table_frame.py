"""Provide a tkinter frame for a scrollable table.

The frame is divided into four sections, each containing one "public" frame:

+-----------+--------------+
|  topLeft  | columnTitles |
+-----------+--------------+
| rowTitles |   display    |
+-----------+--------------+

- topLeft is not scrollable. 
- rowTitles and display are simultaneously vertically scrollable.
- columnTitles and display are simultaneously horizontally scrollable.

Mouse wheel

- Use the mouse wheel for vertical scrolling.
- Use the mouse wheel with the `Shift` key pressed for horizontal scrolling.    


Based on the VerticalScrolledFrame example class shown and discussed here:
https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame
https://stackoverflow.com/questions/4066974/scrolling-multiple-tkinter-listboxes-together

Mouse wheel binding as proposed here:
https://stackoverflow.com/questions/17355902/tkinter-binding-mousewheel-to-scrollbar
https://stackoverflow.com/questions/63629407/tkinter-how-to-stop-scrolling-above-canvas-window
https://stackoverflow.com/questions/51538818/python-tkinter-binding-child-widgets

Copyright (c) 2024 Peter Triesberger
https://github.com/peter88213/
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
import platform
from tkinter import ttk

import tkinter as tk


class TableFrame(ttk.Frame):
    """A tkinter framew for a scrollable table. 
    
    Public instance variables:
        rowTitles -- ttk.Frame for a vertically scrolled column of row titles. 
        columnTitles -- ttk.Frame for a horizontally scrolled row of column titles. 
        display -- ttk.Frame for columns and rows to be displayed and scrolled in both directions.        
    """

    def __init__(self, parent, *args, **kw):

        ttk.Frame.__init__(self, parent, *args, **kw)

        # Scrollbars.
        scrollY = ttk.Scrollbar(self, orient='vertical', command=self.yview)
        scrollY.pack(fill='y', side='right', expand=False)
        scrollX = ttk.Scrollbar(self, orient='horizontal', command=self.xview)
        scrollX.pack(fill='x', side='bottom', expand=False)

        # Left column frame.
        leftColFrame = ttk.Frame(self)
        leftColFrame.pack(side='left', fill='both', expand=False)

        # Fixed title column header.
        self.topLeft = ttk.Frame(leftColFrame)
        self.topLeft.pack(anchor='w', fill='x', expand=False)

        #--- Vertically scrollable row titles.
        rowTitlesFrame = ttk.Frame(leftColFrame)
        rowTitlesFrame.pack(fill='both', expand=True)
        self._rowTitlesCanvas = tk.Canvas(rowTitlesFrame, bd=0, highlightthickness=0)
        self._rowTitlesCanvas.configure(yscrollcommand=scrollY.set)
        self._rowTitlesCanvas.pack(side='left', fill='both', expand=True)
        self._rowTitlesCanvas.xview_moveto(0)
        self._rowTitlesCanvas.yview_moveto(0)

        # Create a frame inside the row titles canvas which will be scrolled with it.
        self.rowTitles = ttk.Frame(self._rowTitlesCanvas)
        self._rowTitlesCanvas.create_window(0, 0, window=self.rowTitles, anchor='nw', tags="self.rowTitles")

        def _configure_rowTitles(event):
            # Update the scrollbars to match the size of the display frame.
            size = (self.rowTitles.winfo_reqwidth(), self.rowTitles.winfo_reqheight())
            self._rowTitlesCanvas.config(scrollregion="0 0 %s %s" % size)

            # Update the display Canvas's width to fit the inner frame.
            if self.rowTitles.winfo_reqwidth() != self._rowTitlesCanvas.winfo_width():
                self._rowTitlesCanvas.config(width=self.rowTitles.winfo_reqwidth())

        self.rowTitles.bind('<Configure>', _configure_rowTitles)

        # Right column frame.
        rightColFrame = ttk.Frame(self)
        rightColFrame.pack(side='left', anchor='nw', fill='both', expand=True)

        #--- Horizontally scrollable column titles.
        columnTitlesFrame = ttk.Frame(rightColFrame)
        columnTitlesFrame.pack(fill='x', anchor='nw', expand=False)
        self._columnTitlesCanvas = tk.Canvas(columnTitlesFrame, bd=0, highlightthickness=0)
        self._columnTitlesCanvas.configure(xscrollcommand=scrollX.set)
        self._columnTitlesCanvas.pack(side='left', fill='both', expand=True)
        self._columnTitlesCanvas.xview_moveto(0)
        self._columnTitlesCanvas.yview_moveto(0)

        # Create a frame inside the column titles canvas which will be scrolled with it.
        self.columnTitles = ttk.Frame(self._columnTitlesCanvas)
        self._columnTitlesCanvas.create_window(0, 0, window=self.columnTitles, anchor='nw', tags="self.columnTitles")

        def _configure_columnTitles(event):
            # Update the scrollbars to match the size of the display frame.
            size = (self.columnTitles.winfo_reqwidth(), self.columnTitles.winfo_reqheight())
            self._columnTitlesCanvas.config(scrollregion="0 0 %s %s" % size)

            # Update the display Canvas's width and height to fit the inner frame.
            if self.columnTitles.winfo_reqwidth() != self._columnTitlesCanvas.winfo_width():
                self._columnTitlesCanvas.config(width=self.columnTitles.winfo_reqwidth())
            if self.columnTitles.winfo_reqheight() != self._columnTitlesCanvas.winfo_height():
                self._columnTitlesCanvas.config(height=self.columnTitles.winfo_reqheight())

        self.columnTitles.bind('<Configure>', _configure_columnTitles)

        #--- Vertically and horizontally scrollable display.
        displayFrame = ttk.Frame(rightColFrame)
        displayFrame.pack(fill='both', expand=True)
        self._displayCanvas = tk.Canvas(displayFrame, bd=0, highlightthickness=0)
        self._displayCanvas.configure(xscrollcommand=scrollX.set)
        self._displayCanvas.configure(yscrollcommand=scrollY.set)
        self._displayCanvas.pack(side='left', fill='both', expand=True)
        self._displayCanvas.xview_moveto(0)
        self._displayCanvas.yview_moveto(0)

        # Create a frame inside the display canvas which will be scrolled with it.
        self.display = ttk.Frame(self._displayCanvas)
        self._displayCanvas.create_window(0, 0, window=self.display, anchor='nw', tags="self.display")

        def _configure_display(event):
            # Update the scrollbars to match the size of the display frame.
            size = (self.display.winfo_reqwidth(), self.display.winfo_reqheight())
            self._displayCanvas.config(scrollregion="0 0 %s %s" % size)
            if self.display.winfo_reqwidth() != self._displayCanvas.winfo_width():
                # Update the display Canvas's width to fit the inner frame.
                self._displayCanvas.config(width=self.display.winfo_reqwidth())

        self.display.bind('<Configure>', _configure_display)
        self.bind('<Enter>', self._bind_mousewheel)
        self.bind('<Leave>', self._unbind_mousewheel)
        # this will prevent the frame from being scrolled along with the windows on the desktop

    def destroy(self):
        """Destructor for deleting event bindings."""
        self.display.unbind('<Configure>')
        self._unbind_mousewheel()
        super().destroy()

    def vertical_scroll(self, event):
        """Event handler for vertical scrolling."""
        if platform.system() == 'Windows':
            self.yview_scroll(int(-1 * (event.delta / 120)), 'units')
        elif platform.system() == 'Darwin':
            self.yview_scroll(int(-1 * event.delta), 'units')
        else:
            if event.num == 4:
                self.yview_scroll(-1, 'units')
            elif event.num == 5:
                self.yview_scroll(1, 'units')

    def horizontal_scroll(self, event):
        """Event handler for horizontal scrolling."""
        if platform.system() == 'Windows':
            self.xview_scroll(int(-1 * (event.delta / 120)), 'units')
        elif platform.system() == 'Darwin':
            self.xview_scroll(int(-1 * event.delta), 'units')
        else:
            if event.num == 4:
                self.xview_scroll(-1, 'units')
            elif event.num == 5:
                self.xview_scroll(1, 'units')

    def xview(self, *args):
        self._columnTitlesCanvas.xview(*args)
        self._displayCanvas.xview(*args)

    def xview_scroll(self, *args):
        if not self._displayCanvas.xview() == (0.0, 1.0):
            self._columnTitlesCanvas.xview_scroll(*args)
            self._displayCanvas.xview_scroll(*args)

    def yview(self, *args):
        self._rowTitlesCanvas.yview(*args)
        self._displayCanvas.yview(*args)

    def yview_scroll(self, *args):
        if not self._displayCanvas.yview() == (0.0, 1.0):
            self._rowTitlesCanvas.yview_scroll(*args)
            self._displayCanvas.yview_scroll(*args)

    def _bind_mousewheel(self, event=None):
        if platform.system() in ('Linux', 'FreeBSD'):
            # Vertical scrolling
            self._rowTitlesCanvas.bind_all('<Button-4>', self.vertical_scroll)
            self._rowTitlesCanvas.bind_all('<Button-5>', self.vertical_scroll)
            self._displayCanvas.bind_all('<Button-4>', self.vertical_scroll)
            self._displayCanvas.bind_all('<Button-5>', self.vertical_scroll)

            # Horizontal scrolling
            self._rowTitlesCanvas.bind_all('<Shift-Button-4>', self.horizontal_scroll)
            self._rowTitlesCanvas.bind_all('<Shift-Button-5>', self.horizontal_scroll)
            self._displayCanvas.bind_all('<Shift-Button-4>', self.horizontal_scroll)
            self._displayCanvas.bind_all('<Shift-Button-5>', self.horizontal_scroll)
        else:
            # Vertical scrolling
            self._rowTitlesCanvas.bind_all('<MouseWheel>', self.vertical_scroll)
            self._displayCanvas.bind_all('<MouseWheel>', self.vertical_scroll)

            # Horizontal scrolling
            self._rowTitlesCanvas.bind_all('<Shift-MouseWheel>', self.horizontal_scroll)
            self._displayCanvas.bind_all('<Shift-MouseWheel>', self.horizontal_scroll)

    def _unbind_mousewheel(self, event=None):
        if platform.system() in ('Linux', 'FreeBSD'):
            # Vertical scrolling
            self._rowTitlesCanvas.unbind_all('<Button-4>')
            self._rowTitlesCanvas.unbind_all('<Button-5>')
            self._displayCanvas.unbind_all('<Button-4>')
            self._displayCanvas.unbind_all('<Button-5>')

            # Horizontal scrolling
            self._rowTitlesCanvas.unbind_all('<Shift-Button-4>')
            self._rowTitlesCanvas.unbind_all('<Shift-Button-5>')
            self._displayCanvas.unbind_all('<Shift-Button-4>')
            self._displayCanvas.unbind_all('<Shift-Button-5>')
        else:
            # Vertical scrolling
            self._rowTitlesCanvas.unbind_all('<MouseWheel>')
            self._displayCanvas.unbind_all('<MouseWheel>')

            # Horizontal scrolling
            self._rowTitlesCanvas.unbind_all('<Shift-MouseWheel>')
            self._displayCanvas.unbind_all('<Shift-MouseWheel>')

