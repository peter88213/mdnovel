"""Helper module for removing illegal xml characters.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
import re


def strip_illegal_characters(text):
    return re.sub('[\x00-\x08|\x0b-\x0c|\x0e-\x1f]', '', text)

