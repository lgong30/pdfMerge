"""
Most parts of this script are copied from Internet and 
patched together!!!
"""
import Tkinter
import Tkconstants
import tkFileDialog
from PyPDF2 import PdfFileMerger, PdfFileReader
import os
import os.path

class PDFMergerGUI(Tkinter.Frame):

    def __init__(self, root):

        Tkinter.Frame.__init__(self, root)

        # options for buttons
        button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

        # define buttons
        # Tkinter.Button(self, text='askopenfile', command=self.askopenfile).pack(**button_opt)
        Tkinter.Button(self, text='Select PDFs', command=self.askopenfilename).pack(
            **button_opt)
        Tkinter.Button(
            self, text='Select a Directory', command=self.askdirectory).pack(**button_opt)

        # define options for opening or saving a file
        self.file_opt = options = {}
        # options['defaultextension'] = '.pdf'
        options['filetypes'] = [('text files', '.pdf')]
        options['initialdir'] = '.'
        # options['initialfile'] = 'example.pdf'
        options['parent'] = root
        options['title'] = 'PyPDFMerger'

        # defining options for opening a directory
        self.dir_opt = options = {}
        options['initialdir'] = '.'
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = 'PyPDFMerger'

    def merge(self, filenames):
        # open file on your own
        if len(filenames) > 0:
            # return open(filename, 'r')
            merger = PdfFileMerger()
            for f in filenames:
                merger.append(PdfFileReader(file(f, 'rb')))
            try:
                outname = self.getfilename() + '.pdf'
            except:
                outname = "document-merged.pdf"
            merger.write(outname)        

    def askopenfilename(self):
        """Returns an opened file in read mode.
        This time the dialog just returns a filename and the file is opened by your own code.
        """
        # get filename
        filenames = tkFileDialog.askopenfilenames(**self.file_opt)
        self.merge(filenames)


    def getfilename(self):
        """Returns an opened file in write mode.
        This time the dialog just returns a filename and the file is opened by your own code.
        """

        # get filename
        return tkFileDialog.asksaveasfilename(**self.file_opt)



    def askdirectory(self):
        """Returns a selected directoryname."""

        dirname = tkFileDialog.askdirectory(**self.dir_opt)
        filenames = []
        for f in os.listdir(dirname):
            if f.endswith('.pdf'):
                filenames.append(os.path.join(dirname,f))
        self.merge(filenames)


if __name__ == '__main__':
    root = Tkinter.Tk()
    PDFMergerGUI(root).pack()
    root.mainloop()
