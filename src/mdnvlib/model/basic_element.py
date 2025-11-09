"""Provide a base class for mdnovel element representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from urllib.parse import quote
from urllib.parse import unquote


class BasicElement:
    """Basic data model element representation.

    Public instance variables:
        on_element_change -- Points to a callback routine for element changes
        
    The on_element_change method is called when the value of any property changes.
    This method can be overridden at runtime for each individual element instance.
    """

    def __init__(self,
            on_element_change=None,
            title=None,
            desc=None,
            links=None):
        """Set the initial values.

        If on_element_change is None, the do_nothing method will be assigned to it.
            
        General note:
        When merging files, only new elements that are not None will override 
        existing elements. This allows you to easily update a mdnovel project 
        from a document that contains only a subset of the data model.
        Keep this in mind when setting the initial values.
        """
        if on_element_change is None:
            self.on_element_change = self.do_nothing
        else:
            self.on_element_change = on_element_change
        self._title = title
        self._desc = desc
        if links is None:
            self._links = {}
        else:
            self._links = links

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._title != newVal:
            self._title = newVal
            self.on_element_change()

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._desc != newVal:
            self._desc = newVal
            self.on_element_change()

    @property
    def links(self):
        # dict: (Key:str -- relative path, value:str -- full path)
        try:
            return self._links.copy()
        except AttributeError:
            return None

    @links.setter
    def links(self, newVal):
        if newVal is not None:
            for elem in newVal:
                val = newVal[elem]
                if val is not None:
                    assert type(val) == str
        if self._links != newVal:
            self._links = newVal
            self.on_element_change()

    def do_nothing(self):
        """Standard callback routine for element changes."""
        pass

    def get_links(self):
        """Return a list of (relative link, absolute link) tuples."""
        linkList = []
        if self.links:
            for path in self.links:
                relativeLink = f'[LinkPath]({quote(path)})'
                if self.links[path]:
                    absoluteLink = f'[FullPath](file:///{quote(self.links[path])})'
                else:
                    absoluteLink = ''
                linkList.append((relativeLink, absoluteLink))
        return linkList

    def set_links(self, linkList):
        links = self.links
        for relativeLink, absoluteLink in linkList:
            links[unquote(relativeLink)] = unquote(absoluteLink).split('file:///')[1]
        self.links = links

