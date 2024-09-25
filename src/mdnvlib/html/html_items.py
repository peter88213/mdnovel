"""Provide a class for HTML items report file representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnvlib
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from mdnvlib.html.html_report import HtmlReport
from mdnvlib.novx_globals import ITEM_REPORT_SUFFIX
from mdnvlib.novx_globals import _


class HtmlItems(HtmlReport):
    """Class for HTML items report file representation."""
    DESCRIPTION = 'HTML items report'
    EXTENSION = '.html'
    SUFFIX = ITEM_REPORT_SUFFIX

    _fileHeader = f'''{HtmlReport._fileHeader}
<title>{_('Items')} ($Title)</title>
</head>

<body>
<p class=title>$Title {_('by')} $AuthorName - {_('Items')}</p>
<table>
<tr class="heading">
<td class="chtitle">{_('Name')}</td>
<td>{_('AKA')}</td>
<td>{_('Tags')}</td>
<td>{_('Description')}</td>
</tr>
'''

    _itemTemplate = '''<tr>
<td class="chtitle">$Title</td>
<td>$AKA</td>
<td>$Tags</td>
<td>$Desc</td>
</tr>
'''

