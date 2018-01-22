# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 10:22:18 2017

@author: princ
"""

'''Twitter API'''
from twitter import Twitter,OAuth

#connecting to the Twitter API
t = Twitter(auth=OAuth("841376905878159360-3fc06f8nE2uAZ2Y9ypMWJSCroEWIjAX",
                       "Vql9jVLalMHdwT8hICaJBW7jtnZnY6yNah1XIFv7v6sFV",
                       "MsysAHm4X8RSvPZzLtEoeFiiZ",
                       "70D1mHX8M3Wz75SMXWpt69W3mdgwH2x71y4WjfjhNCGFbNeeRA"))

#printing a JSON list of tweets containing the hashtag #python
pythonTweets = t.search.tweets(q = "#python")
print(pythonTweets)

#making a status update through the API:
statusUpdate = t.statuses.update(status='Hello, world!')
print(statusUpdate)

#asking for the last five tweets that were posted to @montypython’s
#timeline (this includes any retweets they might have made).
pythonStatuses = t.statuses.user_timeline(screen_name="montypython", count=5)
print(pythonStatuses)


'''Parsing JSON'''

import json
from urllib.request import urlopen

#accessing imformation by using json
def getCountry(AddressIP):
    response = urlopen("http://freegeoip.net/json/"+AddressIP).read().decode("utf-8")
    responseJason = json.loads(response)
    return responseJason.get("country_code")

print(getCountry("50.78.253.58"))

#manipulating jason strings with json
jsonString = '''{"arrayOfNums":[{"number":0},{"number":1},{"number":2}],
               "arrayOfFruits":[{"fruit":"apple"},{"fruit":"banana"},
                                {"fruit":"pear"}]}'''
jsonObj = json.loads(jsonString)

print(jsonObj.get("arrayOfNums"))
print(jsonObj.get("arrayOfNums")[1])
print(jsonObj.get("arrayOfNums")[1].get("number")+
jsonObj.get("arrayOfNums")[2].get("number"))
print(jsonObj.get("arrayOfFruits")[2].get("fruit"))


'''Bringing it All Back Home'''

from urllib.request import HTTPError
from bs4 import BeautifulSoup
import re
import datetime
import random

#set unique seed
random.seed(datetime.datetime.now())

def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html)
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a",
                     href=re.compile("^(/wiki/)((?!:).)*$"))

def getHistoryIPs(pageUrl):
    #Format of revision history pages is:
    #http://en.wikipedia.org/w/index.php?title=Title_in_URL&action=history
    pageUrl = pageUrl.replace("/wiki/", "")
    historyUrl = "http://en.wikipedia.org/w/index.php?title="+pageUrl+"&action=history"
    print("history url is: "+historyUrl)
    html = urlopen(historyUrl)
    bsObj = BeautifulSoup(html)
    #finds only the links with class "mw-anonuserlink" which has IP addresses
    #instead of usernames
    ipAddresses = bsObj.findAll("a", {"class":"mw-anonuserlink"})
    addressList = set()
    for ipAddress in ipAddresses:
        addressList.add(ipAddress.get_text())
    return addressList

links = getLinks("/wiki/Python_(programming_language)")

while(len(links) > 0):
    for link in links:
        print("-------------------")
        historyIPs = getHistoryIPs(link.attrs["href"])
        for historyIP in historyIPs:
            print(historyIP)
            
newLink = links[random.randint(0, len(links)-1)].attrs["href"]
links = getLinks(newLink)
    
def getCountry(ipAddress):
    try:
        response = urlopen("http://freegeoip.net/json/"
                           +ipAddress).read().decode('utf-8')
    except HTTPError:
        return None
    responseJson = json.loads(response)
    return responseJson.get("country_code")

links = getLinks("/wiki/Python_(programming_language)")

while(len(links) > 0):
    for link in links:
        print("-------------------")
        historyIPs = getHistoryIPs(link.attrs["href"])
        for historyIP in historyIPs:
            IPcountry = getCountry(historyIP)
            print(historyIP," : ", IPcountry)



























