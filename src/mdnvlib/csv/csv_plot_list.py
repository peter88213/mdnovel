"""Provide a class for csv plot list representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/yw-table
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from mdnvlib.csv.csv_file import CsvFile
from mdnvlib.novx_globals import CH_ROOT
from mdnvlib.novx_globals import PLOTLINES_SUFFIX
from mdnvlib.novx_globals import PLOTLIST_SUFFIX
from mdnvlib.novx_globals import PL_ROOT
from mdnvlib.novx_globals import _
from mdnvlib.novx_globals import list_to_string


class CsvPlotList(CsvFile):
    """csv plot list representation.

    Public instance variables:
        filePath: str -- path to the file (property with getter and setter). 

    """
    DESCRIPTION = _('csv Plot list')
    SUFFIX = PLOTLIST_SUFFIX

    _CE_OFFSET = 6

    _fileHeader = ''
    _fileHeader = f'{_fileHeader}{DESCRIPTION}" table:style-name="ta1" table:print="false">'

    def write_content_xml(self):
        """Create the csv table.
        
        Raise the "Error" exception in case of error. 
        Extends the superclass method.
        """

        def create_cell(text, attr='', link=''):
            """Return the markup for a table cell with text and attributes."""
            if link:
                attr = f'{attr} table:formula="of:=HYPERLINK(&quot;file:///{self.projectPath}/{self._convert_from_novx(self.projectName)}{link}&quot;;&quot;{self._convert_from_novx(text, isLink=True)}&quot;)"'
                text = ''
            else:
                text = f'\n      <text:p>{self._convert_from_novx(text)}</text:p>'
            return f'     <table:table-cell {attr} office:value-type="string">{text}\n     </table:table-cell>'

        odsText = [
            self._fileHeader,
            '<table:table-column table:style-name="co4" table:default-cell-style-name="Default"/>',
        ]

        plotLineColorsTotal = 6
        # total number of the background colors used in the "ce" table cell styles

        # Get plot lines.
        if self.novel.tree.get_children(PL_ROOT) is not None:
            plotLines = self.novel.tree.get_children(PL_ROOT)
        else:
            plotLines = []

        # Plot line columns.
        for plId in plotLines:
            odsText.append('<table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>')

        # Title row.
        odsText.append('   <table:table-row table:style-name="ro2">')
        odsText.append(create_cell(''))
        for i, plId in enumerate(plotLines):
            colorIndex = (i % plotLineColorsTotal) + self._CE_OFFSET
            odsText.append(
                create_cell(
                    self.novel.plotLines[plId].title,
                    attr=f'table:style-name="ce{colorIndex}"',
                    link=f'{PLOTLINES_SUFFIX}.odt#{plId}'
                )
            )
        odsText.append('    </table:table-row>')

        # Section rows.
        for chId in self.novel.tree.get_children(CH_ROOT):
            for scId in self.novel.tree.get_children(chId):
                # Section row
                if self.novel.sections[scId].scType == 0:
                    odsText.append('   <table:table-row table:style-name="ro2">')
                    odsText.append(
                        create_cell(
                            self.novel.sections[scId].title,
                            link=f'.odt#{scId}%7Cregion'
                        )
                    )
                    for i, plId in enumerate(plotLines):
                        colorIndex = (i % plotLineColorsTotal) + self._CE_OFFSET
                        if scId in self.novel.plotLines[plId].sections:
                            plotPoints = []
                            for ppId in self.novel.tree.get_children(plId):
                                if scId == self.novel.plotPoints[ppId].sectionAssoc:
                                    plotPoints.append(self.novel.plotPoints[ppId].title)
                            odsText.append(
                                create_cell(
                                    list_to_string(plotPoints),
                                    attr=f'table:style-name="ce{colorIndex}" '
                                )
                            )
                        else:
                            odsText.append(create_cell(''))
                    odsText.append(f'    </table:table-row>')

        odsText.append(self._CONTENT_XML_FOOTER)
        with open(self.filePath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(odsText))
