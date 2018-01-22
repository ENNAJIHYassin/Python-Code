# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 14:44:29 2017

@author: princ
"""
'''Pyhton Unitest'''

#test title and content of the 'Monty Python' wikipage
from urllib.request import urlopen, unquote
from bs4 import BeautifulSoup
import unittest
import random
import re

class TestWikipedia(unittest.TestCase):
    bsObj = None
    def setUpClass():
        global bsObj
        url = "http://en.wikipedia.org/wiki/Monty_Python"
        bsObj = BeautifulSoup(urlopen(url), "html5lib")
    def test_titleText(self):
        global bsObj
        pageTitle = bsObj.find("h1").get_text()
        self.assertEqual("Monty Python", pageTitle);
    def test_contentExists(self):
        global bsObj
        content = bsObj.find("div",{"id":"mw-content-text"})
        self.assertIsNotNone(content)
        
if __name__ == '__main__':
    unittest.main()
    
#test
class TestWikipedia2(unittest.TestCase):
    bsObj = None
    url = None
    def test_PageProperties(self):
        global bsObj
        global url
        url = "http://en.wikipedia.org/wiki/Monty_Python"
        #Test the first 100 pages we encounter
        for i in range(1, 100):
            bsObj = BeautifulSoup(urlopen(url), "html5lib")
            titles = self.titleMatchesURL()
            self.assertEqual(titles[0], titles[1])
            self.assertTrue(self.contentExists())
            url = self.getNextLink()
        print("Done!")
    def titleMatchesURL(self):
        global bsObj
        global url
        pageTitle = bsObj.find("h1").get_text()
        urlTitle = url[(url.index("/wiki/")+6):]
        urlTitle = urlTitle.replace("_", " ")
        urlTitle = unquote(urlTitle)
        return [pageTitle.lower(), urlTitle.lower()]
    def contentExists(self):
        global bsObj
        content = bsObj.find("div",{"id":"mw-content-text"})
        if content is not None:
            return True
        return False
    def getNextLink(self):
        bsObj = BeautifulSoup(urlopen(url), "html5lib")
        links = bsObj.find("div", {"id":"bodyContent"}).findAll("a",
                         href=re.compile("^(/wiki/)((?!:).)*$"))
        articleUrl = links[random.randint(0, len(links)-1)].attrs["href"]
        if articleUrl is not None:
            return "http://en.wikipedia.org"+articleUrl
        else:
            print("No new links found")
                
if __name__ == '__main__':
    unittest.main()
    
'''interacting with a website'''
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

driver = webdriver.PhantomJS(executable_path='PhantomJS/bin/phantomjs')
driver.get("http://pythonscraping.com/pages/files/form.html")

firstnameField = driver.find_element_by_name("firstname")
lastnameField = driver.find_element_by_name("lastname")
submitButton = driver.find_element_by_id("submit")

### METHOD 1 ###
firstnameField.send_keys("Ryan")
lastnameField.send_keys("Mitchell")
submitButton.click()
################
### METHOD 2 ###
actions = ActionChains(driver).click(firstnameField).send_keys("Ryan").click(lastnameField).send_keys("Mitchell").send_keys(Keys.RETURN)
actions.perform()
################
print(driver.find_element_by_tag_name("body").text)
driver.close()

'''drag and drop'''
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ActionChains
import time

driver = webdriver.PhantomJS(executable_path='PhantomJS/bin/phantomjs')
driver = webdriver.Chrome()
driver.get('http://pythonscraping.com/pages/javascript/draggableDemo.html')
print(driver.find_element_by_id("message").text)

element = driver.find_element_by_id("draggable")
target = driver.find_element_by_id("div2")
actions = ActionChains(driver)
time.sleep(4)
actions.drag_and_drop(element, target).perform()

time.sleep(4)
print(driver.find_element_by_id("message").text)

'''screen shot'''
driver = webdriver.PhantomJS(executable_path='PhantomJS/bin/phantomjs') #crops the whole page!!
#driver = webdriver.Chrome() #only crops the part of page visible on the browser window
driver.get('http://www.pythonscraping.com/')
#driver.save_screenshot('pythonscraping.png')
driver.get_screenshot_as_file('pythonscraping.png')


'''Combining Unnitest and selenium'''
class TestAddition(unittest.TestCase):
    driver = None
    def setUp(self):
        global driver
        driver = webdriver.PhantomJS(executable_path='<Path to Phantom JS>')
        url = 'http://pythonscraping.com/pages/javascript/draggableDemo.html'
        driver.get(url)
    def tearDown(self):
        print("Tearing down the test")
    def test_drag(self):
        global driver
        element = driver.find_element_by_id("draggable")
        target = driver.find_element_by_id("div2")
        actions = ActionChains(driver)
        actions.drag_and_drop(element, target).perform()
        self.assertEqual("You are definitely not a bot!", driver.find_element_by_id("message").text)
    
if __name__ == '__main__':
    unittest.main()