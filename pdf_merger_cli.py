#! /usr/bin/python2.7

from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import os
import os.path
import sys
import argparse


def get_files(path='.', max_depth=2, ext_filter=('.*')):
    """Get files from path"""
    full_path = os.path.abspath(path)
    depth = 0
    return dive_into_path(full_path, set(ext_filter), depth, max_depth)


def dive_into_path(path, ext_filter, depth, max_depth):
    """Dive into path"""
    if depth >= max_depth:
        return []

    file_list = []
    for f in os.listdir(path):
        if f.startswith('.'):
            # ignore hidden files and folders and . and ..
            continue
        fullf = os.path.join(path,f)
        if os.path.isfile(fullf):
            if ('.*' in ext_filter) or (os.path.splitext(f)[-1] in ext_filter):
                file_list.append(fullf)
        else:
            file_list += dive_into_path(fullf, ext_filter, depth + 1, max_depth)
    return file_list


def get_student_name(fname):
    """Get student name"""
    file_parts = fname.split('/')
    for part in file_parts:
        if part.find(',') != -1:
            return part.split('(')[0]
    return ""


def merge_pdfs(pdfs, outline_filename='outline.txt', outname='document-merged.pdf'):
    """Merge PDFs"""
    if len(pdfs) > 0:
        page_num = 1
        content = ''
        # return open(filename, 'r')
        merger = PdfFileMerger()
        for f in pdfs:
            merger.append(PdfFileReader(file(f, 'rb')))
            name = get_student_name(f)
            content += name + ' ' + '-'*10 + ' ' + str(page_num) + '\n'

        merger.write(outname)
        if outline_filename is not None:
            with open(outline_filename, 'w') as fp:
                fp.write(content)


def helper(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', type=str, action='store', help='where to fetch files (default: current)', default=os.path.realpath(__file__))
    parser.add_argument('-D', '--depth',type=int, action='store', help='maximum depth to fetch (default: 4)', default=4)
    parser.add_argument('-o', '--output', type=str, action='store', help='output filename (default: merged.pdf)', default='merged.pdf')

    return parser.parse_args(arguments)


if __name__ == '__main__':
    args = helper(sys.argv[1:])
    pdfs = get_files(path=args.directory, max_depth=args.depth, ext_filter=('.pdf'))
    merge_pdfs(pdfs=pdfs, outname=args.output)




