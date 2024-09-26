"""Provide a converter class for mdnovel universal import and export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnvlib
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from mdnvlib.converter.converter_ff import ConverterFf
from mdnvlib.converter.new_project_factory import NewProjectFactory
from mdnvlib.mdnov.mdnov_file import MdnovFile
from novxlib.ods.ods_r_charlist import OdsRCharList
from novxlib.ods.ods_r_grid import OdsRGrid
from novxlib.ods.ods_r_itemlist import OdsRItemList
from novxlib.ods.ods_r_loclist import OdsRLocList
from novxlib.ods.ods_w_charlist import OdsWCharList
from novxlib.ods.ods_w_grid import OdsWGrid
from novxlib.ods.ods_w_itemlist import OdsWItemList
from novxlib.ods.ods_w_loclist import OdsWLocList
from novxlib.ods.ods_w_plot_list import OdsWPlotList
from novxlib.ods.ods_w_sectionlist import OdsWSectionList
from novxlib.odt.odt_r_chapterdesc import OdtRChapterDesc
from novxlib.odt.odt_r_characters import OdtRCharacters
from novxlib.odt.odt_r_items import OdtRItems
from novxlib.odt.odt_r_locations import OdtRLocations
from novxlib.odt.odt_r_partdesc import OdtRPartDesc
from novxlib.odt.odt_r_plotlines import OdtRPlotlines
from novxlib.odt.odt_r_sectiondesc import OdtRSectionDesc
from novxlib.odt.odt_r_stages import OdtRStages
from novxlib.odt.odt_w_brief_synopsis import OdtWBriefSynopsis
from novxlib.odt.odt_w_chapterdesc import OdtWChapterDesc
from novxlib.odt.odt_w_characters import OdtWCharacters
from novxlib.odt.odt_w_export import OdtWExport
from novxlib.odt.odt_w_items import OdtWItems
from novxlib.odt.odt_w_locations import OdtWLocations
from novxlib.odt.odt_w_partdesc import OdtWPartDesc
from novxlib.odt.odt_w_plotlines import OdtWPlotlines
from novxlib.odt.odt_w_sectiondesc import OdtWSectionDesc
from novxlib.odt.odt_w_stages import OdtWStages
from novxlib.odt.odt_w_xref import OdtWXref


class NovxConverter(ConverterFf):
    """A converter for universal import and export.

    Support mdnovel projects and most of the File subclasses 
    that can be read or written by OpenOffice/LibreOffice.

    Overrides the superclass constants EXPORT_SOURCE_CLASSES,
    EXPORT_TARGET_CLASSES, IMPORT_SOURCE_CLASSES, IMPORT_TARGET_CLASSES.

    Class constants:
        CREATE_SOURCE_CLASSES -- list of classes that - additional to HtmlImport
                        and HtmlOutline - can be exported to a new mdnovel project.
    """
    EXPORT_SOURCE_CLASSES = [MdnovFile]
    EXPORT_TARGET_CLASSES = [
        OdsWCharList,
        OdsWGrid,
        OdsWItemList,
        OdsWLocList,
        OdsWPlotList,
        OdsWSectionList,
        OdtWBriefSynopsis,
        OdtWChapterDesc,
        OdtWCharacters,
        OdtWExport,
        OdtWItems,
        OdtWLocations,
        OdtWPartDesc,
        OdtWPlotlines,
        OdtWSectionDesc,
        OdtWStages,
        OdtWXref,
    ]
    IMPORT_SOURCE_CLASSES = [
        OdsRCharList,
        OdsRGrid,
        OdsRItemList,
        OdsRLocList,
        OdtRChapterDesc,
        OdtRCharacters,
        OdtRItems,
        OdtRLocations,
        OdtRPartDesc,
        OdtRPlotlines,
        OdtRSectionDesc,
        OdtRStages,
    ]
    IMPORT_TARGET_CLASSES = [MdnovFile]
    CREATE_SOURCE_CLASSES = []

    def __init__(self):
        """Change the newProjectFactory strategy.
        
        Extends the superclass constructor.
        """
        super().__init__()
        self.newProjectFactory = NewProjectFactory(self.CREATE_SOURCE_CLASSES)
