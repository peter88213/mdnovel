"""Provide helper functions for date/time processing.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv-timeline
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


def fix_iso_dt(tlDateTime):
    """Return a date/time string with a four-number year.
    
    Positional arguments:
        tlDateTime - date/time string as read in from Timeline.
    
    This is required for comparing date/time strings, 
    and by the datetime.fromisoformat() method.
    """
    if tlDateTime.startswith('-'):
        tlDateTime = tlDateTime.strip('-')
        isBc = True
    else:
        isBc = False
    dt = tlDateTime.split('-', 1)
    dt[0] = dt[0].zfill(4)
    tlDateTime = ('-').join(dt)
    if isBc:
        tlDateTime = f'-{tlDateTime}'
    return tlDateTime
