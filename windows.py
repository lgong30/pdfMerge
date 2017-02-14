#!/usr/bin/python
#! -*- coding: utf-8 -*-

from Tkinter import *
import Tkconstants
import tkFileDialog
import os
import os.path
from pdf_merge import merge


_FONT_FAMILY = "Helvetica"
_FONT_SIZE = 14
_FONT_BOLD = (_FONT_FAMILY, _FONT_SIZE, "bold")
_FONT_NORMAL = (_FONT_FAMILY, _FONT_SIZE)



class PdfMerger(Frame):
    def __init__(self,
                 parent,
                 title="PDF Merger",
                 **kwargs):
        Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self._setUI(title)
        self.file_list = []
        self.last = -1


    def _setUI(self, title):
        if not (title is None):
            self.parent.title(title)

        num_cols = 8
        num_rows = 12

        for c in xrange(num_cols):
            self.columnconfigure(c, pad=0, minsize=98)
        for r in xrange(num_rows):
            self.rowconfigure(r, pad=0, minsize=46)

        # add buttons
        add_files_btn = Button(self,
                               text="Add Files",
                               command=self.add_from_files)
        add_files_btn.grid(row=0, column=0)
        add_directory_btn = Button(self,
                                   text="Add Directory",
                                   command=self.add_from_directory)
        add_directory_btn.grid(row=0, column=1)



        # file list
        fl_label = Label(self, text="Files to be merged", font=_FONT_BOLD ,  anchor=W)
        fl_label.grid(row=1, column=0, columnspan=num_cols, sticky=W+E+N+S)
        self.file_listbox = Listbox(self, selectmode=SINGLE)
        self.file_listbox.grid(row=2, column=0, columnspan=num_cols, rowspan=num_rows-4, sticky=W+E+N+S)

        # output
        Label(self, text="Output Filename:", font=_FONT_BOLD, anchor=W).grid(row=num_rows-2, column=0, columnspan=2, sticky=E)
        self.output_entry = StringVar()
        e = Entry(self, textvariable=self.output_entry)
        e.grid(column=2, row=num_rows - 2, columnspan=num_cols - 2, sticky=W+E+N+S)
        self.output_entry.set("document-merged")
        # other buttons
        last_row_btns = [(Button(self, text="Move Up", command=self._moveup), {"column": 0, "row": num_rows - 1}), # move up
                         (Button(self, text="Move Down", command=self._movedown), {"column": 1, "row": num_rows - 1}), # move down
                         (Button(self, text="Remove", command=self._removeitem), {"column": 2, "row": num_rows - 1}), # remove
                         (Button(self, text="Merge", command=self._merge), {"column": num_cols - 2, "row": num_rows - 1}), # merge
                         (Button(self, text="Reset", command=self._reset), {"column": num_cols - 1, "row": num_rows - 1}) # cancel
                         ]
        for btn in last_row_btns:
            btn[0].grid(**btn[1])

        self.pack()

    def add_from_files(self):
        # get filename
        options = {
            'filetypes': [('text files', '.pdf')],
            'initialdir': '.',
            'parent': self.parent
        }
        filenames = tkFileDialog.askopenfilenames(**options)
        if len(filenames) > 0:
            self._additems(filenames)

    def add_from_directory(self):
        options = {
            'initialdir': '.',
            'mustexist': False,
            'parent': self.parent
        }
        dirname = tkFileDialog.askdirectory(**options)
        filenames = []
        for f in os.listdir(dirname):
            if f.endswith('.pdf'):
                filenames.append(os.path.join(dirname,f))
        if len(filenames) > 0:
            self._additems(filenames)

    def _additems(self, new_file_list):
        try:
            new_filename_list = [os.path.splitext(os.path.split(f)[-1])[0] for f in new_file_list]
            self.file_listbox.insert(END, *new_filename_list)
        except:
            print "Insert Failed"
            return
        self.file_list += new_file_list

    def _moveup(self):
        try:
            sel_index = self.file_listbox.curselection()[0]
            content = self.file_listbox.get(sel_index)
        except:
            sel_index = -1
            content = ""

        if sel_index <= 0:
            return
        try:
            self.file_listbox.delete(sel_index)
            self.file_listbox.insert(sel_index - 1, content)
        except:
            print "MoveUp failed"
            return
        self.file_list[sel_index - 1], self.file_list[sel_index] = self.file_list[sel_index], self.file_list[sel_index - 1]

    def _movedown(self):
        try:
            sel_index = self.file_listbox.curselection()[0]
            content = self.file_listbox.get(sel_index)
        except:
            sel_index = -1
            content = ""

        if sel_index == -1 or sel_index == (len(self.file_list) - 1):
            return
        try:
            self.file_listbox.delete(sel_index)
            self.file_listbox.insert(sel_index + 1, content)
        except:
            print "MoveUp failed"
            return
        self.file_list[sel_index], self.file_list[sel_index + 1] = self.file_list[sel_index + 1], self.file_list[sel_index]

    def _removeitem(self):
        try:
            sel_index = self.file_listbox.curselection()[0]
        except:
            sel_index = -1


        if sel_index >= 0:
            try:
                self.file_listbox.delete(sel_index)
            except:
                print "Remove failed"
                return
            del self.file_list[sel_index]

    def _merge(self):
        merge(self.file_list, output=self.output_entry.get())

    def _reset(self):
        try:
            self.file_listbox.delete(0, len(self.file_list))
        except:
            print "Clear failed"
            return
        self.file_list = []




















root = Tk()
root.geometry("800x560+300+400")
frame = PdfMerger(root)
root.mainloop()
# 
# if __name__ == "__main__":
#     PdfMerger().run()