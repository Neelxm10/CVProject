import cv2 as cv
from matplotlib import pyplot as py
import numpy as np
import os

#Currently converts image to HSV to test functionality. We can build algorithm here.

def imageProcessor(img, framecnt):
    print('processing image...\n')
    #show the original image
    cv.imshow('video reader', img)
    cv.imwrite('Frame_Dump/Frame'+str(framecnt)+ '.png', img)
    #Convert to HSV and display HSV image frame by frame. 
    imgHSV= cv.cvtColor(img, cv.COLOR_BGR2HSV)
    imgHSVGS = cv.cvtColor(imgHSV, cv.COLOR_BGR2GRAY)
    cv.imshow('HSV image', imgHSVGS)
    cv.imwrite('Frame_Dump/FrameHSV'+str(framecnt)+ '.png', imgHSV)
    cv.waitKey(20)
    
