"""Provide a class for Markdown item descriptions export.

Copyright (c) 2025 Peter Triesberger
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

    _fileHeader = f'{MdFile._fileHeader}# {DESCRIPTION}\n\n'
    _itemTemplate = '\n## $Title$AKA\n\n$Desc'

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
        else:
            itemMapping['AKA'] = ''
        if self.novel.items[itId].desc:
            itemMapping['Desc'] = f'### {_("Description")}\n\n{self.novel.items[itId].desc}\n\n'
        else:
            itemMapping['Desc'] = ''
        return itemMapping
