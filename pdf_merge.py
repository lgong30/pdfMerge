from PyPDF2 import PdfFileMerger, PdfFileReader

def merge(file_list, output="document-merged.pdf"):
    # open file on your own
    if not output:
        output = "document-merged.pdf"
    elif not output.endswith(".pdf"):
        output += ".pdf"

    if len(file_list) > 0:
        # return open(filename, 'r')
        merger = PdfFileMerger()
        for f in file_list:
            merger.append(PdfFileReader(file(f, 'rb')))
        merger.write(output)