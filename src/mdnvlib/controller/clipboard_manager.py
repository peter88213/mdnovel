"""Provide a servide class to manage the novelibre tree view clipboard transfer.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import json

from mdnvlib.novx_globals import CHAPTER_PREFIX
from mdnvlib.novx_globals import CHARACTER_PREFIX
from mdnvlib.novx_globals import ITEM_PREFIX
from mdnvlib.novx_globals import LOCATION_PREFIX
from mdnvlib.novx_globals import PLOT_LINE_PREFIX
from mdnvlib.novx_globals import PLOT_POINT_PREFIX
from mdnvlib.novx_globals import PRJ_NOTE_PREFIX
from mdnvlib.novx_globals import SECTION_PREFIX


class ClipboardManager:

    def __init__(self, model, view, controller):
        self._mdl = model
        self._ui = view
        self._ctrl = controller

    def cut_element(self, elemPrefix=None):
        if self._mdl.prjFile is None:
            return

        try:
            node = self._ui.tv.tree.selection()[0]
        except:
            return

        if self.copy_element(elemPrefix) is None:
            return

        if self._ui.tv.tree.prev(node):
            self._ui.tv.go_to_node(self._ui.tv.tree.prev(node))
        else:
            self._ui.tv.go_to_node(self._ui.tv.tree.parent(node))
        self._mdl.delete_element(node, trash=False)
        return 'break'

    def copy_element(self, elemPrefix=None):
        if self._mdl.prjFile is None:
            return

        try:
            node = self._ui.tv.tree.selection()[0]
        except:
            return

        nodePrefix = node[:2]
        if elemPrefix is not None:
            if nodePrefix != elemPrefix:
                return

        elementContainers = {
            CHAPTER_PREFIX: (
                self._mdl.novel.chapters,
                'CHAPTER',
                self._mdl.prjFile.chapterCnv,
            ),
            SECTION_PREFIX: (
                self._mdl.novel.sections,
                'SECTION',
                self._mdl.prjFile.sectionCnv,
            ),
            PLOT_LINE_PREFIX: (
                self._mdl.novel.plotLines,
                'ARC',
                self._mdl.prjFile.plotLineCnv,
            ),
            PLOT_POINT_PREFIX: (
                self._mdl.novel.plotPoints,
                'POINT',
                self._mdl.prjFile.plotPointCnv,
            ),
            CHARACTER_PREFIX: (
                self._mdl.novel.characters,
                'CHARACTER',
                self._mdl.prjFile.characterCnv,
            ),
            LOCATION_PREFIX: (
                self._mdl.novel.locations,
                'LOCATION',
                self._mdl.prjFile.worldElementCnv,
            ),
            ITEM_PREFIX: (
                self._mdl.novel.items,
                'ITEM',
                self._mdl.prjFile.worldElementCnv,
            ),
            PRJ_NOTE_PREFIX: (
                self._mdl.novel.projectNotes,
                'PROJECTNOTE',
                self._mdl.prjFile.basicElementCnv,
            ),
        }
        if not nodePrefix in elementContainers:
            return

        elementContainer, jsonTag, elementCnv = elementContainers[nodePrefix]
        element = elementContainer[node]
        jsonElement = {}
        elementCnv.export_data(element, jsonElement)
        self._remove_references(jsonElement)

        # Get children, if any.
        if nodePrefix == CHAPTER_PREFIX:
            jsonElement['SECTIONS'] = {}
            for scId in self._mdl.novel.tree.get_children(node):
                jsonElement['SECTIONS'][scId] = {}
                jsonSection = jsonElement['SECTIONS'][scId]
                self._mdl.prjFile.sectionCnv.export_data(
                    self._mdl.novel.sections[scId],
                    jsonSection
                )
                self._remove_references(jsonSection)
        elif nodePrefix == PLOT_LINE_PREFIX:
            jsonElement['POINTS'] = {}
            for ppId in self._mdl.novel.tree.get_children(node):
                jsonElement['POINTS'][ppId] = {}
                jsonPlotPoint = jsonElement['POINTS'][ppId]
                self._mdl.prjFile.plotPointCnv.export_data(
                    self._mdl.novel.plotPoints[ppId],
                    jsonPlotPoint
                )
                self._remove_references(jsonPlotPoint)

        text = json.dumps({jsonTag: jsonElement}, ensure_ascii=False)
        # no utf-8 encoding here, because the text is escaped
        self._ui.root.clipboard_clear()
        self._ui.root.clipboard_append(text)
        self._ui.root.update()
        return 'break'

    def paste_element(self, elemPrefix=None):
        if self._mdl.prjFile is None:
            return

        try:
            node = self._ui.tv.tree.selection()[0]
        except:
            return

        try:
            text = self._ui.root.clipboard_get()
            jsonRoot = json.loads(text)
        except:
            return

        prefixes = {
            'CHAPTER': CHAPTER_PREFIX,
            'SECTION': SECTION_PREFIX,
            'ARC': PLOT_LINE_PREFIX,
            'POINT': PLOT_POINT_PREFIX,
            'CHARACTER': CHARACTER_PREFIX,
            'LOCATION': LOCATION_PREFIX,
            'ITEM': ITEM_PREFIX,
            'PROJECTNOTE': PRJ_NOTE_PREFIX
        }
        jsonRootKey = next(iter(jsonRoot))
        nodePrefix = prefixes.get(
            jsonRootKey,
            None
        )
        if nodePrefix is None:
            return

        if elemPrefix is not None:
            if nodePrefix != elemPrefix:
                return

        jsonElement = jsonRoot[jsonRootKey]
        if nodePrefix == SECTION_PREFIX:
            typeStr = jsonElement.get('type', 0)
            if int(typeStr) > 1:
                elemCreator = self._mdl.add_stage
            else:
                elemCreator = self._mdl.add_section
            elemContainer = self._mdl.novel.sections
            elemCnv = self._mdl.prjFile.sectionCnv
        else:
            elementControls = {
                CHAPTER_PREFIX: (
                    self._mdl.add_chapter,
                    self._mdl.novel.chapters,
                    self._mdl.prjFile.chapterCnv,
                ),
                PLOT_LINE_PREFIX: (
                    self._mdl.add_plot_line,
                    self._mdl.novel.plotLines,
                    self._mdl.prjFile.plotLineCnv,
                ),
                PLOT_POINT_PREFIX: (
                    self._mdl.add_plot_point,
                    self._mdl.novel.plotPoints,
                    self._mdl.prjFile.plotPointCnv,
                ),
                CHARACTER_PREFIX: (
                    self._mdl.add_character,
                    self._mdl.novel.characters,
                    self._mdl.prjFile.characterCnv,
                ),
                LOCATION_PREFIX: (
                    self._mdl.add_location,
                    self._mdl.novel.locations,
                    self._mdl.prjFile.worldElementCnv
                ),
                ITEM_PREFIX: (
                    self._mdl.add_item,
                    self._mdl.novel.items,
                    self._mdl.prjFile.worldElementCnv
                ),
                PRJ_NOTE_PREFIX: (
                    self._mdl.add_project_note,
                    self._mdl.novel.projectNotes,
                    self._mdl.prjFile.basicElementCnv,
                )
            }
            if not nodePrefix in elementControls:
                return

            elemCreator, elemContainer, elemCnv = elementControls[nodePrefix]

        elemId = elemCreator(targetNode=node)
        if not elemId:
            return

        elemCnv.import_data(
            elemContainer[elemId],
            jsonElement
        )

        # Get children, if any.
        targetNode = elemId
        if nodePrefix == CHAPTER_PREFIX:
            jsonSections = jsonElement.get('SECTIONS', {})
            for jScId in jsonSections:
                typeStr = jsonSections[jScId].get('type', 0)
                if int(typeStr) > 1:
                    scId = self._mdl.add_stage(targetNode=targetNode)
                else:
                    scId = self._mdl.add_section(targetNode=targetNode)
                self._mdl.prjFile.sectionCnv.import_data(
                    self._mdl.novel.sections[scId],
                    jsonSections[jScId]
                )
                targetNode = scId
        elif nodePrefix == PLOT_LINE_PREFIX:
            jsonPoints = jsonElement.get('POINTS', {})
            for jPpId in jsonPoints:
                ppId = self._mdl.add_plot_point(targetNode=targetNode)
                self._mdl.prjFile.plotPointCnv.import_data(
                    self._mdl.novel.plotPoints[ppId],
                    jsonPoints[jPpId]
                )
                targetNode = ppId

        self._ctrl.refresh_views()
        self._ui.tv.go_to_node(elemId)
        return 'break'

    def _remove_references(self, jsonElement):
        references = [
            'Characters',
            'Locations',
            'Items',
            'PlotlineNotes',
            'Sections',
            'Section',
        ]
        for jsonRef in references:
            if jsonRef in jsonElement:
                del(jsonElement[jsonRef])
