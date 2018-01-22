# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 17:55:51 2017

@author: princ
"""

#Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#Importing Dataset
dataset= pd.read_csv('Market_Basket_Optimisation.csv', header = None)
transactions=[]
for i in range(0, 7501):
    transactions.append([str(dataset.values[i,j]) for j in range(0, 20)])
    
#Training the Apriori model
from apyori import apriori
rules = apriori(transactions, min_support = 0.003, min_confidence = 0.2, min_lift = 3, min_lengh = 2)

#visualising the results
results = list(rules)
myResults = [list(x) for x in results]
myRes = []
for j in range(0, 153):
    myRes.append([list(x) for x in myResults[j][2]])