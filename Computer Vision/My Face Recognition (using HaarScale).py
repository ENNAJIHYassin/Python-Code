# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 10:03:55 2017

@author: princ
"""

#Importing Libraries
import cv2

#loading the cascades
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

#Defining a function tha will do the detections and draw the squares
def detect(gray, frame):
    #detect the face
    faces = face_cascade.detectMultiScale(gray, #the image it takes in
                                          1.3, #the ratio by which the image are scalled down and the filters scalled up
                                          5) #in order for a zone of pixels to be accepted, at least 5 neighbor zones must also be accepted 
    # faces is a tuple (x, y, w, z)
    # while x and y are the coordinate of the upper left corner of the detected face square
    # z is the height of the square, w is its width
    for (x, y, w, z) in faces:
        #drawing the face square
        cv2.rectangle(frame, #where to draw the square 
                      (x,y), #coordinate of the upper left corner 
                      (x+w, y+z), #coordinate of the lower right corner
                      (255, 0, 0), #color of the square : blue
                      2) #thichness of the square
        # taking our region of interest that corresponds to the detected face square
        roi_gray = gray[y:y+z, x:x+w]  #from the gray image  
        roi_color = frame[y:y+z, x:x+w] #from the frame colored image
        #detect the eyes
        eyes = eye_cascade.detectMultiScale(roi_gray, #we could have taken gray, but in order to save time, we narrow it down
                                               1.1, #this value is obtained by experimenting
                                               3) #same with this one
        # eyes is a tuple (ex, ey, ew, ez)
        # while ex and ey are the coordinate of the upper left corner of the detected face square
        # ez is the height of the square, ew is its width
        for (ex, ey, ew, ez) in eyes:
            #drawing the eye square
            cv2.rectangle(roi_color, #where to draw the square 
                          (ex,ey), #coordinate of the upper left corner 
                          (ex+ew, ey+ez), #coordinate of the lower right corner
                          (0, 255, 0), #color of the square : green
                          2) #thichness of the square
    return frame #return the frame on which the squares are printed

#Starts video capture
video_capture = cv2.VideoCapture(0)  #(0 for internal webcam, 1 for external)

#Applying everything to the webcam stream
while True:
    _, frame = video_capture.read() #get the frame from the video
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #scale the frame in gray 
    canvas = detect(gray, frame) #get the frame with printed face and eye squares
    cv2.imshow('Video', canvas) #show the canvas live on the video
    if cv2.waitKey(1) & 0xFF == ord('q'): #if we press 'q'
        break   #the detection is gonna end

#Turn off the webcam
video_capture.release()

#Close the window
cv2.destroyAllWindows()