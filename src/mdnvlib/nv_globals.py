"""Provide global variables and functions.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date
import webbrowser

from mdnvlib.novx_globals import _

prefs = {}

HELP_URL = 'https://github.com/peter88213/mdnovel/docs/help/'
HOME_URL = 'https://github.com/peter88213/mdnovel/'
SC_EDITOR = _('Section Editor')
SC_EDITOR_ICON = 'eLogo32'


def to_string(text):
    """Return text, converted to a string."""
    if text is None:
        return ''

    return str(text)


def open_help(page):
    """Show the online help page specified by page."""
    webbrowser.open(f'{HELP_URL}{page}')


def datestr(isoDate):
    """Return a localized date string, if the localize_date option is set.
    
    Otherwise return the input unchanged.
    """
    if prefs['localize_date']:
        return date.fromisoformat(isoDate).strftime("%x")
    else:
        return isoDate


def get_section_date_str(section):
    """Return a localized date string, if the localize_date option is set.
    
    Otherwise return the section's date in ISO format.
    """
    if prefs['localize_date']:
        return section.localeDate
    else:
        return section.date
