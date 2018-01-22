# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 15:39:39 2017

@author: princ
"""
#using PIL
from PIL import Image, ImageFilter

logo = Image.open("logo.jpg")
blurrylogo = logo.filter(ImageFilter.GaussianBlur)
blurrylogo.save("logo_blurred.jpg")
blurrylogo.show()

#using pytesseract
import pytesseract

img = Image.open("tesseract/ClearText.png")
text = pytesseract.image_to_string(img)
print(text)

img2 = Image.open("tesseract/NotsoClearText.png")
text2 = pytesseract.image_to_string(img2)
print(text2)

#using tesseract in cmd or Anaconda terminal:
'''tesseract ClearText.png stdout'''

#preprocessing the image
import subprocess

def cleanFile(filePath, newFilePath):
    image = Image.open(filePath)
    
    #Set a threshold value for the image, and save
    image = image.point(lambda x: 0 if x<143 else 255)
    image.save(newFilePath)
    
    #call tesseract to do OCR on the newly created image
    subprocess.call(["tesseract", newFilePath, "output"])
    
    #Open and read the resulting data file
    outputFile = open("output.txt", 'r')
    print(outputFile.read())
    outputFile.close()
    
cleanFile("tesseract/NotsoClearText.png", "tesseract/NotsoClearText_Cleaned.png")

'''Scrap book preview images from amazon'''

import time
from urllib.request import urlretrieve
import subprocess
from selenium import webdriver

#Create new Selenium driver
#driver = webdriver.PhantomJS(executable_path="PhantomJS/bin/phantomjs") #this driver reads 14 images
driver = webdriver.Chrome() #chrome reads in 16 images
driver.get("http://www.amazon.com/War-Peace-Leo-Nikolayevich-Tolstoy/dp/1427030200")

#wait for page to load
time.sleep(2)

#Click on the book preview button
driver.find_element_by_id("sitbLogoImg").click()

##Wait for the book preview to load
time.sleep(5) #if not for this timer, we would have the error:
              #"Element is not currently visible and so may not be interacted with"
              
#initialize unique imqge list
imageList = set()

#make the driver(chrome) big screen
#driver.maximize_window()

#While the right arrow is available for clicking, turn through pages
while "pointer" in driver.find_element_by_id("sitbReaderRightPageTurner").get_attribute("style"):
    driver.find_element_by_id("sitbReaderRightPageTurner").click()
    time.sleep(2)
    #Get any new pages that have loaded (multiple pages can load at once,
    #but duplicates will not be added to a set)
    pages = driver.find_elements_by_xpath("//div[@class='pageImage']/div/img")
    for page in pages:
        image = page.get_attribute("src")
        imageList.add(image)
        
driver.quit()

#Start processing the images we've collected URLs for with Tesseract
for i, image in enumerate(imageList):
    urlretrieve(image, "page{}.jpg".format(i))
    p = subprocess.Popen(["tesseract", "page{}.jpg".format(i), "page{}".format(i)],
                         stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()
    f = open("page{}.txt".format(i), encoding="utf8")
    print(f.read())

f.close()

'''Retrieving CAPTCHAs and submiting solutions'''
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup
import subprocess
import requests
from PIL import Image
from PIL import ImageOps

def cleanImage(imagePath):
    image = Image.open(imagePath)
    image = image.point(lambda x: 0 if x<143 else 255)
    borderImage = ImageOps.expand(image,border=20,fill='white')
    borderImage.save(imagePath)
    
html = urlopen("http://www.pythonscraping.com/humans-only")
bsObj = BeautifulSoup(html)

#Gather prepopulated form values
imageLocation = bsObj.find("img", {"title": "Image CAPTCHA"})["src"]
formBuildId = bsObj.find("input", {"name":"form_build_id"})["value"]
captchaSid = bsObj.find("input", {"name":"captcha_sid"})["value"]
captchaToken = bsObj.find("input", {"name":"captcha_token"})["value"]

#retrieve+clean the captcha image
captchaUrl = "http://pythonscraping.com"+imageLocation
urlretrieve(captchaUrl, "captcha.jpg")
cleanImage("captcha.jpg")

#process cleaned image through tesseract
p = subprocess.Popen(["tesseract", "captcha.jpg", "captcha"], stdout=
                     subprocess.PIPE,stderr=subprocess.PIPE)
p.wait()
f = open("captcha.txt", "r")

#Clean any whitespace characters
captchaResponse = f.read().replace(" ", "").replace("\n", "")
print("Captcha solution attempt: "+captchaResponse)

if len(captchaResponse) == 5:
    params = {"captcha_token":captchaToken, "captcha_sid":captchaSid,
              "form_id":"comment_node_page_form", "form_build_id": formBuildId,
              "captcha_response":captchaResponse, "name":"Ryan Mitchell",
              "subject": "I come to seek the Grail",
              "comment_body[und][0][value]":
                  "...and I am definitely not a bot"}
    r = requests.post("http://www.pythonscraping.com/comment/reply/10",
                      data=params)
    responseObj = BeautifulSoup(r.text)
    if responseObj.find("div", {"class":"messages"}) is not None:
        print(responseObj.find("div", {"class":"messages"}).get_text())
else:
    print("There was a problem reading the CAPTCHA correctly!")


















