# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 15:08:44 2017

@author: princ
"""



#importing libraries
from pygraph.classes.digraph import digraph
from pygraph.algorithms.minmax import maximum_flow
import imtools


            """Graph Cuts"""

'''simple example'''
#creating the graph
gr = digraph()
#adding nodes
gr.add_nodes([0,1,2,3])

#adding edges with respective weights
gr.add_edge((0,1), wt=4)
gr.add_edge((1,2), wt=3)
gr.add_edge((2,3), wt=5)
gr.add_edge((0,2), wt=3)
gr.add_edge((1,3), wt=4)

#computing the maximum flow
flows,cuts = maximum_flow(gr,0,3) #node 0 as 'source' and node 3 as 'sink'
print ('flow is:', flows)
print ('cut is:', cuts)

'''Graphs from Images'''

from scipy.misc import imresize
import graphcut
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

im = np.array(Image.open('empire.jpg'))
im = imresize(im,0.07,interp='nearest')
size = im.shape[:2]

# add two rectangular training regions
labels = np.zeros(size)
labels[3:18,3:18] = -1
labels[-18:-3,-18:-3] = 1

# create graph
g = graphcut.build_bayes_graph(im,labels,kappa=1)

# cut the graph
res = graphcut.cut_graph(g,size)
im = np.array(Image.open('empire.jpg'))
im = imresize(im,0.07,interp='nearest')
plt.figure()
graphcut.show_labeling(im,labels)
plt.figure()
plt.gray()
plt.imshow(res)
plt.gray()
plt.axis('off')
plt.show()


            """Segmentation using clustering"""
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            

            """Variational Methods"""

from scipy.ndimage import morphology
im = array(Image.open('ceramic-houses_t0.png').convert('L'))
im = array(Image.open('flower32_t0.png').convert('L'))
U,T = imtools.rof_denoise(im,im,tolerance=0.001)
#the 'whiter' the wanted items to be isolated, the 'higher' the threshold should be (case of flowers)
#the 'darker' the wanted items to be isolated, the 'lower' the threshold should be (case of houses)
t = 0.8 #threshold for flowers
t = 0.35 #threshold for houses
U_t = 1*(U < t*U.max())
#U_t = abs(1 - U_t)
U_t_open = morphology.binary_opening(abs(1-U_t),ones((9,5)),iterations=2)
U_t_open = abs(1-U_t_open)
figure()
subplot(1, 4, 1)
imshow(im)
subplot(1, 4, 2)
imshow(U)
subplot(1, 4, 3)
imshow(U_t)
subplot(1, 4, 4)
imshow(U_t_open)
#we can also save it directly instead of graphing it
import scipy.misc
scipy.misc.imsave('result.pdf', U < t*U.max())










