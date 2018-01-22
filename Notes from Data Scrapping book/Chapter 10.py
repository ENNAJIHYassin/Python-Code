# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 13:26:36 2017

@author: princ
"""

from selenium import webdriver
import time

driver = webdriver.PhantomJS(executable_path="PhantomJS/bin/phantomjs")
driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")
#scrap the page while it is loading:
time.sleep(1)
print(driver.find_element_by_id("content").text)
driver.close()
#wait for the page to load, then scrap it
time.sleep(3)
print(driver.find_element_by_id("content").text)
driver.close()

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.PhantomJS(executable_path = "PhantomJS/bin/phantomjs")
driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")

try:
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "LoadedButton")))
finally:
    print(driver.find_element_by_id("content").text)
    driver.close()
    
    
'''Handeling Redirect'''

from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException

def waitForLoad(driver):
    elem = driver.find_element_by_tag_name("html")
    count = 0
    while True:
        count += 1
        if count > 20:
            print("Timing out after 10 seconds and returning")
            return
        time.sleep(.5)
        try:
            elem == driver.find_element_by_tag_name("html")
        except StaleElementReferenceException:
            return
    
driver = webdriver.PhantomJS(executable_path='PhantomJS/bin/phantomjs')
driver.get("http://pythonscraping.com/pages/javascript/redirectDemo1.html")
waitForLoad(driver)
print(driver.page_source)