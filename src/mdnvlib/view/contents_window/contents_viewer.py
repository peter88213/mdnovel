"""Provide a tkinter text box class for "contents" viewing.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import re

from mdnvlib.novx_globals import CH_ROOT
from mdnvlib.novx_globals import _
from mdnvlib.nv_globals import prefs
from mdnvlib.view.contents_window.rich_text_nv import RichTextNv
import tkinter as tk
from apptk.view.view_component_base import ViewComponentBase


class ContentsViewer(ViewComponentBase, RichTextNv):
    """A tkinter text box class for mdnovel file viewing.
    
    Show the novel contents in a text box.
    """
    NO_TEXT = re.compile(r'\<note\>.*?\<\/note\>|\<comment\>.*?\<\/comment\>|\<.+?\>')

    def __init__(self, parent, model, view, controller):
        """Put a text box to the specified window.
        
        Positional arguments:
            parent: tk.Frame -- The parent window.
            model -- reference to the main model instance of the application.
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.
        
        Required keyword arguments:
            show_markup: bool 
        """
        ViewComponentBase.__init__(self, model, view, controller)
        RichTextNv.__init__(self, parent, **prefs)
        self.pack(expand=True, fill='both')
        self.showMarkup = tk.BooleanVar(parent, value=prefs['show_markdown'])
        # ttk.Checkbutton(parent, text=_('Show Markdown'), variable=self.showMarkup).pack(anchor='w')
        self.showMarkup.trace('w', self.refresh)
        self._textMarks = {}
        self._index = '1.0'
        self._parent = parent

    def reset_view(self):
        """Clear the text box."""
        self.config(state='normal')
        self.delete('1.0', 'end')
        self.config(state='disabled')

    def see(self, idStr):
        """Scroll the text to the position of the idStr node.
        
        Positional arguments:
            idStr: str -- Chapter or section node (tree selection).
        """
        try:
            self._index = self._textMarks[idStr]
            super().see(self._index)
        except KeyError:
            pass

    def refresh(self, event=None, *args):
        """Reload the text to view."""
        if self._mdl.prjFile is None:
            return

        if self._parent.winfo_manager():
            self.view_text()
            try:
                super().see(self._index)
            except KeyError:
                pass

    def view_text(self):
        """Build a list of "tagged text" tuples and send it to the text box."""

        # Build a list of (text, tag) tuples for the whole book.
        taggedText = []
        for chId in self._mdl.novel.tree.get_children(CH_ROOT):
            chapter = self._mdl.novel.chapters[chId]
            taggedText.append(chId)
            # inserting a chapter mark
            if chapter.chLevel == 2:
                if chapter.chType == 0:
                    headingTag = self.H2_TAG
                else:
                    headingTag = self.H2_UNUSED_TAG
            else:
                if chapter.chType == 0:
                    headingTag = self.H1_TAG
                else:
                    headingTag = self.H1_UNUSED_TAG
            if chapter.title:
                heading = f'{chapter.title}\n'
            else:
                    heading = f"[{_('Unnamed')}]\n"
            taggedText.append((heading, headingTag))

            for scId in self._mdl.novel.tree.get_children(chId):
                section = self._mdl.novel.sections[scId]
                taggedText.append(scId)
                # inserting a section mark
                textTag = ''
                if section.scType == 3:
                    headingTag = self.STAGE2_TAG
                elif section.scType == 2:
                    headingTag = self.STAGE1_TAG
                elif section.scType == 0:
                    headingTag = self.H3_TAG
                else:
                    headingTag = self.H3_UNUSED_TAG
                    textTag = self.UNUSED_TAG
                if section.title:
                    heading = f'[{section.title}]\n'
                else:
                    heading = f"[{_('Unnamed')}]\n"
                taggedText.append((heading, headingTag))

                if section.sectionContent:
                    taggedText.append((section.sectionContent, textTag))

        if not taggedText:
            taggedText.append((f'({_("No text available")})', self.ITALIC_TAG))
        self._textMarks = {}

        # Clear the text box first.
        self.config(state='normal')
        self.delete('1.0', 'end')

        # Send the (text, tag) tuples to the text box.
        for entry in taggedText:
            if len(entry) == 2:
                # entry is a regular (text, tag) tuple.
                text, tag = entry
                self.insert('end', text, tag)
            else:
                # entry is a mark to insert.
                index = f"{self.count('1.0', 'end', 'lines')[0]}.0"
                self._textMarks[entry] = index
        self.config(state='disabled')

