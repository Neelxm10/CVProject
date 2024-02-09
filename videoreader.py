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
if not os.path.exists:
    os.mkdir('Frame_Dump')
else:
    print("Directory already exists, proceeding with overwriting directory\n")
#while the video capture bit is true
while (capture.isOpened()):
    #store the state whether there is a frame or not, and record the frame data
    state,frame = capture.read()
    #if state is true (state == 1), process the image
    if state:
        framecnt+=1
        imageProcessor(frame,framecnt)
        print('FrameCount:'+str(framecnt)+'\n')
        
    #other wise end the program (if there is no frame, state == 0)  
    else:
        print("No remaining frames to process\n") 
        break





 
