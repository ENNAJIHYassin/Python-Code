# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 12:57:45 2017

@author: princ
"""

'''Coonecting'''
#reading an html file content
from urllib.request import urlopen

html = urlopen("http://pythonscraping.com/pages/page1.html") #request the webpage adress
print(html.read()) #print the HTML content of the page as it is




'''Beautiful Soup'''
#reading an html file content with beautifulsoup
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

html = urlopen("http://pythonscraping.com/pages/page1.html")
bs4Obj = bs(html.read())
print(bs4Obj) #print the whole HTML content of the page, transformed into an BeautifulSoup object
print(bs4Obj.h1) #print the content of the BS object tagged 'h1'
print(bs4Obj.html.body.h1) #same as before
print(bs4Obj.body.h1) #same as before
print(bs4Obj.html.h1) #same as before
"""this shows how convenient beautiful soup is at fetching data (no need for multiple layers)"""




'''Connecting Reliably'''
from urllib.request import urlopen, HTTPError
from bs4 import BeautifulSoup

#define a function that gets titles
def getTitle(url):
    try:
        html = urlopen(url)  #try reading the url
    except HTTPError as e:
        return None  #return a "none" object if there was a problem with the server/page
    try:
        bsObj = BeautifulSoup(html.read())  #try creating bs object
        title = bsObj.h1                    #try fetching the title
    except AttributeError as e:
        return None  #return a "none" object if there was a problem with the tag
    return title  #else return the title

title = getTitle("http://pythonscraping.com/pages/page1.html")
if title == None:
    print('Title could not be found')
else:
    print('The Title is:', title)