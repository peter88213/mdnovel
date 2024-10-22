"""Provide a class representing a table of relationships.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.novx_globals import CH_ROOT
from mdnvlib.novx_globals import CR_ROOT
from mdnvlib.novx_globals import IT_ROOT
from mdnvlib.novx_globals import LC_ROOT
from mdnvlib.novx_globals import PL_ROOT
from mdnvlib.novx_globals import _
from mdnvlib.plugin.matrix.node import Node
import tkinter as tk


class RelationsTable:
    """Represent a table of relationships. 
    
    The visual part consists of one frame per column, each containing 
    one node per row. 
    The logical part consists of one dictionary per element type (protected instance variables):
    {section ID: {element Id: node}}
    """

    def __init__(self, master, novel, **kwargs):
        """Draw the matrix with blank nodes.
        
        Positional arguments:
            novel: Novel -- Project reference.
            
        """
        self._novel = novel
        self._kwargs = kwargs
        self.draw_matrix(master)

    def draw_matrix(self, master):

        def fill_str(text):
            """Return a string that is at least 7 characters long.
            
            Extend text with spaces so that it does not fall 
            below the length of 7 characters.
            This is for column titles, to widen narrow columns.
            """
            while len(text) < 7:
                text = f' {text} '
            return text

        colorsBackground = ((self._kwargs['color_bg_00'], self._kwargs['color_bg_01']),
                            (self._kwargs['color_bg_10'], self._kwargs['color_bg_11']))
        columns = []
        col = 0
        bgc = col % 2

        #--- Section title column.
        tk.Label(master.topLeft, text=_('Sections')).pack(fill='x')
        tk.Label(master.topLeft, bg=colorsBackground[1][1], text=' ').pack(fill='x')

        #--- Display titles of "normal" sections.
        row = 0
        self._plotlineNodes = {}
        self._characterNodes = {}
        self._locationNodes = {}
        self._itemNodes = {}
        for chId in self._novel.tree.get_children(CH_ROOT):
            if self._novel.chapters[chId].chType == 0:
                for scId in self._novel.tree.get_children(chId):
                    bgr = row % 2
                    if self._novel.sections[scId].scType != 0:
                        continue

                    #--- Initialize matrix section row dictionaries.
                    self._characterNodes[scId] = {}
                    self._locationNodes[scId] = {}
                    self._itemNodes[scId] = {}
                    self._plotlineNodes[scId] = {}

                    tk.Label(master.rowTitles,
                             text=self._novel.sections[scId].title,
                             bg=colorsBackground[bgr][1],
                             justify='left',
                             anchor='w'
                             ).pack(fill='x')
                    row += 1
        bgr = row % 2
        tk.Label(master.rowTitles,
                         text=' ',
                         bg=colorsBackground[bgr][1],
                         ).pack(fill='x')
        tk.Label(master.rowTitles,
                         text=_('Sections'),
                         ).pack(fill='x')

        #--- Plot line columns.
        if self._novel.plotLines:
            plotlineTitleWindow = tk.Frame(master.columnTitles)
            plotlineTitleWindow.pack(side='left', fill='both')
            tk.Label(plotlineTitleWindow, text=_('Plot lines'), bg=self._kwargs['color_arc_heading']).pack(fill='x')
            plotlineTypeColumn = tk.Frame(master.display)
            plotlineTypeColumn.pack(side='left', fill='both')
            plotlineColumn = tk.Frame(plotlineTypeColumn)
            plotlineColumn.pack(fill='both')
            for plId in self._novel.tree.get_children(PL_ROOT):
                # Display plot line titles.
                row = 1
                bgr = row % 2
                bgc = col % 2
                plotlineTitle = fill_str(self._novel.plotLines[plId].shortName)
                tk.Label(plotlineTitleWindow,
                         text=plotlineTitle,
                         bg=colorsBackground[bgr][bgc],
                         justify='left',
                         anchor='w'
                         ).pack(side='left', fill='x', expand=True)
                row += 1

                # Display plot line nodes.
                columns.append(tk.Frame(plotlineColumn))
                columns[col].pack(side='left', fill='both', expand=True)
                for scId in self._plotlineNodes:
                    bgr = row % 2
                    node = Node(columns[col],
                         colorFalse=colorsBackground[bgr][bgc],
                         colorTrue=self._kwargs['color_arc_node']
                         )
                    node.pack(fill='x', expand=True)
                    self._plotlineNodes[scId][plId] = node
                    row += 1
                bgr = row % 2
                tk.Label(columns[col],
                         text=plotlineTitle,
                         bg=colorsBackground[bgr][bgc],
                         justify='left',
                         anchor='w'
                         ).pack(fill='x', expand=True)
                col += 1
            tk.Label(plotlineTypeColumn, text=_('Plot lines'), bg=self._kwargs['color_arc_heading']).pack(fill='x')

        #--- Character columns.
        if self._novel.characters:
            characterTypeColumn = tk.Frame(master.display)
            characterTypeColumn.pack(side='left', fill='both')
            characterColumn = tk.Frame(characterTypeColumn)
            characterColumn.pack(fill='both')
            characterTitleWindow = tk.Frame(master.columnTitles)
            characterTitleWindow.pack(side='left', fill='both')
            tk.Label(characterTitleWindow, text=_('Characters'), bg=self._kwargs['color_character_heading']).pack(fill='x')
            for crId in self._novel.tree.get_children(CR_ROOT):
                # Display character titles.
                row = 1
                bgr = row % 2
                bgc = col % 2
                characterTitle = fill_str(self._novel.characters[crId].title)
                tk.Label(characterTitleWindow,
                         text=characterTitle,
                         bg=colorsBackground[bgr][bgc],
                         justify='left',
                         anchor='w'
                         ).pack(side='left', fill='x', expand=True)
                row += 1

                # Display character nodes.
                columns.append(tk.Frame(characterColumn))
                columns[col].pack(side='left', fill='both', expand=True)
                for scId in self._characterNodes:
                    bgr = row % 2
                    node = Node(columns[col],
                         colorFalse=colorsBackground[bgr][bgc],
                         colorTrue=self._kwargs['color_character_node']
                         )
                    node.pack(fill='x', expand=True)
                    self._characterNodes[scId][crId] = node
                    row += 1
                bgr = row % 2
                tk.Label(columns[col],
                         text=characterTitle,
                         bg=colorsBackground[bgr][bgc],
                         justify='left',
                         anchor='w'
                         ).pack(fill='x', expand=True)
                col += 1
            tk.Label(characterTypeColumn, text=_('Characters'), bg=self._kwargs['color_character_heading']).pack(fill='x')

        #--- Location columns.
        if self._novel.locations:
            locationTypeColumn = tk.Frame(master.display)
            locationTypeColumn.pack(side='left', fill='both')
            locationColumn = tk.Frame(locationTypeColumn)
            locationColumn.pack(fill='both')
            locationTitleWindow = tk.Frame(master.columnTitles)
            locationTitleWindow.pack(side='left', fill='both')
            tk.Label(locationTitleWindow, text=_('Locations'), bg=self._kwargs['color_location_heading']).pack(fill='x')
            for lcId in self._novel.tree.get_children(LC_ROOT):
                # Display location titles.
                row = 1
                bgr = row % 2
                bgc = col % 2
                locationTitle = fill_str(self._novel.locations[lcId].title)
                tk.Label(locationTitleWindow,
                         text=locationTitle,
                         bg=colorsBackground[bgr][bgc],
                         justify='left',
                         anchor='w'
                         ).pack(side='left', fill='x', expand=True)
                row += 1

                # Display location nodes.
                columns.append(tk.Frame(locationColumn))
                columns[col].pack(side='left', fill='both', expand=True)
                for scId in self._locationNodes:
                    bgr = row % 2
                    node = Node(columns[col],
                         colorFalse=colorsBackground[bgr][bgc],
                         colorTrue=self._kwargs['color_location_node']
                         )
                    node.pack(fill='x', expand=True)
                    self._locationNodes[scId][lcId] = node
                    row += 1
                bgr = row % 2
                tk.Label(columns[col],
                         text=locationTitle,
                         bg=colorsBackground[bgr][bgc],
                         justify='left',
                         anchor='w'
                         ).pack(fill='x', expand=True)
                col += 1
            tk.Label(locationTypeColumn, text=_('Locations'), bg=self._kwargs['color_location_heading']).pack(fill='x')

        #--- Item columns.
        if self._novel.items:
            itemTypeColumn = tk.Frame(master.display)
            itemTypeColumn.pack(side='left', fill='both')
            itemColumn = tk.Frame(itemTypeColumn)
            itemColumn.pack(fill='both')
            itemTitleWindow = tk.Frame(master.columnTitles)
            itemTitleWindow.pack(side='left', fill='both')
            tk.Label(itemTitleWindow, text=_('Items'), bg=self._kwargs['color_item_heading']).pack(fill='x')
            for itId in self._novel.tree.get_children(IT_ROOT):
                # Display item titles.
                row = 1
                bgr = row % 2
                bgc = col % 2
                itemTitle = fill_str(self._novel.items[itId].title)
                tk.Label(itemTitleWindow,
                         text=itemTitle,
                         bg=colorsBackground[bgr][bgc],
                         justify='left',
                         anchor='w'
                         ).pack(side='left', fill='x', expand=True)
                row += 1

                # Display item nodes.
                columns.append(tk.Frame(itemColumn))
                columns[col].pack(side='left', fill='both', expand=True)
                for scId in self._itemNodes:
                    bgr = row % 2
                    node = Node(columns[col],
                         colorFalse=colorsBackground[bgr][bgc],
                         colorTrue=self._kwargs['color_item_node']
                         )
                    node.pack(fill='x', expand=True)
                    self._itemNodes[scId][itId] = node
                    row += 1
                bgr = row % 2
                tk.Label(columns[col],
                         text=itemTitle,
                         bg=colorsBackground[bgr][bgc],
                         justify='left',
                         anchor='w'
                         ).pack(fill='x', expand=True)
                col += 1
            tk.Label(itemTypeColumn, text=_('Items'), bg=self._kwargs['color_item_heading']).pack(fill='x')

    def set_nodes(self):
        """Loop through all nodes, setting states."""
        for scId in self._plotlineNodes:

            # Plot lines.
            for plId in self._novel.plotLines:
                self._plotlineNodes[scId][plId].state = (plId in self._novel.sections[scId].scPlotLines)

            # Characters.
            for crId in self._novel.characters:
                self._characterNodes[scId][crId].state = (crId in self._novel.sections[scId].characters)

            # Locations.
            for lcId in self._novel.locations:
                self._locationNodes[scId][lcId].state = (lcId in self._novel.sections[scId].locations)

            # Items.
            for itId in self._novel.items:
                self._itemNodes[scId][itId].state = (itId in self._novel.sections[scId].items)

    def get_nodes(self):
        """Loop through all nodes, modifying the sections according to the states."""
        for scId in self._plotlineNodes:

            # Plot lines.
            self._novel.sections[scId].scPlotLines = []
            for plId in self._novel.plotLines:
                plotlineSections = self._novel.plotLines[plId].sections
                if self._plotlineNodes[scId][plId].state:
                    self._novel.sections[scId].scPlotLines.append(plId)
                    if not scId in plotlineSections:
                        plotlineSections.append(scId)
                else:
                    if scId in plotlineSections:
                        plotlineSections.remove(scId)
                    for ppId in list(self._novel.sections[scId].scPlotPoints):
                        if self._novel.sections[scId].scPlotPoints[ppId] == plId:
                            del self._novel.sections[scId].scPlotPoints[ppId]
                            self._novel.plotPoints[ppId].sectionAssoc = None
                            # don't trigger the update here
                self._novel.plotLines[plId].sections = plotlineSections

            # Characters.
            scCharacters = self._novel.sections[scId].characters
            # this keeps the order
            for crId in self._novel.characters:
                if self._characterNodes[scId][crId].state:
                    if not crId in scCharacters:
                        scCharacters.append(crId)
                elif crId in scCharacters:
                    scCharacters.remove(crId)
            self._novel.sections[scId].characters = scCharacters

            # Locations.
            scLocations = self._novel.sections[scId].locations
            for lcId in self._novel.locations:
                if self._locationNodes[scId][lcId].state:
                    if not lcId in scLocations:
                        scLocations.append(lcId)
                elif lcId in scLocations:
                    scLocations.remove(lcId)
            self._novel.sections[scId].locations = scLocations

            # Items.
            scItems = self._novel.sections[scId].items
            for itId in self._novel.items:
                if self._itemNodes[scId][itId].state:
                    if itId in scItems:
                        scItems.append(itId)
                elif itId in scItems:
                    scItems.remove(itId)

            self._novel.sections[scId].items = scItems

