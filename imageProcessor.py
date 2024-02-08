import cv2 as cv
from matplotlib import pyplot as py
import numpy as np
import os

#Currently converts image to HSV to test functionality. We can build algorithm here.

def imageProcessor(img, framecnt):
    print('processing image...\n')
    #show the original image
    cv.imshow('video reader', img)
    #Convert to HSV and display HSV image frame by frame. 
    imgHSV= cv.cvtColor(img, cv.COLOR_BGR2HSV)
    imgHSVGS = cv.cvtColor(imgHSV, cv.COLOR_BGR2GRAY)
    imgSat= imgHSV[:,:,1]
    imgVal = imgHSV[:,:,0]
    imgHue = imgHSV[:,:,2]
    #Apply initial binary mask using Saturation image channel
    ret, mask = cv.threshold(imgSat, 0, 255, cv.THRESH_BINARY)

    #create structuring element and use it to perform opening mask
    disc = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7,7))
    eroded_mask = cv.erode(mask, disc)
    dilated_mask = cv.dilate(eroded_mask, disc)
    #Subtract dilated mask from initial binary mask to retreive only the edges
    edges = cv.absdiff(mask, dilated_mask)
    
    #Uncomment these for when you wanna check out the masks.
    #edges = cv.Canny(dilated_mask, 120,180)
    #cv.imshow('Saturation Grayscale', mask)
    #cv.imshow('Dilated Masked image', dilated_mask)
    cv.imshow('Edge Detection', edges)
    cv.imwrite('Frame_Dump/Frame_'+str(framecnt)+'.png',edges)
    cv.waitKey(20)
    
cv.destroyAllWindows()