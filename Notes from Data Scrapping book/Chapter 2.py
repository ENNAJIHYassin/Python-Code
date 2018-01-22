# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 15:24:54 2017

@author: princ
"""

'''You don't always need a hammer'''

from urllib.request import urlopen, HTTPError
from bs4 import BeautifulSoup as BS

#reading the HTML content + converting to BS obj
try:
    html = urlopen("http://www.pythonscraping.com/pages/warandpeace.html")  #try reading the url
except HTTPError as e:
    print('Problem retreiving the URL') 
bsObj = BS(html)

#getting a list specefic tagnames with special tagattributes
nameList = bsObj.findAll("span", {"class":"green"})
print(nameList)

#cropping out the text
for name in nameList:
    print(name.get_text())
    #Calling .get_text() should always be the last thing you do, immediately
    #before you print, store, or manipulate your final data. In general, you 
    #should try to preserve the tag structure of a document as long as possible.




'''Another Serving of BS'''

        '''find() and findAll() with BeautifulSoup'''
#structure is :
#   findAll(tag, attributes, recursive, text, limit, keywords)
#   find(tag, attributes, recursive, text, keywords)

#return a list of all the header tags in a document
bsObj.findall({"h1","h2","h3","h4","h5"})

#return both the green and red span tags in the HTML document
bsObj.findall("span", {"class":"red", "class":"green"} )

#find the number of times “the prince” was surrounded by tags on the example page
nameList = bsObj.findAll(text ="the prince")
print(len(nameList))

#find any text in the HTML file
allText = bsObj.findAll(id="text")
print(allText[0].get_text())
'''or'''
allText = bsObj.findAll("", {"id":"text"})
print(allText[0].get_text())


        '''Other BeautifulSoup Objects'''
#NavigableString objects
    #Used to represent text within tags, rather than the tags themselves (some functions
    #operate on, and produce, NavigableStrings, rather than tag objects).
#The Comment object
    #Used to find HTML comments in comment tags, <!--like this one-->
    
        '''Navigating Trees'''
#find the first div tag in the document, then retrieve a
#list of all img tags that are descendants of that div tag
bsObj.div.findAll("img")


from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html)

'''children'''
#prints out the list of rows in the giftList table (even the title row is printed)
for child in bsObj.find("table", {"id":"giftList"}).children:
    print(child)
    
'''siblings'''
#print all rows of products from the product table, except for the first title row
for sibling in bsObj.find("table", {"id":"giftList"}).tr.next_siblings:
    print(sibling)

'''parents'''
#print out the price of the object represented by the image at the location../img/gifts/img1.jpg
print(bsObj.find("img",{"src":"../img/gifts/img1.jpg"
}).parent.previous_sibling.get_text())
    
    

    
'''Regular Expressions'''
#table in the book


'''Regular Expressions and BeautifulSoup'''
from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
import re

html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BS(html)
#matching the whole expression
images = bsObj.findAll("img", {"src":re.compile("\.\.\/img\/gifts\/img[0-9]+\.jpg")})
'''or'''
#matching the begining of the expression
images = bsObj.findAll("img", {"src":re.compile("^(\.\.\/img\/gifts\/img)")})
'''or'''
#matching the begining and the end of the expression
images = bsObj.findAll("img", {"src":re.compile("\.\./img/gifts/img.*\.jpg")})
for image in images:
    print(image["src"]) #"images" is a list of html tag lines with their attributes
                        #[<img src="../img/gifts/img1.jpg"/>,
                        #<img src="../img/gifts/img2.jpg"/>,...]

'''Accessing Attributes'''
images = []
for i in range(len(bsObj.findAll("img"))):
    images.append(bsObj.img.attrs['src'])
print(images) #"images" is a list of strings containing the attribute
              #['../img/gifts/logo.jpg',
              # '../img/gifts/logo.jpg',...]
              
'''Lambda Expressions'''
#retrieves all tags that have exactly two attributes
double_attr_tags = bsObj.findAll(lambda tag: len(tag.attrs) == 2)
print(double_attr_tags)