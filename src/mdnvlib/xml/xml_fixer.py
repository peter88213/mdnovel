"""Provide a parser to fix malformed XML.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from html.parser import HTMLParser
from html import escape


class XmlFixer(HTMLParser):
    """Event driven parser that accepts malformed XML."""

    def __init__(self, tags):
        """Set the format tags that must not overlap.
        
        Positional arguments:
            tags: set of str, e.g. ('em', 'strong')
        """
        super().__init__()
        self._formatTags = tags
        # set of formatting tags to consider
        self._fixedXmlStr = []
        # list of processed lines
        self._format = []
        # stack for nested formattings

    def fixed(self, xmlStr):
        """Return an XML string with wrong format nestings fixed.
        
        Overrides the superclass method             
        """
        self.feed(xmlStr)
        return ''.join(self._fixedXmlStr)

    def handle_data(self, data):
        """Generally keep all character data. 
        
        Escape characters reserved for XML.
        Overrides the superclass method             
        """
        self._fixedXmlStr.append(escape(data))

    def handle_endtag(self, tag):
        """Close formatting areas if needed to avoid overlapping.
        
        Overrides the superclass method             
        """
        if tag in self._formatTags:
            if not tag in self._format:
                # formatting area is already closed
                return

            while  self._format[-1] != tag:
                self._fixedXmlStr.append(f'</{self._format.pop()}>')
                # closing overlapping formatting area
            self._format.pop()
            # removing the tag from the stack
        self._fixedXmlStr.append(f'</{tag}>')

    def handle_starttag(self, tag, attrs):
        """Keep all tags, except multiple formatting tags of the same kind.
        
        Overrides the superclass method             
        """
        if tag in self._formatTags:
            if tag in self._format:
                return

            self._format.append(tag)
            # pushing the tag on the stack
        attrStr = ''
        for name, value in attrs:
            attrStr = f'{attrStr} {name}="{value}"'
        self._fixedXmlStr.append(f'<{tag}{attrStr}>')

