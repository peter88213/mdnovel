"""Provide a facade class for a command line user interface.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.novx_globals import _
from mdnvlib.converter.ui import Ui


class UiCmd(Ui):
    """Ui subclass implementing a console interface.
    
    Public methods:
        ask_yes_no(text) -- query yes or no at the console.
        set_info(message) -- show how the converter is doing.
        set_info_what(message) -- show what the converter is going to do.
        show_warning(message) -- Display a warning message.
    """

    def __init__(self, title):
        """Print the title.
        
        Positional arguments:
            title -- application title to be displayed at the console.
        
        Extends the superclass constructor.
        """
        super().__init__(title)
        print(title)

    def ask_yes_no(self, text):
        """Query yes or no at the console.
        
        Positional arguments:
            text -- question to be asked at the console. 
            
        Overrides the superclass method.       
        """
        result = input(f'{_("WARNING")}: {text} (y/n)')
        if result.lower() == 'y':
            return True
        else:
            return False

    def set_info(self, message):
        """Show how the converter is doing.

        Positional arguments:
            message -- message to be printed at the console. 
            
        Print the message, replacing the error marker, if any.
        Overrides the superclass method.
        """
        if message.startswith('!'):
            message = f'FAIL: {message.split("!", maxsplit=1)[1].strip()}'
        self.infoHowText = message
        print(message)

    def set_info_what(self, message):
        """Show what the converter is going to do.
        
        Positional arguments:
            message -- message to be printed at the console. 
            
        Print the message.
        Overrides the superclass method.
        """
        print(message)

    def show_warning(self, message):
        """Display a warning message."""
        print(f'\nWARNING: {message}\n')
