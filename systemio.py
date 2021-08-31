#!/usr/bin/env python3

"""systemio.py: Systemio reads the specified PDF and returns the keywords from the metadata along with a frequency of appearance in the PDF"""

import sys
import re
import json
import datetime

import argparse
import pdfreader
from pdfreader import PDFDocument, SimplePDFViewer

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
import io


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
    keywords = re.split(r'[ ,;]', pdf.metadata['Keywords'].lower())

    while ('' in keywords):
        keywords.remove('') 
    
    return keywords

def list_paper_keywords():
    pass

def get_pdf_txt(file, keywords): # this is accurate but not perfect. we can be around 10 off
    keyword_frequency = {}
    
    fp = open(file, 'rb')
    rsrcmgr = PDFResourceManager()
    
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    

    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data =  retstr.getvalue()

    for keyword in keywords:
        keyword_frequency[keyword] = count_keyword(keyword, data)

    #print(keyword_frequency)
    return keyword_frequency

def analyze_paper(file, page_count, keywords): # this function does not produce accurate results
    fd = open(file, "rb")
    pdf = SimplePDFViewer(fd)

    pdf_pages = {}
    keyword_frequency = {}

    for i in range(1, page_count):
        pdf.navigate(i)
        pdf.render()
        
        temp = pdf.canvas.strings
        pdf_pages[i] = pdf.canvas.strings #[x.lower() for x in temp]

    for keyword in keywords:
        keyword_frequency[keyword] = count_keyword(keyword, pdf_pages)    

    print(keyword_frequency)

def count_keyword(keyword, pages):

    count = pages.count(keyword)

    # the loop below is for the analyze_paper function
    #for page_number, page_content in pages.items():
    #    print("Searching for {} on page {}...".format(keyword, page_number))
    #    count = page_content.count(keyword)

    return count

def write_output(filename, keyword_frequency):
    output_file = 'data/output.csv'

    #output should be: document name, keyword1, count1, keyword2, count2, ...
    with open(output_file, mode='a') as f:
        f.write('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + ',' + filename + ',' + json.dumps(keyword_frequency) + '\n')

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
        
        keyword_frequency = get_pdf_txt(args.file[0], keywords)
        print(keyword_frequency)

        write_output(args.file[0], keyword_frequency)
        #analyze_paper(args.file[0], page_count, keywords)
    else:
        print(parser.print_help())

if __name__ == '__main__':
    main()