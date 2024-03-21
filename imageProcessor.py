import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import os
from ransac import ransac

def imageProcessor(img, framecnt):
#Currently converts image to HSV to test functionality. We can build algorithm here.
    filename = 'calibration_data/'

    
    #show the original image
    #cv.imshow('video reader', img)

    height, width = img.shape[:2]

# Define the ROI parameters
    roi = np.load(filename+'roi.npy')
    x, y, w, h = roi
    

# Applying ROI mask
    newimg = img[y: y+h, x: x+h]
    avgkernel = np.ones((8,8),np.float32)/(64)

# Convert the image to grayscale
    gray_img = cv.cvtColor(newimg, cv.COLOR_BGR2GRAY)
    #cv.imshow('region of interest', gray_img)
# Ensure that the image is of type CV_8UC1
    if gray_img.dtype != np.uint8:
        gray_img = cv.convertScaleAbs(gray_img)

#Apply Otsu's thresholding
    ret, mask = cv.threshold(gray_img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
  
#create structuring element and use it to perform opening mask
    disc = cv.getStructuringElement(cv.MORPH_RECT, (5,5))
    #cv.imshow('mask', mask)  

#dilate, erode, and dilate again.
    eroded_mask = cv.erode(mask, disc,1)
    dilated_mask = cv.dilate(eroded_mask, disc, 5)
    #cv.imshow('mask', dilated_mask)
    

    edges = cv.Canny(dilated_mask, 0, 220)
    #cv.imshow('edges', edges)

    Circle = ransac(edges,300, 100,10, framecnt, newimg)

    cv.waitKey(200)
    if Circle is not None:
        return Circle[0], Circle[1]  # Return only the center coordinates (x, y)
    else:
        return [0,0], 0  # Return None when no circle is found
        
   
    