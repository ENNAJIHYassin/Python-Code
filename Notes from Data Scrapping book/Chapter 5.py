# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 13:48:58 2017

@author: princ
"""

'''Media files'''
#Download the logo of the website
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import os

html = urlopen("http://www.pythonscraping.com/")
bsObj = BeautifulSoup(html)
logo_img_url = bsObj.find("a", {"id":"logo"}).find("img")["src"]
urlretrieve(logo_img_url, "logo.jpg")

#download all internal files, linked to by any tag’s src
#attribute, from the home page of http://pythonscraping.com
downloadDirectory = "downloaded"
baseUrl = "http://pythonscraping.com"

def getAbsoluteURL(baseUrl, source):
    if source.startswith("http://www."):
        url = "http://"+source[11:]
    elif source.startswith("http://"):
        url = source
    elif source.startswith("www."):
        url = source[4:]
        url = "http://"+source
    else:
        url = baseUrl+"/"+source
    if baseUrl not in url:
        return None
    return url

def getDownloadPath(baseUrl, absoluteUrl, downloadDirectory):
    path = absoluteUrl.replace("www.", "")
    path = path.replace(baseUrl, "")
    path = downloadDirectory+path
    path_parts = path.split("/") 
    normal_path_parts =[]
    for part in path_parts:
        normal_path_parts.append(''.join(e for e in part if e.isalnum()))
    normal_path = '/'.join(e for e in normal_path_parts)
    directory = os.path.dirname(normal_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return normal_path

html = urlopen("http://www.pythonscraping.com")
bsObj = BeautifulSoup(html)
downloadList = bsObj.findAll(src=True)

for download in downloadList:
    fileUrl = getAbsoluteURL(baseUrl, download["src"])
    if fileUrl is not None:
        print(fileUrl)
        urlretrieve(fileUrl, getDownloadPath(baseUrl, fileUrl, downloadDirectory))
        
'''Storing data to CSV'''
import csv

csvFile = open("test.csv", 'w+')

try:
    fileWriter = csv.writer(csvFile)
    fileWriter.writerow(("n","n+2","n*2"))
    for i in range(10):
        fileWriter.writerow((i, i+2, i*2))
finally:
    csvFile.close()
    
#importing a table from a wikipedia page into a csv file
html = urlopen("http://en.wikipedia.org/wiki/Comparison_of_text_editors")
bsObj = BeautifulSoup(html)

#The main comparison table is currently the first table on the page
table = bsObj.findAll("table",{"class":"wikitable"})[0]
rows = table.findAll("tr")

csvFile = open("editor.csv", 'wt')
writer = csv.writer(csvFile)
try:
    for row in rows:
        csvRow = []
        for cell in row.findAll(['td', 'th']):
            csvRow.append(cell.get_text())
        writer.writerow(csvRow)
finally:
    csvFile.close()
    
'''MySQL'''
#connect to a MySQL database through python
import pymysql

conn = pymysql.connect(host='127.0.0.1',
                       user ='root', passwd="YASSOUNe11", db='mysql')

cur = conn.cursor()
cur.execute("USE scraping")
cur.execute("SELECT * FROM pages WHERE id=1")
print(cur.fetchone())
cur.close()
conn.close()

#Insert scraped wikipedia table into MySQL with python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import pymysql
import re

conn = pymysql.connect(host='127.0.0.1',
                       user='root', passwd="YASSOUNe11", db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("USE scraping")

random.seed(datetime.datetime.now())

def store(title, content):
    cur.execute("INSERT INTO pages (title, content) VALUES (%s,%s)", (title, content))
    cur.connection.commit()
    
def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html)
    title = bsObj.find("h1").get_text()
    content = bsObj.find("div", {"id":"mw-content-text"}).find("p").get_text()
    store(title, content)
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a",
                     href=re.compile("^(/wiki/)((?!:).)*$"))
    
links = getLinks("/wiki/Kevin_Bacon")

try:
    while len(links) > 0:
        newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
        print(newArticle)
        links = getLinks(newArticle)
finally:
    cur.close()
    conn.close()

'''DATABASE TECHNIQUES AND GOOD PRACTICES'''
#calculate the 'Bacon Number'
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import pymysql
import re

conn = pymysql.connect(host='127.0.0.1',
                       user='root', passwd="YASSOUNe11", db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("USE wikipedia")

def insertPageIfNotExists(url):
    cur.execute("SELECT * FROM pages WHERE url = %s", (url))
    if cur.rowcount == 0:
        cur.execute("INSERT INTO pages (url) VALUES (%s)", (url))
        conn.commit()
        return cur.lastrowid
    else:
        return cur.fetchone()[0]
    
def insertLink(fromPageId, toPageId):
    cur.execute("SELECT * FROM links WHERE fromPage = %s AND toPage = %s",
                (int(fromPageId), int(toPageId)))
    if cur.rowcount == 0:
        cur.execute("INSERT INTO links (fromPage, toPage) VALUES (%s, %s)",
                    (int(fromPageId), int(toPageId)))
        conn.commit()

pages = set()

def getLinks(pageUrl, recursionLevel):
    global pages
    if recursionLevel > 4:
        return;
    pageId = insertPageIfNotExists(pageUrl)
    html = urlopen("http://en.wikipedia.org"+pageUrl)
    bsObj = BeautifulSoup(html)
    for link in bsObj.findAll("a",
                              href=re.compile("^(/wiki/)((?!:).)*$")):
        insertLink(pageId,
                   insertPageIfNotExists(link.attrs['href']))
        if link.attrs['href'] not in pages:
            #We have encountered a new page, add it and search it for links
            newPage = link.attrs['href']
            pages.add(newPage)
            getLinks(newPage, recursionLevel+1)
            
getLinks("/wiki/Kevin_Bacon", 0)
cur.close()
conn.close()

        



































