"""Provide a tkinter widget for progress log display.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnovel
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date
from tkinter import ttk

from mdnvlib.novx_globals import _
from mdnvlib.view.platform.platform_settings import KEYS
from mdnvlib.view.platform.platform_settings import PLATFORM
import tkinter as tk


class ProgressViewer(tk.Toplevel):

    def __init__(self, manager, model):
        self._manager = manager
        self._mdl = model
        super().__init__()

        self.geometry(self._manager.kwargs['wc_win_geomety'])
        self.lift()
        self.focus()
        self.protocol("WM_DELETE_WINDOW", self.on_quit)
        if PLATFORM != 'win':
            self.bind(KEYS.QUIT_PROGRAM[0], self.on_quit)

        #--- Tree for log view.
        columns = (
            'date',
            'wordCount',
            'wordCountDelta',
            'totalWordCount',
            'totalWordCountDelta',
            'spacer',
            )
        self.tree = ttk.Treeview(self, selectmode='none', columns=columns)
        scrollY = ttk.Scrollbar(self.tree, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollY.set)
        scrollY.pack(side='right', fill='y')
        self.tree.pack(fill='both', expand=True)
        self.tree.heading('date', text=_('Date'))
        self.tree.heading('wordCount', text=_('Words total'))
        self.tree.heading('wordCountDelta', text=_('Daily'))
        self.tree.heading('totalWordCount', text=_('With unused'))
        self.tree.heading('totalWordCountDelta', text=_('Daily'))
        self.tree.column('#0', width=0)
        self.tree.column('date', anchor='center', width=self._manager.kwargs['wc_date_width'], stretch=False)
        self.tree.column('wordCount', anchor='center', width=self._manager.kwargs['wc_wordcount_width'], stretch=False)
        self.tree.column('wordCountDelta', anchor='center', width=self._manager.kwargs['wc_wordcount_delta_width'], stretch=False)
        self.tree.column('totalWordCount', anchor='center', width=self._manager.kwargs['wc_totalcount_width'], stretch=False)
        self.tree.column('totalWordCountDelta', anchor='center', width=self._manager.kwargs['wc_totalcount_delta_width'], stretch=False)

        self.tree.tag_configure('positive', foreground='black')
        self.tree.tag_configure('negative', foreground='red')
        self.isOpen = True
        self.build_tree()

        # "Close" button.
        ttk.Button(self, text=_('Close'), command=self.on_quit).pack(side='right', padx=5, pady=5)

    def build_tree(self):
        self.reset_tree()
        wcLog = {}

        # Copy the read-in word count log.
        for wcDate in self._mdl.prjFile.wcLog:
            sessionDate = date.fromisoformat(wcDate).strftime('%x')
            wcLog[sessionDate] = self._mdl.prjFile.wcLog[wcDate]

        # Add the word count determined when opening the project.
        for wcDate in self._mdl.prjFile.wcLogUpdate:
            sessionDate = date.fromisoformat(wcDate).strftime('%x')
            wcLog[sessionDate] = self._mdl.prjFile.wcLogUpdate[wcDate]

        # Add the actual word count.
        newCountInt, newTotalCountInt = self._mdl.prjFile.count_words()
        newCount = str(newCountInt)
        newTotalCount = str(newTotalCountInt)
        today = date.today().strftime('%x')
        wcLog[today] = [newCount, newTotalCount]

        lastCount = 0
        lastTotalCount = 0
        for wc in wcLog:
            columns = []
            nodeTags = ()
            countInt = int(wcLog[wc][0])
            countDiffInt = countInt - lastCount
            totalCountInt = int(wcLog[wc][1])
            totalCountDiffInt = totalCountInt - lastTotalCount
            if countDiffInt == 0 and totalCountDiffInt == 0:
                continue

            if countDiffInt > 0:
                nodeTags = ('positive')
            else:
                nodeTags = ('negative')
            columns = [
                wc,
                str(wcLog[wc][0]),
                str(countDiffInt),
                str(wcLog[wc][1]),
                str(totalCountDiffInt),
                ]
            lastCount = countInt
            lastTotalCount = totalCountInt
            # startIndex = 'end'
            # chronological order
            startIndex = '0'
            # reverse order
            self.tree.insert('', startIndex, iid=wc, values=columns, tags=nodeTags, open=True)

    def on_quit(self, event=None):
        self._manager.kwargs['wc_win_geomety'] = self.winfo_geometry()
        self._manager.kwargs['wc_date_width'] = self.tree.column('date', 'width')
        self._manager.kwargs['wc_wordcount_width'] = self.tree.column('wordCount', 'width')
        self._manager.kwargs['wc_wordcount_delta_width'] = self.tree.column('wordCountDelta', 'width')
        self._manager.kwargs['wc_totalcount_width'] = self.tree.column('totalWordCount', 'width')
        self._manager.kwargs['wc_totalcount_delta_width'] = self.tree.column('totalWordCountDelta', 'width')
        self.destroy()
        self.isOpen = False

    def reset_tree(self):
        """Clear the displayed tree."""
        for child in self.tree.get_children(''):
            self.tree.delete(child)

