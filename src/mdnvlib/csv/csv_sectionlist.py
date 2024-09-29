"""Provide a class for csv section list export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mdnvlib.csv.csv_file import CsvFile
from mdnvlib.model.section import Section
from mdnvlib.novx_globals import SECTIONLIST_SUFFIX
from mdnvlib.novx_globals import _


class CsvSectionList(CsvFile):
    """csv section list writer."""

    DESCRIPTION = _('Section list')
    SUFFIX = SECTIONLIST_SUFFIX

    # Header structure:
    # Section ID (hidden)
    # Section number (link to manuscript)
    # Title
    # Description
    # Viewpoint
    # Date
    # Time
    # Day
    # Duration
    # Tags
    # Section notes
    # Scene
    # Goal
    # Conflict
    # Outcome
    # Status
    # Words total
    # Word count
    # Characters
    # Locations
    # Items

    _fileHeader = f'''table:style-name="ta1" table:print="false">
    <table:table-column table:style-name="co1" table:visibility="collapse" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co4" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co2" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co2" table:default-cell-style-name="ce2"/>
    <table:table-column table:style-name="co1" table:default-cell-style-name="ce4"/>
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co4" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co4" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co4" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co4" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co2" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>
    <table:table-row table:style-name="ro1" table:visibility="collapse">
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>ID</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Section</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Title</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Description</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Viewpoint</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="ce1" office:value-type="string">
      <text:p>Date</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="ce3" office:value-type="string">
      <text:p>Time</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Day</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Duration</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Tags</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Section notes</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Scene</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Goal</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Conflict</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Outcome</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Status</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Words total</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Word count</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Characters</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Locations</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Items</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" table:number-columns-repeated="1003"/>
    </table:table-row>
    <table:table-row table:style-name="ro1">
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>ID</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>{_("Section")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>{_("Title")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>{_("Description")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>{_("Viewpoint")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="ce1" office:value-type="string">
      <text:p>{_("Date")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="ce3" office:value-type="string">
      <text:p>{_("Time")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>{_("Day")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>{_("Duration")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>{_("Tags")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>{_("Section notes")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>{_("Scene")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>$CustomPlotProgress / {_("Goal")} / {_("Reaction")} / $CustomGoal</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>$CustomCharacterization / {_("Conflict")} / {_("Dilemma")} / $CustomConflict</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>$CustomWorldBuilding / {_("Outcome")} / {_("Choice")} / $CustomOutcome</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>{_("Status")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>{_("Words total")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>{_("Section word count")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>{_("Characters")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>{_("Locations")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>{_("Items")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" table:number-columns-repeated="1003"/>
    </table:table-row>

'''

    _sectionTemplate = '''   <table:table-row table:style-name="ro2">
     <table:table-cell office:value-type="string">
      <text:p>$ID</text:p>
     </table:table-cell>
     <table:table-cell table:formula="of:=HYPERLINK(&quot;file:///$ProjectPath/$ProjectName$ManuscriptSuffix.odt#$ID%7Cregion&quot;;&quot;$SectionNumber&quot;)" office:value-type="string" office:string-value="$SectionNumber">
      <text:p>$SectionNumber</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Title</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Desc</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Viewpoint</text:p>
     </table:table-cell>
$DateCell     
$TimeCell
     <table:table-cell office:value-type="string">
      <text:p>$Day</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Duration</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Tags</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Notes</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Scene</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Goal</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Conflict</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Outcome</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Status</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="float" office:value="$WordsTotal">
      <text:p>$WordsTotal</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="float" office:value="$WordCount">
      <text:p>$WordCount</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Characters</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Locations</text:p>
     </table:table-cell>
     <table:table-cell>
      <text:p>$Items</text:p>
     </table:table-cell>
    </table:table-row>

'''

    def _get_sectionMapping(self, scId, sectionNumber, wordsTotal, **kwargs):
        """Return a mapping dictionary for a section section.
        
        Positional arguments:
            scId: str -- section ID.
            sectionNumber: int -- section number to be displayed.
            wordsTotal: int -- accumulated wordcount.
        
        Extends the superclass method.
        """
        sectionMapping = super()._get_sectionMapping(scId, sectionNumber, wordsTotal)
        sectionMapping['Status'] = Section.STATUS[sectionMapping['Status']]
        return sectionMapping

    def _get_header_columns(self):
        """Return a list with all column records of a headline.
        
        Overrides the superclass method
        """
        pltPrgs, chrczn, wrldbld, goal, cflct, outcm, chrBio, chrGls = self._get_renamings()
        columns = []
        columns.append(_("Section"))
        columns.append(_("Date"))
        columns.append(_("Time"))
        columns.append(_("Day"))
        columns.append(_("Title"))
        columns.append(_("Description"))
        columns.append(_("Viewpoint"))
        columns.append(_("Tags"))
        columns.append(_("Scene"))
        columns.append(f'{_("Goal")} / {_("Reaction")} / {goal}')
        columns.append(f'{chrczn} / {_("Conflict")} / {_("Dilemma")} / {cflct}')
        columns.append(f'{wrldbld} / {_("Outcome")} / {_("Choice")} / {outcm}')
        columns.append(_("Notes"))
        return columns

    def _get_section_columns(self, scId, scNumber):
        """Return a list with all column records of a section row.
        
        Overrides the superclass method
        """
        columns = []
        mapping = self._get_sectionMapping(scId, scNumber, 0)
        columns.append(mapping['SectionNumber'])
        columns.append(mapping['Date'])
        columns.append(mapping['Time'])
        columns.append(mapping['Day'])
        columns.append(mapping['Title'])
        columns.append(mapping['Desc'])
        columns.append(mapping['Viewpoint'])
        columns.append(mapping['Tags'])
        columns.append(mapping['Scene'])
        columns.append(mapping['Goal'])
        columns.append(mapping['Conflict'])
        columns.append(mapping['Outcome'])
        columns.append(mapping['Notes'])
        return columns

    def _get_text(self):
        return self._get_sections()

