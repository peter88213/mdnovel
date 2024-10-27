"""Provide an "index card" class.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/apptk
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from apptk.widgets.text_box import TextBox
from apptk.widgets.my_string_var import MyStringVar


class IndexCard(tk.Frame):
    """An "index card" class displaying a title and a text body.
    
    Public instance variables:
        title: tk.StringVar -- Editable title text.
        bodyBox: TextBox -- Body text editor.   
    """

    def __init__(self, master=None, cnf={}, fg='black', bg='white', font=None, scrollbar=True, **kw):
        super().__init__(master=master, cnf=cnf, **kw)
        # Title label.
        self.title = MyStringVar(value='')
        self.titleEntry = tk.Entry(
            self,
            bg=bg,
            bd=0,
            textvariable=self.title,
            relief='flat',
            font=font,
            )
        self.titleEntry.config({
            'background': bg,
            'foreground': fg,
            'insertbackground': fg,
            })
        self.titleEntry.pack(fill='x', ipady=6)

        tk.Frame(self, bg='red', height=1, bd=0).pack(fill='x')
        tk.Frame(self, bg=bg, height=1, bd=0).pack(fill='x')

        # Description window.
        self.bodyBox = TextBox(
            self,
            scrollbar=scrollbar,
            wrap='word',
            undo=True,
            autoseparators=True,
            maxundo=-1,
            padx=5,
            pady=5,
            bg=bg,
            fg=fg,
            insertbackground=fg,
            font=font,
            )
        self.bodyBox.pack(fill='both', expand=True)

