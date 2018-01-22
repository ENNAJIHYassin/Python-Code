# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 11:18:55 2017

@author: princ
"""

        '''Traversing a Single Domain'''
from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
import re

html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon")
bsObj = BS(html)

#getting all the links within the page
links = bsObj.findAll('a')
for link in links:
    if "href" in link.attrs:
        print(link.attrs['href'])

#getting all the links within the page that goes to other articles (not wiki options/tools)
links = bsObj.find('div', {'id':'bodyContent'}).findAll('a',{'href':re.compile("^(/wiki/)((?!:).)*$")})
for link in links:
    print(link.attrs['href'])
    
#creating a function that loops through random articles in random pages  
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re

#This line ensures a new and interesting random path 
#through Wikipedia articles every time the program is run.
random.seed(datetime.datetime.now())

def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html)
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a",
                     href=re.compile("^(/wiki/)((?!:).)*$"))
    
links = getLinks("/wiki/Kevin_Bacon")

while len(links) > 0:
    newArticle = links[random.randint(1, len(links)-1)].attrs["href"]
    print(newArticle)
    links = getLinks(newArticle)
    



            '''Crawling An Entire Site'''
#Only links that are “new” should be crawled and searched for additional links:
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = set()

def getLinks(pageUrl):
    global pages
    
    html = urlopen("http://en.wikipedia.org"+pageUrl)
    bsObj = BeautifulSoup(html)
    for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                #We have encountered a new page
                newPage = link.attrs['href']
                print(newPage)
                pages.add(newPage)
                getLinks(newPage) #Python has a default recursion limit (how many times programs
                                  #can recursively call themselves) of 1,000
getLinks("") #if this is run, it will crash


#gather the title/ the first paragraph/ the edit link of each page:

pages = set()

def getLinks(pageURL):
    global pages
    html = urlopen("hhtp://en.wikipedia.org"+pageURL)
    bsObj = BeautifulSoup(html)
    try:
        print(bsObj.h1.get_text())
        print(bsObj.find(id = "mw-content-text").find(p)[0])
        print(bsObj.find(id = "ca-edit").find("span").find("a").attrs['href'])
    except AttributeError:
        print("Shit!")
        
for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
    if "href" in link.attrs:
        if link.attrs["href"] not in pages:
            newpage = link.attrs["href"]
            print("----------------\n"+newPage)
            pages.add(newpage)
            getLinks(newpage)
getLinks("") #if this is run, it will crash



            '''Crawling Across the Internet'''
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())

#Retrieves a list of all Internal links found on a page
def getInternalLinks(bsObj, includeUrl):
    InternalLinks = []
    #Finds all links that begin with a "/"
    for link in bsObj.findAll("a", href = re.compile("^(/|.*"+includeUrl+")")):
        if link.attrs["href"] is not None:
            if link.attrs["href"] not in InternalLinks:
                InternalLinks.append(link.attrs["href"])
    return InternalLinks

#Retrieves a list of all external links found on a page
def getExternalLinks(bsObj, excludeUrl):
    ExternalLinks = []
    #Finds all links that start with "http" or "www" that do
    #not contain the current URL
    for link in bsObj.findAll("a", href = re.compile("^(http|https|www)((?!"+excludeUrl+").)*$")):
        if link.attrs["href"] is not None:
            if link.attrs["href"] not in ExternalLinks:
                ExternalLinks.append(link.attrs["href"])
    return ExternalLinks

def splitAddress(address):
    addressParts = address.replace("http","").split("/")
    return addressParts 

def getRandomExternalLink(startingPage):
    html = urlopen(startingPage)
    bsObj = BeautifulSoup(html)
    externalLinks = getExternalLinks(bsObj, splitAddress(startingPage)[0])
    for link in externalLinks:
        if len(externalLinks) == 0:
            internalLinks = getInternalLinks(startingPage)
            return getExternalLinks(internalLinks[random.randint(0, len(internalLinks)-1)])
        else:
            return externalLinks[random.randint(0, len(externalLinks)-1)]

def followExternalOnly(startingSite):
#    externalLink = None
#    while externalLink == None:
    externalLink = getRandomExternalLink(startingSite)
    print("Going to this External Link:", externalLink)
    while externalLink == None:
        externalLink = getRandomExternalLink(startingSite)
        print("None existing Link:", externalLink)
    followExternalOnly(externalLink)

followExternalOnly("http://oreilly.com")
    
#Collects a list of all external URLs found on the site
AllIntLinks = set()
AllExtLinks = set()
def getAllExternalLinks(startingPage):
    html = urlopen(startingPage)
    bsObj = BeautifulSoup(html)
    for addressPart in splitAddress(startingPage):
        if len(addressPart) > 2:
            internalLinks = getInternalLinks(bsObj, addressPart)
            externalLinks = getExternalLinks(bsObj, addressPart)
            break
    for link in externalLinks:
        if link not in AllExtLinks:
            AllExtLinks.add(link)
            print("adding this external link:", link)
    for link in internalLinks:
        if link not in AllIntLinks:
            AllIntLinks.add(link)
            print("Inspecting this internal link:", link)
            getAllExternalLinks(link)

getAllExternalLinks("http://oreilly.com")


            '''Crawling with Scrapy'''
#see examples realized with third party webpage explanations
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    