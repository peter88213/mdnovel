"""Helper module for Markdown processing.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


def sanitize_newlines(text):
    return text.replace('\n\n', '\n').replace('\n', '\n\n').strip()
