"""Provide a class for Markdown location descriptions export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.md.md_file import MdFile
from mdnvlib.novx_globals import LOCATIONS_SUFFIX
from mdnvlib.novx_globals import _


class MdLocations(MdFile):
    """Markdown location descriptions file writer.

    Export a location sheet with descriptions.
    """
    DESCRIPTION = _('Location descriptions')
    SUFFIX = LOCATIONS_SUFFIX

    _fileHeader = f''

    _locationTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">$Title$AKA</text:h>
<text:section text:style-name="Sect1" text:name="$ID">
$Desc
</text:section>
'''

    def _get_locationMapping(self, lcId):
        """Return a mapping dictionary for a location section.
        
        Positional arguments:
            lcId: str -- location ID.
        
        Special formatting of alternate name. 
        Extends the superclass method.
        """
        locationMapping = super()._get_locationMapping(lcId)
        if self.novel.locations[lcId].aka:
            locationMapping['AKA'] = f' ("{self.novel.locations[lcId].aka}")'
        return locationMapping
