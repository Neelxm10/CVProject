import cv2 as cv
from matplotlib import pyplot as py
import numpy as np
import os
from imageProcessor import imageProcessor

## Import Sample video
filename = "/home/instructor/Documents/OpenCV/CVFInalProj/CVProject/CVProject/IMG_8866.mov"
capture = cv.VideoCapture(filename)

#frame counter initialization
framecnt = 0
os.mkdir('Frame_Dump2')
while (capture.isOpened()):
    state,frame = capture.read()
    if state:
        framecnt+=1
        imageProcessor(frame,framecnt)
        print('Print....FrameCount:'+str(framecnt)+'\n')
        
      
    else:
        break






