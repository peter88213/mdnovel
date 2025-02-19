"""Provide the main controller class for mdnovel.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys
from tkinter import filedialog

from apptk.controller.controller_base import ControllerBase
from mdnvlib.controller.link_processor import LinkProcessor
from mdnvlib.exporter.nv_doc_exporter import NvDocExporter
from mdnvlib.exporter.nv_html_reporter import NvHtmlReporter
from mdnvlib.importer.nv_doc_importer import NvDocImporter
from mdnvlib.model.nv_model import NvModel
from mdnvlib.model.nv_work_file import NvWorkFile
from mdnvlib.novx_globals import CHAPTER_PREFIX
from mdnvlib.novx_globals import CHARACTER_PREFIX
from mdnvlib.novx_globals import CH_ROOT
from mdnvlib.novx_globals import CR_ROOT
from mdnvlib.novx_globals import Error
from mdnvlib.novx_globals import ITEM_PREFIX
from mdnvlib.novx_globals import IT_ROOT
from mdnvlib.novx_globals import LC_ROOT
from mdnvlib.novx_globals import LOCATION_PREFIX
from mdnvlib.novx_globals import PLOT_LINE_PREFIX
from mdnvlib.novx_globals import PLOT_POINT_PREFIX
from mdnvlib.novx_globals import PL_ROOT
from mdnvlib.novx_globals import PN_ROOT
from mdnvlib.novx_globals import PRJ_NOTE_PREFIX
from mdnvlib.novx_globals import SECTION_PREFIX
from mdnvlib.novx_globals import _
from mdnvlib.novx_globals import norm_path
from mdnvlib.nv_globals import prefs
from mdnvlib.plugin.nv_plugin_collection import NvPluginCollection
from mdnvlib.view.nv_view import NvView


class NvController(ControllerBase):
    """Controller for the mdnovel application."""

    def __init__(self, title, tempDir):
        """Initialize the model, set up the application's user interface, and load plugins.
    
        Positional arguments:
            title: str -- Application title to be displayed at the window frame.
            tempDir: str -- Path of the temporary directory, used for e.g. packing zipfiles. 
        
        Extends the superclass constructor.
        """
        super().__init__(title)
        self.tempDir = tempDir

        #--- Create the model.
        self._mdl = NvModel()
        self._mdl.register_client(self)

        #--- Build the GUI.
        self._ui = NvView(self._mdl, self, title)

        self.launchers = {}
        # launchers for opening linked non-standard filetypes.

        self.linkProcessor = LinkProcessor(self._mdl)
        # strategy for processing links

        self._fileTypes = [(NvWorkFile.DESCRIPTION, NvWorkFile.EXTENSION)]
        self.importFiletypes = [(_('Markdown document'), '.md')]

        # Link the model to the view.
        # Strictly speaking, this breaks the MVC pattern, since the
        # model depends on a data structure defined by the GUI framework.
        self._mdl.tree = self._ui.tv.tree

        #--- Initialize the plugins.
        self.plugins = NvPluginCollection(self._mdl, self._ui, self)

        self.disable_menu()
        self._ui.tv.reset_view()

    def add_chapter(self, **kwargs):
        """Add a chapter to the novel.
             
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Section title. Default: Auto-generated title. 
            chType: int -- Chapter type. Default: 0.
            NoNumber: str -- Do not auto-number this chapter. Default: None.
            
        Return the chapter ID, if successful.
        """
        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.tv.tree.selection()[0]
            except:
                pass
        newNode = self._mdl.add_chapter(**kwargs)
        self._view_new_element(newNode)
        return newNode

    def add_character(self, **kwargs):
        """Add a character to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title.
            isMajor: bool -- If True, make the new character a major character. Default: False.
            
        Return the element's ID, if successful.
        """
        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.tv.tree.selection()[0]
            except:
                pass
        newNode = self._mdl.add_character(**kwargs)
        self._view_new_element(newNode)
        return newNode

    def add_child(self, event=None):
        """Add a child element to an element.
        
        What kind of element is added, depends on the selection's prefix.
        """
        if self._mdl.prjFile is None:
            return

        try:
            selection = self._ui.tv.tree.selection()[0]
        except:
            return

        if selection == CH_ROOT:
            self.add_chapter(targetNode=selection)
            return

        if selection.startswith(CHAPTER_PREFIX):
            self.add_section(targetNode=selection)
            return

        if selection.startswith(PLOT_LINE_PREFIX):
            self.add_plot_point(targetNode=selection)
            return

        if selection == CR_ROOT:
            self.add_character(targetNode=selection)
            return

        if selection == LC_ROOT:
            self.add_location(targetNode=selection)
            return

        if selection == IT_ROOT:
            self.add_item(targetNode=selection)
            return

        if selection == PL_ROOT:
            self.add_plot_line(targetNode=selection)
            return

        if selection == PN_ROOT:
            self.add_project_note(targetNode=selection)

    def add_element(self, event=None):
        """Add an element to the novel.
        
        What kind of element is added, depends on the selection's prefix.
        """
        if self._mdl.prjFile is None:
            return

        try:
            selection = self._ui.tv.tree.selection()[0]
        except:
            return

        if selection.startswith(SECTION_PREFIX):
            if self._mdl.novel.sections[selection].scType < 2:
                self.add_section(targetNode=selection)
                return

            self.add_stage(targetNode=selection)
            return

        if CHAPTER_PREFIX in selection:
            self.add_chapter(targetNode=selection)
            return

        if CHARACTER_PREFIX in selection:
            self.add_character(targetNode=selection)
            return

        if LOCATION_PREFIX in selection:
            self.add_location(targetNode=selection)
            return

        if ITEM_PREFIX in selection:
            self.add_item(targetNode=selection)
            return

        if PLOT_LINE_PREFIX in selection:
            self.add_plot_line(targetNode=selection)
            return

        if PRJ_NOTE_PREFIX in selection:
            self.add_project_note(targetNode=selection)
            return

        if selection.startswith(PLOT_POINT_PREFIX):
            self.add_plot_point(targetNode=selection)

    def add_item(self, **kwargs):
        """Add an item to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title. 
            
        Return the element's ID, if successful.
        """
        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.tv.tree.selection()[0]
            except:
                pass
        newNode = self._mdl.add_item(**kwargs)
        self._view_new_element(newNode)
        return newNode

    def add_location(self, **kwargs):
        """Add a location to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title. 
            
        Return the element's ID, if successful.
        """
        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.tv.tree.selection()[0]
            except:
                pass
        newNode = self._mdl.add_location(**kwargs)
        self._view_new_element(newNode)
        return newNode

    def add_parent(self, event=None):
        """Add a parent element to an element.
        
        What kind of element is added, depends on the selection's prefix.
        """
        if self._mdl.prjFile is None:
            return

        try:
            selection = self._ui.tv.tree.selection()[0]
        except:
            return

        if selection.startswith(SECTION_PREFIX):
            self.add_chapter(targetNode=selection)
        elif selection.startswith(PLOT_POINT_PREFIX):
            self.add_plot_line(targetNode=selection)

    def add_part(self, **kwargs):
        """Add a part to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str: Part title. Default -- Auto-generated title. 
            chType: int: Part type. Default -- 0.  
            NoNumber: str: Do not auto-number this part. Default -- None.
           
        Return the chapter ID, if successful.
        """
        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.tv.tree.selection()[0]
            except:
                pass
        newNode = self._mdl.add_part(**kwargs)
        self._view_new_element(newNode)
        return newNode

    def add_plot_line(self, **kwargs):
        """Add a plot line to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title. 
            
        Return the plot line ID, if successful.
        """
        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.tv.tree.selection()[0]
            except:
                pass
        newNode = self._mdl.add_plot_line(**kwargs)
        self._view_new_element(newNode)
        return newNode

    def add_plot_point(self, **kwargs):
        """Add a plot point to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Section title. Default: Auto-generated title. 
            
        Return the plot point ID, if successful.
        """
        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.tv.tree.selection()[0]
            except:
                pass
        newNode = self._mdl.add_plot_point(**kwargs)
        self._view_new_element(newNode)
        return newNode

    def add_project_note(self, **kwargs):
        """Add a Project note to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title. 
            
        Return the element's ID, if successful.
        """
        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.tv.tree.selection()[0]
            except:
                pass
        newNode = self._mdl.add_project_note(**kwargs)
        self._view_new_element(newNode)
        return newNode

    def add_section(self, **kwargs):
        """Add a section to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Section title. Default: Auto-generated title. 
            desc: str -- Description.
            scType: int -- Section type. Default: 0.
            status: int -- Section status. Default: 1.
            scene: int -- Scene kind. Default = 0.
            appendToPrev: bool -- Append to previous section. Default: False.
            
        - Place the new node at the next free position after the selection, if possible.
        - Otherwise, do nothing. 
        
        Return the section ID, if successful.
        """
        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.tv.tree.selection()[0]
            except:
                pass
        newNode = self._mdl.add_section(**kwargs)
        self._view_new_element(newNode)
        return newNode

    def add_stage(self, **kwargs):
        """Add a stage to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Stage title. Default: Auto-generated title. 
            desc: str -- Description.
            scType: int -- Scene type. Default: 3.
            
        Return the section ID, if successful.
        """
        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.tv.tree.selection()[0]
            except:
                pass
        newNode = self._mdl.add_stage(**kwargs)
        self._view_new_element(newNode)
        return newNode

    def close_project(self, event=None, doNotSave=False):
        """Close the current project.
        
        - Save changes
        - clear all views
        - reset flags
        """
        self._ui.propertiesView.apply_changes()
        self.plugins.on_close()
        if self._mdl.isModified and not doNotSave:
            if self._ui.ask_yes_no(_('Save changes?')):
                if not self.save_project():
                    self._ui.show_error(_('Cannot save the project'), _('Critical Error'))

        self._ui.propertiesView._view_nothing()
        self._mdl.close_project()
        self._ui.tv.reset_view()
        self._ui.contentsView.reset_view()
        self._ui.root.title(self._ui.title)
        self.show_status('')
        self._ui.show_path('')
        self.disable_menu()
        return 'break'

    def delete_elements(self, event=None, elements=None):
        """Delete elements and their children.
        
        Optional arguments:
            elements: list of IDs of the elements to delete.        
        """
        if elements is None:
            try:
                elements = self._ui.tv.tree.selection()
            except:
                return

        for  elemId in elements:
            if elemId.startswith(SECTION_PREFIX):
                if self._mdl.novel.sections[elemId].scType < 2:
                    candidate = f'{_("Section")} "{self._mdl.novel.sections[elemId].title}"'
                else:
                    candidate = f'{_("Stage")} "{self._mdl.novel.sections[elemId].title}"'
            elif elemId.startswith(CHAPTER_PREFIX):
                candidate = f'{_("Chapter")} "{self._mdl.novel.chapters[elemId].title}"'
            elif elemId.startswith(CHARACTER_PREFIX):
                candidate = f'{_("Character")} "{self._mdl.novel.characters[elemId].title}"'
            elif elemId.startswith(LOCATION_PREFIX):
                candidate = f'{_("Location")} "{self._mdl.novel.locations[elemId].title}"'
            elif elemId.startswith(ITEM_PREFIX):
                candidate = f'{_("Item")} "{self._mdl.novel.items[elemId].title}"'
            elif elemId.startswith(PLOT_LINE_PREFIX):
                candidate = f'{_("Plot line")} "{self._mdl.novel.plotLines[elemId].title}"'
            elif elemId.startswith(PLOT_POINT_PREFIX):
                candidate = f'{_("Plot point")} "{self._mdl.novel.plotPoints[elemId].title}"'
            elif elemId.startswith(PRJ_NOTE_PREFIX):
                candidate = f'{_("Project note")} "{self._mdl.novel.projectNotes[elemId].title}"'
            else:
                return

            if not self._ui.ask_yes_no(_('Delete {}?').format(candidate)):
                return

            if self._ui.tv.tree.prev(elemId):
                self._view_new_element(self._ui.tv.tree.prev(elemId))
            else:
                self._view_new_element(self._ui.tv.tree.parent(elemId))
            self._mdl.delete_element(elemId)

    def export_document(self, suffix, **kwargs):
        """Export a document.
        
        Required arguments:
            suffix -- str: Document type suffix.
        """
        self._ui.restore_status()
        self._ui.propertiesView.apply_changes()
        if self._mdl.prjFile.filePath is not None or self.save_project():
            if self._mdl.isModified:
                if self._ui.ask_yes_no(_('Save changes?')):
                    self.save_project()
                else:
                    # Do not export a document from an unsaved project.
                    return

            exporter = NvDocExporter(self._ui)
            try:
                self._ui.set_status(exporter.run(self._mdl.prjFile, suffix, **kwargs))
            except Error as ex:
                self._ui.set_status(f'!{str(ex)}')

    def get_preferences(self):
        """Return the global preferences dictionary."""
        return prefs

    def import_md(self, event=None, sourcePath=None, defaultExtension='.md'):
        """Update or create the project from a Marksown-formatted document.
        
        Optional arguments:
            sourcePath: str -- Path specifying the source document. If None, a file picker is used.
            defaultExtension: str -- Extension to be preset in the file picker.
        """
        if sourcePath is None:
            if prefs['last_open']:
                startDir, __ = os.path.split(prefs['last_open'])
            else:
                startDir = '.'
            sourcePath = filedialog.askopenfilename(
                filetypes=self.importFiletypes,
                defaultextension=defaultExtension,
                initialdir=startDir,
                )
            if not sourcePath:
                return 'break'

        if self._mdl.prjFile is not None:
            self.show_status()
            self.refresh_views()
            if self._mdl.isModified:
                if self._ui.ask_yes_no(_('Save changes?')):
                    self.save_project()
        importer = NvDocImporter(self._ui)
        try:
            message = importer.run(sourcePath, nv_service=self._mdl.nvService)
        except Error as ex:
            self._ui.set_status(f'!{str(ex)}')
            return 'break'

        if importer.newFile:
            self.open_project(filePath=importer.newFile)
            if os.path.isfile(sourcePath) and prefs['import_mode'] == '1':
                os.replace(sourcePath, f'{sourcePath}.bak')
                message = f'{message} - {_("Source document deleted")}.'
            self._ui.set_status(message)
        return 'break'

    def join_sections(self, event=None, scId0=None, scId1=None):
        """Join section 0 with section 1.

        Optional arguments:
            scId0: str -- ID of the section to be extended
            scId1: str -- ID of the section to be discarded.
            
        If not both arguments are given, determine them from the tree selection.
        """
        if scId0 is None or scId1 is None:
            try:
                scId1 = self._ui.tv.tree.selection()[0]
            except:
                return

            if not scId1.startswith(SECTION_PREFIX):
                return

            scId0 = self._ui.tv.prev_node(scId1)
            if not scId0:
                self._ui.show_error(_('There is no previous section'), title=_('Cannot join sections'))
                return

        if self._ui.ask_yes_no(f'{_("Join with previous")}?'):
            try:
                self._mdl.join_sections(scId0, scId1)
            except Error as ex:
                self._ui.show_error(str(ex), title=_('Cannot join sections'))
                return

            self._view_new_element(scId0)

    def move_node(self, node, targetNode):
        """Move a node to another position.
        
        Positional arguments:
            node: str - ID of the node to move.
            targetNode: str -- ID of the new parent/predecessor of the node.
        """
        if (node.startswith(SECTION_PREFIX) and targetNode.startswith(CHAPTER_PREFIX)
            ) or (node.startswith(PLOT_POINT_PREFIX) and targetNode.startswith(PLOT_LINE_PREFIX)):
            self._ui.tv.open_children(targetNode)
        self._ui.tv.skipUpdate = True
        self._mdl.move_node(node, targetNode)

    def new_project(self, event=None):
        """Create a mdnovel project instance."""
        if self._mdl.prjFile is not None:
            self.close_project()
        self._mdl.new_project(self._ui.tv.tree)
        self._ui.show_path(_('Unnamed'))
        # setting the path bar
        self.enable_menu()
        self.show_status()
        # setting the status bar
        self._ui.tv.go_to_node(CH_ROOT)
        self.refresh_views()
        self.save_project()
        return 'break'

    def on_quit(self, event=None):
        """Save changes and keyword arguments before exiting the program.
        
        Extends the superclass method.
        """
        try:
            if self._mdl.prjFile is not None:
                self.close_project()
            super().on_quit()
        except Exception as ex:
            self._ui.show_error(str(ex), title='ERROR: Unhandled exception on exit')
            self._ui.root.quit()
        return 'break'

    def open_installationFolder(self, event=None):
        """Open the installation folder with the OS file manager."""
        installDir = os.path.dirname(sys.argv[0])
        try:
            os.startfile(norm_path(installDir))
            # Windows
        except:
            try:
                os.system('xdg-open "%s"' % norm_path(installDir))
                # Linux
            except:
                try:
                    os.system('open "%s"' % norm_path(installDir))
                    # Mac
                except:
                    pass
        return 'break'

    def open_link(self, element, linkIndex):
        """Open a linked file.
        
        Positional arguments:
            element: BasicElement or subclass.
            linkIndex: int -- Index of the link to open.
            
        First try to open the link using its relative path.
        If this fails, try to open it using the "full" path. 
        On success, fix the link. 
        Otherwise, show an error message. 
        """
        linkPath = list(element.links)[linkIndex]
        fullPath = element.links[linkPath]
        try:
            self.linkProcessor.open_link(linkPath, self.launchers)
            # using the relative path
        except:

            # The relative link seems to be broken. Try the full path.
            if fullPath is not None:
                newPath = self.linkProcessor.shorten_path(fullPath)
            else:
                newPath = ''
            # fixing the link using the full path
            try:
                self.linkProcessor.open_link(newPath, self.launchers)
            except Exception as ex:

                # The full path is also broken.
                self._ui.show_error(
                    str(ex),
                    title=_('Cannot open link')
                    )
            else:
                # Replace the broken link with the fixed one.
                links = element.links
                del links[linkPath]
                links[newPath] = fullPath
                element.links = links
                self._ui.set_status(_('Broken link fixed'))
        else:
            # Relative path is o.k. -- now check the full path.
            pathOk = self.linkProcessor.expand_path(linkPath)
            if fullPath != pathOk:
                # Replace the broken full path.
                links = element.links
                links[linkPath] = pathOk
                element.links = links
                self._ui.set_status(_('Broken link fixed'))

    def open_project(self, event=None, filePath='', doNotSave=False):
        """Create a mdnovel project instance and read the file.
        
        Optional arguments:
            filePath: str -- The new project's file name.
        
        If no file name is given, a file picker is opened.
        Display project title, description and status.
        Return True on success, otherwise return False.
        """
        self._ui.restore_status()
        filePath = self.select_project(filePath)
        if not filePath:
            return False

        prefs['last_open'] = filePath

        if self._mdl.prjFile is not None:
            self.close_project(doNotSave=doNotSave)
        try:
            self._mdl.open_project(filePath)
        except Error as ex:
            self.close_project(doNotSave=doNotSave)
            self._ui.set_status(f'!{str(ex)}')
            return False

        self._ui.show_path(f'{norm_path(self._mdl.prjFile.filePath)}')
        self.enable_menu()

        self.refresh_views()
        self._ui.show_path(_('{0} (last saved on {1})').format(norm_path(self._mdl.prjFile.filePath), self._mdl.prjFile.fileDate))
        self.show_status()
        self._ui.contentsView.view_text()
        self._ui.tv.show_branch(CH_ROOT)
        return True

    def open_project_folder(self, event=None):
        """Open the project folder with the OS file manager."""
        if not self.save_project():
            if not self._mdl:
                return

            if not self._mdl.prjFile:
                return

            if self._mdl.prjFile.filePath is None:
                return

        projectDir, __ = os.path.split(self._mdl.prjFile.filePath)
        try:
            os.startfile(norm_path(projectDir))
            # Windows
        except:
            try:
                os.system('xdg-open "%s"' % norm_path(projectDir))
                # Linux
            except:
                try:
                    os.system('open "%s"' % norm_path(projectDir))
                    # Mac
                except:
                    pass
        return 'break'

    def refresh(self):
        """Callback function to report model element modifications.
        
        Overrides the superclass method.
        """
        self.show_status()

    def refresh_views(self, event=None):
        """Update all registered views."""
        self._ui.propertiesView.apply_changes()
        self._mdl.renumber_chapters()
        self._mdl.prjFile.adjust_section_types()
        self._mdl.novel.update_plot_lines()
        self._ui.refresh()
        return 'break'

    def reload_project(self, event=None):
        """Discard changes and reload the project."""
        if self._mdl.prjFile is None:
            return 'break'

        if self._mdl.isModified and not self._ui.ask_yes_no(_('Discard changes and reload the project?')):
            return 'break'

        if self._mdl.prjFile.has_changed_on_disk() and not self._ui.ask_yes_no(_('File has changed on disk. Reload anyway?')):
            return 'break'

        # this is to avoid saving when closing the project
        if self.open_project(filePath=self._mdl.prjFile.filePath, doNotSave=True):
            # includes closing
            self._ui.set_status(_('Project successfully restored from disk.'))
        return 'break'

    def reset_tree(self, event=None):
        """Clear the displayed tree, and reset the browsing history."""
        self._mdl.reset_tree()

    def restore_backup(self, event=None):
        """Discard changes and restore the latest backup file."""
        if self._mdl.prjFile is None:
            return 'break'

        latestBackup = f'{self._mdl.prjFile.filePath}.bak'
        if not os.path.isfile(latestBackup):
            self._ui.set_status(f'!{_("No backup available")}')
            return 'break'

        if self._mdl.isModified:
            if not self._ui.ask_yes_no(_('Discard changes and restore the latest backup?')):
                return 'break'

        elif not self._ui.ask_yes_no(_('Restore the latest backup?')):
            return 'break'

        try:
            os.replace(latestBackup, self._mdl.prjFile.filePath)
        except Exception as ex:
            self._ui.set_status(str(ex))
        else:
            if self.open_project(filePath=self._mdl.prjFile.filePath, doNotSave=True):
                # Includes closing
                self._ui.set_status(_('Latest backup successfully restored.'))
        return 'break'

    def save_as(self, event=None):
        """Rename the project file and save it to disk.
        
        Return True on success, otherwise return False.
        """
        if self._mdl.prjFile is None:
            return False

        if prefs['last_open']:
            startDir, __ = os.path.split(prefs['last_open'])
        else:
            startDir = '.'
        fileName = filedialog.asksaveasfilename(
            filetypes=self._fileTypes,
            defaultextension=self._fileTypes[0][1],
            initialdir=startDir,
            )
        if fileName:
            if self._mdl.prjFile is not None:
                self._ui.propertiesView.apply_changes()
                try:
                    self._mdl.save_project(fileName)
                except Error as ex:
                    self._ui.set_status(f'!{str(ex)}')
                else:
                    self._ui.show_path(f'{norm_path(self._mdl.prjFile.filePath)} ({_("last saved on")} {self._mdl.prjFile.fileDate})')
                    self._ui.restore_status()
                    prefs['last_open'] = self._mdl.prjFile.filePath
                    return True

        return False

    def save_project(self, event=None):
        """Save the mdnovel project to disk.
        
        Return True on success, otherwise return False.
        """
        if self._mdl.prjFile is None:
            return False

        if self._mdl.prjFile.filePath is None:
            return self.save_as()

        if self._mdl.prjFile.has_changed_on_disk() and not self._ui.ask_yes_no(_('File has changed on disk. Save anyway?')):
            return False

        self._ui.propertiesView.apply_changes()
        try:
            self._mdl.save_project()
        except Error as ex:
            self._ui.set_status(f'!{str(ex)}')
            return False

        self._ui.show_path(f'{norm_path(self._mdl.prjFile.filePath)} ({_("last saved on")} {self._mdl.prjFile.fileDate})')
        self._ui.restore_status()
        prefs['last_open'] = self._mdl.prjFile.filePath
        return True

    def select_project(self, fileName):
        """Return a project file path.

        Positional arguments:
            fileName: str -- project file path.
            
        Optional arguments:
            fileTypes -- list of tuples for file selection (display text, extension).

        Priority:
        1. use file name argument
        2. open file select dialog

        On error, return an empty string.
        """
        initDir = os.path.dirname(prefs.get('last_open', ''))
        if not initDir:
            initDir = './'
        if not fileName or not os.path.isfile(fileName):
            fileName = filedialog.askopenfilename(
                filetypes=self._fileTypes,
                defaultextension=NvWorkFile.EXTENSION,
                initialdir=initDir
                )
        if not fileName:
            return ''

        return fileName

    def set_character_status(self, isMajor, elemIds=None):
        """Set character status to Major.
        
        Optional arguments:
            isMajor: bool -- If True, make the characters major. Otherwise, make them minor.
            elemIds: list of character IDs to process.
        """
        if elemIds is None:
            try:
                elemIds = self._ui.tv.tree.selection()
            except:
                return

        self._ui.tv.open_children(CR_ROOT)
        self._mdl.set_character_status(isMajor, elemIds)

    def set_level(self, newLevel, elemIds=None):
        """Set chapter or stage level.
        
        Positional arguments:
            newLevel: int -- New level to be set.
            elemIds: list of IDs to process.
        """
        if elemIds is None:
            try:
                elemIds = self._ui.tv.tree.selection()
            except:
                return

        self._mdl.set_level(newLevel, elemIds)

    def set_completion_status(self, newStatus, elemIds=None):
        """Set section completion status (Outline/Draft..).
        
        Positional arguments:
            newStatus: int -- New section status to be set.        
            elemIds: list of IDs to process.            
        """
        if elemIds is None:
            try:
                elemIds = self._ui.tv.tree.selection()
            except:
                return

        self._ui.tv.open_children(elemIds[0])
        self._mdl.set_completion_status(newStatus, elemIds)

    def set_type(self, newType, elemIds=None):
        """Set section or chapter type Normal).
        
        Positional arguments:
            newType: int -- New type to be set.
            elemIds: list of IDs to process.
        """
        if elemIds is None:
            try:
                elemIds = self._ui.tv.tree.selection()
            except:
                return

        self._ui.tv.open_children(elemIds[0])
        self._mdl.set_type(newType, elemIds)

    def show_report(self, suffix):
        """Create HTML report for the web browser.
        
        Positional arguments:
            suffix: str -- the HTML file name suffix, indicating the report type.        
        """
        if self._mdl.prjFile.filePath is None:
            return False

        self._ui.restore_status()
        self._ui.propertiesView.apply_changes()
        reporter = NvHtmlReporter()
        try:
            reporter.run(self._mdl.prjFile, suffix, tempdir=self.tempDir)
        except Error as ex:
            self._ui.set_status(f'!{str(ex)}')

    def show_status(self, message=None):
        """Display project statistics at the status bar.
        
        Optional arguments:
            message: str -- Message to be displayed instead of the statistics.
        """
        if self._mdl.novel is not None and not message:
            wordCount, sectionCount, chapterCount, partCount = self._mdl.get_counts()
            message = _('{0} parts, {1} chapters, {2} sections, {3} words').format(partCount, chapterCount, sectionCount, wordCount)
            self.wordCount = wordCount
        self._ui.show_status(message)

    def _view_new_element(self, newNode):
        """View the element with ID newNode.
        
        - Open the properties window for the new element.
        - Show and select it in the tree view.
        - Prepare the current element's title entry for manual input.
        The order is mandatory for smooth operation.
        """
        if newNode:
            self._ui.tv.go_to_node(newNode)
            self._ui.propertiesView.show_properties(newNode)
            self._ui.propertiesView.focus_title()
        else:
            self._ui.set_status(f'!{_("Cannot create the element at this position")}.')

