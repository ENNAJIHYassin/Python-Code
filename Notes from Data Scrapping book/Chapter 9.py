# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 10:50:05 2017

@author: princ
"""

import requests

'''Submitting Text, Files and Images'''

#sending text
params = { "firstname" : "ana" , "lastname" : "houwa"}
r = requests.post("http://pythonscraping.com/files/processing.php", data=params)
print(r.text)

params = {'email_addr': 'ryan.e.mitchell@gmail.com'}
r = requests.post("http://post.oreilly.com/client/o/oreilly/forms/quicksignup.cgi", data=params)
print(r.text)

#sending files
files = {'uploadFile': open('logo.jpg', 'rb')}
r = requests.post("http://pythonscraping.com/pages/processing2.php", files=files)
print(r.text)

'''Handling Cookies'''

#using cookies to browse through the website 
params = {"username" : "anything", "password" : "password"}
r = requests.post("http://pythonscraping.com/pages/cookies/welcome.php", params)
print(r.cookies.get_dict())
r2 = requests.get("http://pythonscraping.com/pages/cookies/profile.php", cookies = r.cookies)
print(r2.text)

#using a session
s = requests.Session() 
params = {"username" : "anything", "password" : "password"}
r = s.post("http://pythonscraping.com/pages/cookies/welcome.php", params)
print(r.cookies.get_dict())
r2 = s.get("http://pythonscraping.com/pages/cookies/profile.php")
print(r2.text)

'''HTTP Basic Access Authentification'''
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth("anything","password")
r = requests.post("http://pythonscraping.com/pages/auth/login.php", auth = auth)
print(r.text)