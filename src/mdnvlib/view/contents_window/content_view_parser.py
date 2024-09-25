"""Provide a class for parsing novx section content, generating tags for the text box.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from xml import sax


class ContentViewParser(sax.ContentHandler):
    """A novx section content parser."""
    BULLET = '•'

    def __init__(self):
        super().__init__()
        self.textTag = ''
        self.xmlTag = ''
        self.emTag = ''
        self.strongTag = ''
        self.commentTag = ''
        self.commentXmlTag = ''
        self.noteTag = ''
        self.noteXmlTag = ''

        self._marks = {
            'em':'*',
            'strong':'**'
        }

        self.taggedText = None
        # tagged text, assembled by the parser

        self._list = None
        self._comment = None
        self._note = None
        self._em = None
        self._strong = None

    def feed(self, xmlString):
        """Feed a string file to the parser.
        
        Positional arguments:
            filePath: str -- novx document path.        
        """
        self.taggedText = []
        self._list = False
        self._comment = False
        self._note = False
        self._em = False
        self._strong = False
        if xmlString:
            sax.parseString(f'<content>{xmlString}</content>', self)

    def characters(self, content):
        """Receive notification of character data.
        
        Overrides the xml.sax.ContentHandler method             
        """
        tag = self.textTag
        if self._em:
            tag = self.emTag
        elif self._strong:
            tag = self.strongTag
        if self._comment:
            tag = self.commentTag
        elif self._note:
            tag = self.noteTag
        self.taggedText.append((content, tag))

    def endElement(self, name):
        """Signals the end of an element in non-namespace mode.
        
        Overrides the xml.sax.ContentHandler method     
        """
        tag = self.xmlTag
        suffix = ''
        if self._comment:
            tag = self.commentXmlTag
        elif self._note:
            tag = self.noteXmlTag
        if name == 'p' and not self._list:
            suffix = '\n'
        elif name == 'em':
            self._em = False
        elif name == 'strong':
            self._strong = False
        if self.showTags:
            self.taggedText.append((f'{self._marks.get(name, "")}{suffix}', tag))
        else:
            self.taggedText.append((suffix, tag))

    def startElement(self, name, attrs):
        """Signals the start of an element in non-namespace mode.
        
        Overrides the xml.sax.ContentHandler method             
        """
        tag = self.xmlTag
        suffix = ''
        if name == 'em':
            self._em = True
        elif name == 'strong':
            self._strong = True
        if self.showTags:
            self.taggedText.append((f'{self._marks.get(name, '')}{suffix}', tag))
        else:
            self.taggedText.append((suffix, tag))
