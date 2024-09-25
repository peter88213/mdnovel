"""Helper module for ID generation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnvlib
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""


def create_id(elements, prefix=''):
    """Return an unused ID for a new element.
    
    Positional arguments:
        elements -- list or dictionary containing all existing IDs
    """
    i = 1
    while f'{prefix}{i}' in elements:
        i += 1
    return f'{prefix}{i}'

