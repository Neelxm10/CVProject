import cv2 as cv
from matplotlib import pyplot as py
import numpy as np
import os

#Currently converts image to HSV to test functionality. We can build algorithm here.

def imageProcessor(img, framecnt):
    print('processing image...\n')
    #show the original image
    cv.imshow('video reader', img)
    #cv.imwrite('Frame_Dump/Frame'+str(framecnt)+ '.png', img)
    #Convert to HSV and display HSV image frame by frame. 
    imgHSV= cv.cvtColor(img, cv.COLOR_BGR2HSV)
    imgHSVGS = cv.cvtColor(imgHSV, cv.COLOR_BGR2GRAY)
    imgSat= imgHSV[:,:,1]
    imgVal = imgHSV[:,:,0]
    ret, mask = cv.threshold(imgVal, 75, 200, cv.THRESH_BINARY)
    disc = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7,7))
    eroded_mask = cv.erode(mask, disc)
    dilated_mask = cv.dilate(eroded_mask, disc)
    cv.imshow('Saturation Grayscale', mask)
    cv.imshow('Eroded masked image', eroded_mask)
    cv.imshow('Dilated Masked image', dilated_mask)
    cv.waitKey(20)
    
cv.destroyAllWindows()