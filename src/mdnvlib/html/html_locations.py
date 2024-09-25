"""Provide a class for HTML locations report file representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnvlib
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from mdnvlib.html.html_report import HtmlReport
from mdnvlib.novx_globals import LOCATION_REPORT_SUFFIX
from mdnvlib.novx_globals import _


class HtmlLocations(HtmlReport):
    """Class for HTML locations report file representation."""
    DESCRIPTION = 'HTML locations report'
    EXTENSION = '.html'
    SUFFIX = LOCATION_REPORT_SUFFIX

    _fileHeader = f'''{HtmlReport._fileHeader}
<title>{_('Locations')} ($Title)</title>
</head>

<body>
<p class=title>$Title {_('by')} $AuthorName - {_('Locations')}</p>
<table>
<tr class="heading">
<td class="chtitle">{_('Name')}</td>
<td>{_('AKA')}</td>
<td>{_('Tags')}</td>
<td>{_('Description')}</td>
</tr>
'''

    _locationTemplate = '''<tr>
<td class="chtitle">$Title</td>
<td>$AKA</td>
<td>$Tags</td>
<td>$Desc</td>
</tr>
'''

