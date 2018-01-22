# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 15:32:51 2017

@author: princ
"""

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
'''import random
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
 '''

#Thompson Sampling
import random
N = 10000
d = 10
total_rewards = 0
ads_selected = []
actual_accumulated_reward = []
max_accumulated_reward = []
number_of_rewards_1 = [0] * d
number_of_rewards_0 = [0] * d
for n in range(0, N):
    ad = 0
    max_random = 0
    for i in range(0, d):
        random_beta = random.betavariate(number_of_rewards_1[i] + 1, number_of_rewards_0[i] + 1)
        if random_beta > max_random:
            max_random = random_beta
            ad = i
    ads_selected.append(ad)  
    reward = dataset.values[n , ad]
    if reward == 1:
        number_of_rewards_1[ad] = number_of_rewards_1[ad] + reward 
    else:
        number_of_rewards_0[ad] = number_of_rewards_0[ad] + 1
    number_of_rewards_1[ad] = number_of_rewards_1[ad] + reward 
    total_rewards = total_rewards + reward         
    actual_accumulated_reward.append(reward)
    max_accumulated_reward.append(max(dataset.values[n, :]))
    
    
    
#Visualising the results
#plt.hist(ads_selected)
#plt.show()
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



