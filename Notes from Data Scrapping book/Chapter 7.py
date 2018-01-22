# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 11:41:39 2017

@author: princ
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup 
import re
import string
from collections import OrderedDict, Counter

#reading in the text from the web
html = urlopen("https://en.wikipedia.org/wiki/Python_(programming_language)")
bsObj = BeautifulSoup(html)
text = bsObj.find("div", {"id":"mw-content-text"}).findAll("p")
for t in text:
    print(t.get_text())

#cleaning the data from junk html expressions
def cleanInput(content):
    content = str()
    for t in text:
        content += t.get_text() 
    content = re.sub("\[[0-9]*\]"," ", content) #take away wikipedia reference numbers
    content = re.sub('\n+', " ", content)
    content = re.sub(' +', " ", content)
    content = bytes(content, "UTF-8")
    content = content.decode("ascii", "ignore")
    content = content.lower()
    content = content.split(' ')
    cleanInput = []
    for word in content:
        word = word.strip(string.punctuation)
        if len(word)>1 or (word == 'a' or word == 'i'):
            cleanInput.append(word)
    return cleanInput
    
#defining the ngrams function
def ngrams(input, n):
    content = cleanInput(input)
    ngram=[]
    for i in range(len(content)-n+1):
        ngram.append(content[i:i+n])
    return ngram

ngrams = ngrams(text, 2)

cnt = Counter()
for ngram in ngrams:
    cnt[str(ngram)] += 1
sort_dict = OrderedDict(sorted(cnt.items(), key = lambda t: t[1], reverse = True))
"3462"
print(sort_dict)

first_10_ngrams = [ (ngram, sort_dict[ngram]) for ngram in list(sort_dict.keys())[:10]  ]












