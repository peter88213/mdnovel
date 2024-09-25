"""Provide global variables and functions.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_editor
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import gettext
import locale
import os
import sys
import webbrowser

# Initialize localization.
LOCALE_PATH = f'{os.path.dirname(sys.argv[0])}/locale/'
try:
    CURRENT_LANGUAGE = locale.getlocale()[0][:2]
except:
    # Fallback for old Windows versions.
    CURRENT_LANGUAGE = locale.getdefaultlocale()[0][:2]
try:
    t = gettext.translation('nv_editor', LOCALE_PATH, languages=[CURRENT_LANGUAGE])
    _ = t.gettext
except:

    def _(message):
        return message

APPLICATION = _('Section Editor')
PLUGIN = f'{APPLICATION} plugin v@release'
ICON = 'eLogo32'
SECTION_PREFIX = 'sc'
HELP_URL = f'https://peter88213.github.io/{_("nvhelp-en")}/nv_editor/'


def open_help(event=None):
    """Show the online help page specified by HELP_URL."""
    webbrowser.open(HELP_URL)
