# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 12:32:19 2017

@author: princ
"""

'''Adjust Headers to look like human'''
import requests
from bs4 import BeautifulSoup

session = requests.Session()
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
url = "https://www.whatismybrowser.com/developers/what-http-headers-is-my-browser-sending"
req = session.get(url, headers=headers)
bsObj = BeautifulSoup(req.text, "html5lib")
print(bsObj.find("table",{"class":"table-striped"}).get_text)

'''Handling Cookies'''
from selenium import webdriver

driver = webdriver.PhantomJS(executable_path = "PhantomJS/bin/phantomjs")
driver.get("http://pythonscraping.com")
driver.implicitly_wait(1)
print(driver.get_cookies())
savedCookies = driver.get_cookies()

driver2 = webdriver.PhantomJS(executable_path = "PhantomJS/bin/phantomjs")
driver2.get("http://pythonscraping.com")
driver2.delete_all_cookies()
for cookie in savedCookies:
    driver2.add_cookie(cookie)
    
driver2.get("http://pythonscraping.com")
driver.implicitly_wait(1)
print(driver2.get_cookies())

'''Avoiding HoneyPots'''
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

#openup the connection to the website
driver = webdriver.PhantomJS(executable_path="PhantomJS/bin/phantomjs")
driver.get("http://pythonscraping.com/pages/itsatrap.html")

#get links on the page 
links = driver.find_elements_by_tag_name("a")

#check for trap links
for link in links:
    if not link.is_displayed():
        print("The link "+link.get_attribute("href")+" is a trap")
        
#get input fields on the page        
fields = driver.find_elements_by_tag_name("input")

#check for trap inputs
for field in fields:
    if not field.is_displayed():
        print("Do not change value of "+field.get_attribute("name"))