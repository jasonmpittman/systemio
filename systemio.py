#!/usr/bin/env python3

"""systemio.py: Systemio reads the specified PDF and returns the keywords from the metadata along with a frequency of appearance in the PDF"""

import sys

import argparse
import pdfreader
from pdfreader import PDFDocument, SimplePDFViewer

__author__ = "Jason M. Pittman"
__copyright__ = "Copyright 2021, Jason M. Pittman"
__credits__ = ["Jason M. Pittman, Reilly Kobbe, Taylor Lynch"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Jason M. Pittman"
__email__ = "jason.pittman@umgc.edu"
__status__ = "Development"

"""
    operational functions for structural bibliometric keyword analysis
"""

def load_pdf(file):
    fd = open(file, "rb")
    pdf = PDFDocument(fd)

    return pdf

def get_page_count(pdf):
    pages = [p for p in pdf.pages()]
    
    return len(pages)

def list_metadata_keywords(pdf):
    return pdf.metadata['Keywords']

def list_paper_keywords():
    pass

def analyze_paper(file, page_count):
    fd = open(file, "rb")
    pdf = SimplePDFViewer(fd)

    for i in range(1, page_count):
        pdf.navigate(i)
        pdf.render()
        print(pdf.canvas.strings)

def main():
    parser = argparse.ArgumentParser(description='Analyze a PDF for keyword structural bibliometrics')
    parser.add_argument('file', help='the file or file path to the PDF', nargs=1, action="store") 
    
    args = parser.parse_args()

    if args.file:
        pdf = load_pdf(args.file[0])
        
        keywords = list_metadata_keywords(pdf)
        print(keywords)

        page_count = get_page_count(pdf)
        print(page_count)
        
        analyze_paper(args.file[0], page_count)
    else:
        print(parser.print_help())

if __name__ == '__main__':
    main()