# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 16:24:33 2017

@author: princ
"""

#Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#Importing Dataset
dataset= pd.read_csv('Ads_CTR_Optimisation.csv')


#Random Selection
import random
N = 10000
d = 10
ad_selected = []
total_reward = 0
for n in range(N):
    ad = random.randrange(d)
    ad_selected.append(ad)
    reward = dataset.values[n , ad]
    total_reward = total_reward + reward
    
#Visualisation
plt.hist(ad_selected)
plt.title('Histogram of ads selections')
plt.xlabel('Ads')
plt.ylabel('Number of times each ad was selected')
plt.show()
 

#Upper Confidence Bound Algo
import math
from collections import Counter
N = 10000
d = 10
total_rewards = 0
ads_selected = []
actual_accumulated_reward = []
max_accumulated_reward = []
number_of_selections = [0] * d
sum_of_rewards = [0] * d
for n in range(0, N):
    ad = 0
    max_upper_bound = 0
    for i in range(0, d):
        if( number_of_selections[i] > 0 ):
            average_reward = sum_of_rewards[i] / number_of_selections[i]
            delta_i = math.sqrt(3/2 * math.log(n+1) / number_of_selections[i])
            UCB = average_reward + delta_i
        else:
            UCB = 1e400
        if UCB > max_upper_bound:
            max_upper_bound = UCB
            ad = i
    ads_selected.append(ad)
    number_of_selections[ad] = number_of_selections[ad] + 1   
    reward = dataset.values[n , ad]
    sum_of_rewards[ad] = sum_of_rewards[ad] + reward 
    total_rewards = total_rewards + reward         
    actual_accumulated_reward.append(reward)
    max_accumulated_reward.append(max(dataset.values[n, :]))
    
    
    
#Visualising the results
plt.hist(ads_selected)
plt.show()


    #Regret Curve
X = range(0, N)
Y1 = [0] * N
Y2 = [0] * N
Y3 = [0] * N
Y1[0] = actual_accumulated_reward[0] 
Y2[0] = max_accumulated_reward[0]
Y3[0] = max_accumulated_reward[0] - actual_accumulated_reward[0] 
for i in range(0 , 9999):
    Y1[i+1] = Y1[i] + actual_accumulated_reward[i+1]
    Y2[i+1] = Y2[i] + max_accumulated_reward[i+1]
    Y3[i+1] = Y3[i] + max_accumulated_reward[i+1] - actual_accumulated_reward[i+1]
plt.plot(X , Y1, label = 'Realised Reward')
plt.plot(X , Y2, label = 'Best Action (Max Expected Reward)')
plt.plot(X , Y3, label = 'Regret Curve (Best - Realised)')
plt.xlabel('Rounds')
plt.ylabel('Reward Count')
plt.title(' Regret Curve')
plt.legend()
plt.show()


