# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 14:29:11 2017

@author: princ
"""
#Importing Libraries
import torch #Contains dynamic graphs which is very useful for gradiant descent
from torch.autograd import Variable #torch variable containing the tensor and the gradient which will be one element of the graph 
import cv2 #to draw rectangles
from data import BaseTransform, VOC_CLASSES as labelmap #import from data folder
from ssd import build_ssd #import from the ssd python file
import imageio

#Defining function that will do detections
def detect(frame, net, transform):
    height, width = frame.shape[:2]
    '''transform the frame to suit the ANN'''
    #This process is necessary before every torch ANN
    frame_t = transform(frame)[0] #convert frame to np array
    x = torch.from_numpy(frame_t) #convert np array to torch tensor
    x = x.permute(2, 0, 1) #switch from BGR to RBG
    x = x.unsqueeze(0) #gather input images into batches: 0 here is the index of the first dimension corresponding to the batch that we are adding to our structure of input images
    x = Variable(x)#convert torch tensor of inputs into a torch variable which computes very efficiently gradient descent during back propagation
    '''process the ANN output'''
    y = net(x) #feed the frame to the ANN
    # normalize between 0 and 1 the values of the detected objects' positions 
    scale = torch.Tensor([width, height, #upper left corner of the rectangle
                          width, height]) #lower right corner of the rectangle
    detections = y.data #extract specefic data attributes from ANN output. y is here a torch variable (tensor, gradient). calling .data method gives us back the tensor component
    # detections tensor elements : [batch of outputs, number of classes(dogs, cars etc..) detected in the input batch, number of occurence of the class, (score, x0, Yo, x1 Y1)]
    # that last tuple of 5 elements: for each occurence of each class in the output batch we get an acceptance threshold(class occurs if score > 0.6), upper left, and lower right coordinates
    '''draw the rectangles'''
    for i in range(detections.size(1)): #range is number of classes
        j = 0 # j is occurence of the class
        while detections[0,i,j,0] >= 0.6: #score of the class i with occurence j >= 0.6
            pt = (detections[0, i, j, 1:] * scale) #coordinates of the square position scaled to the images dimensions 
            pt = pt.numpy() #convert the coordinates into a numpay array
            cv2.rectangle(frame, (int(pt[0]), int(pt[1])), (int(pt[2]), int(pt[3])), (255, 0, 0), 2) #draw the rectangle on top of the frame
            cv2.putText(frame, labelmap[i-1], (int(pt[0]), int(pt[1])), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA) #print the label of the class
            j += 1
    return frame

#Creating the SSD ANN
net = build_ssd('test') #create the ANN
net.load_state_dict(torch.load('ssd300_mAP_77.43_v2.pth', map_location = lambda storage, loc: storage) #Load the weights of the already pre-trained ANN

#creating the transformation
transform = BaseTransform(net.size, (104/256.0, 117/256.0, 123/256.0))
#net.size is the target size of the images to feed to the ANN
#the last tuple is for scaling the color values

#doing some object detection on a video
reader = imageio.get_reader('funny_dog.mp4') #opening the video
fps = reader.get_meta_data()['fps'] #get FPS of the video
writer = imageio.get_writer('output.mp4', fps = fps) #output the video
for i, frame in enumerate(reader):
    frame = detect(frame, net.eval(), transform)
    writer.append_data(frame) #add frames to the output video
    print(i)
writer.close()






























