#This code is just in charge of reading the video and using the image processor to send each frame in form of images 
#In order to track the edge 

import cv2 as cv
from matplotlib import pyplot as py
import numpy as np
import os
from imageProcessor import imageProcessor

## Import Sample video
filename = "videos/coin.mov"
capture = cv.VideoCapture(filename)

#frame counter initialization
framecnt = 0
#make a directory called frame dump

#while the video capture bit is true
while (capture.isOpened()):
    #store the state whether there is a frame or not, and record the frame data
    state,frame = capture.read()
    #if state is true (state == 1), process the image
    if state:
        framecnt+=1
        imageProcessor(frame,framecnt)
       
    #other wise end the program (if there is no frame, state == 0)  
    else:
        print("No remaining frames to process\n") 
        break





 
