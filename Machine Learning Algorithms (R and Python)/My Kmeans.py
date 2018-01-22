# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 10:06:55 2017

@author: princ
"""

#Importing the Libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#Reading the data
dataset = pd.read_csv('Mall_Customers.csv')
X = dataset.iloc[:, 3:5].values

#using the Elbow method to find the optimum number of clusters
from sklearn.cluster import KMeans
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters = i, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)
plt.plot(range(1 ,11), wcss)
plt.title('The Elbow Method')
plt.ylabel('WCSS')
plt.xlabel('Number of Clusters')
plt.show()

#Applying k-means to the mall dataset
kmeans = KMeans(n_clusters = 5, init = 'k-means++', random_state = 0)
y_kmeans = kmeans.fit_predict(X)

#Visuliasing the clusters
plt.scatter(X[y_kmeans == 0, 0], X[y_kmeans == 0, 1], s = 100, c ='red', label = 'Careful', edgecolors="black")
plt.scatter(X[y_kmeans == 1, 0], X[y_kmeans == 1, 1], s = 100, c ='blue', label = 'Standard', edgecolors="black")
plt.scatter(X[y_kmeans == 2, 0], X[y_kmeans == 2, 1], s = 100, c ='green', label = 'Target',edgecolors="black")
plt.scatter(X[y_kmeans == 3, 0], X[y_kmeans == 3, 1], s = 100, c ='cyan', label = 'Careless', edgecolors="black")
plt.scatter(X[y_kmeans == 4, 0], X[y_kmeans == 4, 1], s = 100, c ='magenta', label = 'Sensible', edgecolors="black")
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s = 300, c = 'yellow', label = 'Centroids', edgecolors="black")
plt.title('Cluster of Clients')
plt.xlabel('Income in k$')
plt.ylabel('Spending Score (1-100)')
plt.legend()
plt.show()


