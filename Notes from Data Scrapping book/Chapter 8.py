# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 14:19:59 2017

@author: princ
"""

from urllib.request import urlopen
#from bs4 import BeautifulSoup 
import re
import string
import operator
#from collections import OrderedDict, Counter

#reading in the text from the web
content = str(urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt").read(),'utf-8')

#cleaning the data from junk html expressions
def cleanInput(input):
    input = re.sub('\n+', " ", input).lower()
    input = re.sub('\[[0-9]*\]', "", input)
    input = re.sub(' +', " ", input)
    input = bytes(input, "UTF-8")
    input = input.decode("ascii", "ignore")
    cleanInput = []
    input = input.split(' ')
    for item in input:
        item = item.strip(string.punctuation)
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            cleanInput.append(item)
    return cleanInput
    
#defining the ngrams function
def ngrams(input, n):
    input = cleanInput(input)
    output = {}
    for i in range(len(input)-n+1):
        ngramTemp = " ".join(input[i:i+n])
        if ngramTemp not in output:
            output[ngramTemp] = 0
        output[ngramTemp] += 1
    return output

ngrams = ngrams(content, 2)
sortedNGrams = sorted(ngrams.items(), key = operator.itemgetter(1), reverse=True)
print(sortedNGrams)

'''Marcov Model'''
from urllib.request import urlopen
from random import randint

def wordListSum(wordList):
    sum = 0
    for word, value in wordList.items():
        sum += value
    return sum

def retrieveRandomWord(wordList):
    randIndex = randint(1, wordListSum(wordList))
    for word, value in wordList.items():
        randIndex -= value
        if randIndex <= 0:
            return word
        
def buildWordDict(text):
    #Remove newlines and quotes
    text = text.replace("\n", " ");
    text = text.replace("\"", "");
    #Make sure punctuation marks are treated as their own "words,"
    #so that they will be included in the Markov chain
    punctuation = [',','.',';',':']
    for symbol in punctuation:
        text = text.replace(symbol, " "+symbol+" ");
        words = text.split(" ")
    #Filter out empty words
    words = [word for word in words if word != ""]
    wordDict = {}
    for i in range(1, len(words)):
        if words[i-1] not in wordDict:
            #Create a new dictionary for this word
            wordDict[words[i-1]] = {}
        if words[i] not in wordDict[words[i-1]]:
            wordDict[words[i-1]][words[i]] = 0
        wordDict[words[i-1]][words[i]] = wordDict[words[i-1]][words[i]] + 1
    return wordDict

text = str(urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt").read(), 'utf-8')
wordDict = buildWordDict(text)

#Generate a Markov chain of length 100
length = 100
chain = ""
currentWord = "I"
for i in range(0, length):
    chain += currentWord+" "
    currentWord = retrieveRandomWord(wordDict[currentWord])

print(chain)

'''six degress of wikipedia'''
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', passwd="YASSOUNe11", db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("USE wikipedia")

class SolutionFound(RuntimeError):
    def __init__(self, message):
        self.message = message
        
def getLinks(fromPageId):
    cur.execute("SELECT toPage FROM links WHERE fromPage = %s", (fromPageId))
    if cur.rowcount == 0:
        return None
    else:
        return [x[0] for x in cur.fetchall()]
    
def constructDict(currentPageId):
    links = getLinks(currentPageId)
    if links:
        return dict(zip(links, [{}]*len(links)))
    return {}

#The link tree may either be empty or contain multiple links
def searchDepth(targetPageId, currentPageId, linkTree, depth):
    if depth == 0:
        print(" "*(4-depth) + "depth is 4, can't go further")
        #Stop recursing and return, regardless
        return linkTree
    if not linkTree:
        linkTree = constructDict(currentPageId)
        if not linkTree:
            #No links found. Cannot continue at this node
            print(" "*(4-depth) , currentPageId, "doesn't point to any other page, depth:", (4 - depth))
            return {}
    if targetPageId not in linkTree.keys():
        print(" "*(4-depth) + "we serached ", currentPageId, "dict, but didn't find the target, depth:", (4 - depth))
    else:
        print("TARGET "+str(targetPageId)+" FOUND!")
        print(" "*(4-depth) +"depth:",(4-depth))
        #send an alert to the stackflow upahead, to execute 'except' code only
        raise SolutionFound(" "*(4-depth) + "PAGE: "+str(currentPageId))
        
    for branchKey, branchValue in linkTree.items():
        try:
            #Recurse here to continue building the tree, while alert is not raised
            print(" "*(4-depth)+ "now looking into:", branchKey, "from previous depth:", (4 - depth))
            linkTree[branchKey] = searchDepth(targetPageId, branchKey,
                    branchValue, depth-1)
        except SolutionFound as e: #break the code, stack by stack (not abruptly)
            print(e.message)
            print(" "*(4-depth) +"Depth:", (4-depth))
            #send an alert to the stackflow upahead, to execute 'except' code only
            raise SolutionFound(" "*(4-depth) +"Page: "+str(currentPageId))
    return linkTree

try:
    searchDepth(549, 1, {}, 4)
    print("No solution found")
except SolutionFound as e:
    print(e.message)
    
    
"""NLTK"""
import nltk
nltk.download()
from nltk.book import text6
from nltk import word_tokenize
from nltk import Text
import operator

#example of importing a string into NLTK
tokens = word_tokenize("Here is some not very interesting text")
text = Text(tokens)

#frequency calculations
from nltk import FreqDist

fdist = FreqDist(text6)
words = []
for word, _ in fdist.items():
    words.append(word) 

#ratio of words to unique words
len(text6) / len(words)

#top 10 frequent words
fdist.most_common(10)

#frequency of a special word
fdist["Grail"]


#play with ngrams
from nltk import bigrams

#2-grams
bigrams = bigrams(text6)
bigramsDist = FreqDist(bigrams)
bigramsDist[("Sir", "Robin")]

#4-grams
from nltk import ngrams
fourgrams = ngrams(text6, 4)
fourgramsDist = FreqDist(fourgrams)
fourgramsDist[("father", "smelt", "of", "elderberries")]

'''Lexicology'''
from nltk.book import *
from nltk import word_tokenize
from nltk import pos_tag

#example 1
text = word_tokenize("""Strange women lying in ponds distributing swords is no
basis for a system of government. Supreme executive power derives from a mandate
from the masses, not from some farcical aquatic ceremony.""")
pos_tag(text)

#example 2
text = word_tokenize("The dust was thick so he had to dust")
pos_tag(text)

#example 3
from nltk import word_tokenize, sent_tokenize, pos_tag
sentences = sent_tokenize("""Google is one of the best companies in the world.
I constantly google myself to see what I'm up to.""")
nouns = ['NN', 'NNS', 'NNP', 'NNPS']

for sentence in sentences:
    if "google" in sentence.lower():
        taggedWords = pos_tag(word_tokenize(sentence))
        for word in taggedWords:
            if word[0].lower() == "google" and word[1] in nouns:
                print(sentence)

















