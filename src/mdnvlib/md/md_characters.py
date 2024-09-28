"""Provide a class for Markdown character descriptions export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.md.md_file import MdFile
from mdnvlib.novx_globals import CHARACTERS_SUFFIX
from mdnvlib.novx_globals import _


class MdCharacters(MdFile):
    """Markdown character descriptions file writer.

    Export a character sheet with descriptions.
    """
    DESCRIPTION = _('Character descriptions')
    SUFFIX = CHARACTERS_SUFFIX

    _fileHeader = f'{MdFile._fileHeader}# {DESCRIPTION}\n\n'
    _characterTemplate = f'''\n## $Title$FullName$AKA\n\n$Desc$Bio$Goals'''

    def _get_characterMapping(self, crId):
        """Return a mapping dictionary for a character section.
        
        Positional arguments:
            crId: str -- character ID.
        
        Special formatting of alternate and full name. 
        Extends the superclass method.
        """
        characterMapping = super()._get_characterMapping(crId)
        if self.novel.characters[crId].aka:
            characterMapping['AKA'] = f' ("{self.novel.characters[crId].aka}")'
        else:
            characterMapping['AKA'] = ''
        if self.novel.characters[crId].fullName:
            characterMapping['FullName'] = f'/{self.novel.characters[crId].fullName}'
        else:
            characterMapping['FullName'] = ''
        if self.novel.characters[crId].desc:
            characterMapping['Desc'] = f'### {_("Description")}\n\n{self.novel.characters[crId].desc}\n\n'
        else:
            characterMapping['Desc'] = ''
        if self.novel.characters[crId].bio:
            characterMapping['Bio'] = f"### {characterMapping['CustomChrBio']}\n\n{self.novel.characters[crId].bio}\n\n"
        else:
            characterMapping['Bio'] = ''
        if self.novel.characters[crId].goals:
            characterMapping['Goals'] = f"### {characterMapping['CustomChrGoals']}\n\n{self.novel.characters[crId].goals}\n\n"
        else:
            characterMapping['Goals'] = ''

        return characterMapping
