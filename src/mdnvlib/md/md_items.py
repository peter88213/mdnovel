"""Provide a class for Markdown item descriptions export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.md.md_file import MdFile
from mdnvlib.novx_globals import ITEMS_SUFFIX
from mdnvlib.novx_globals import _


class MdItems(MdFile):
    """Markdown item descriptions file writer.

    Export a item sheet with descriptions.
    """
    DESCRIPTION = _('Item descriptions')
    SUFFIX = ITEMS_SUFFIX

    _fileHeader = f''

    _itemTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">$Title$AKA</text:h>
<text:section text:style-name="Sect1" text:name="$ID">
$Desc
</text:section>
'''

    def _get_itemMapping(self, itId):
        """Return a mapping dictionary for an item section.
        
        Positional arguments:
            itId: str -- item ID.
        
        Special formatting of alternate name. 
        Extends the superclass method.
        """
        itemMapping = super()._get_itemMapping(itId)
        if self.novel.items[itId].aka:
            itemMapping['AKA'] = f' ("{self.novel.items[itId].aka}")'
        return itemMapping
