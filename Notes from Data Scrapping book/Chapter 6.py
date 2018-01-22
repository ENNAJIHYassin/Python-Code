# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 14:42:26 2017

@author: princ
"""


'''Text files'''
#reading russiann and french in as ASCII
from urllib.request import urlopen
textPage = urlopen("http://www.pythonscraping.com/pages/warandpeace/chapter1-ru.txt")
print(textPage.read())

#reading it at UTF-8
from urllib.request import urlopen
textPage = urlopen("http://www.pythonscraping.com/pages/warandpeace/chapter1-ru.txt")
print(str(textPage.read()), "utf-8" )

#encode bsobj content into UTF-8
from bs4 import BeautifulSoup
html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
bsObj = BeautifulSoup(html)
content = bsObj.find("div", {"id":"mw-content-text"}).get_text()
content = bytes(content, "UTF-8")
content = content.decode("UTF-8")

'''CSV'''
#read csv file in memory from internet without storing in the hdd
from urllib.request import urlopen
from io import StringIO
import csv

data = urlopen("http://pythonscraping.com/files/MontyPythonAlbums.csv").read().decode('ascii', 'ignore')
dataFile = StringIO(data)
csvReader = csv.reader(dataFile)
for row in csvReader:
    print(row)

#same thing but with dictionary instead to account for the header
from urllib.request import urlopen
from io import StringIO
import csv

data = urlopen("http://pythonscraping.com/files/MontyPythonAlbums.csv").read().decode('ascii', 'ignore')
dataFile = StringIO(data)
dictReader = csv.DictReader(dataFile)

print(dictReader.fieldnames)

for row in dictReader:
    print(row)

'''PDF'''
#Read arbitrary PDFs to a string
from urllib.request import urlopen
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
#incase of a localy PDf file, use open instead of urlopen
#   from io import open

def readPDF(pdfFile):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    process_pdf(rsrcmgr, device, pdfFile)
    device.close()
    
    content = retstr.getvalue()
    retstr.close()
    return content

pdfFile = urlopen("http://pythonscraping.com/pages/warandpeace/chapter1.pdf")
outputString = readPDF(pdfFile)
print(outputString)
pdfFile.close()

'''Docsx'''
#reading a docx file from the web
from zipfile import ZipFile
from urllib.request import urlopen
from io import BytesIO
from bs4 import BeautifulSoup

wordFile = urlopen("http://pythonscraping.com/pages/AWordDocument.docx").read()
wordFile = BytesIO(wordFile)
document = ZipFile(wordFile)
xml_content = document.read('word/document.xml')
#this prints the xml unziped version of the docx
print(xml_content.decode('utf-8'))

wordObj = BeautifulSoup(xml_content.decode('utf-8'), "lxml")
textStrings = wordObj.findAll("w:t")
len(textStrings)
for textElem in textStrings:
    print(textElem)
textStrings = wordObj.findAll("w:t")
for textElem in textStrings:
    closeTag = ""
try:
    style = textElem.parent.previousSibling.find("w:pstyle")
    if style is not None and style["w:val"] == "Title":
        print("<h1>")
        closeTag = "</h1>"
except AttributeError:
#No tags to print
    pass
    print(textElem.text)
    print(closeTag)
    
    
    
    