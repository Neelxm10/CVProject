import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import os
from ransac import ransac

#Currently converts image to HSV to test functionality. We can build algorithm here.

def imageProcessor(img, framecnt):
    
    #show the original image
    cv.imshow('video reader', img)

    height, width = img.shape[:2]

# Define the ROI parameters
    roi_y = height // 3  # Start from one-third of the height
    roi_height = height * 2 // 2  # Take the bottom two-thirds of the height

# Applying ROI mask
    roi = img[roi_y:roi_y + roi_height, :]

# Convert BGR image to HSV
    imgHSV = cv.cvtColor(roi, cv.COLOR_BGR2HSV)

# Extract individual channels
    imgHue = imgHSV[:, :, 0]
    imgSat = imgHSV[:, :, 1]
    imgVal = imgHSV[:, :, 2]

# Convert individual channels to grayscale

    #Apply initial binary mask using Saturation image channel
    ret, mask = cv.threshold(imgSat, 70, 220, cv.THRESH_BINARY)
  
    #create structuring element and use it to perform opening mask
    disc = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5,5))
    
    #dilate, erode, and dilate again.
    eroded_mask = cv.erode(mask, disc,100)
    dilated_mask = cv.dilate(eroded_mask, disc, iterations = 7)
    
    #additional filtering
    avgkernel = np.ones((3,3),np.float32)/(9)
    meanfiltered = cv.filter2D(dilated_mask, -1, avgkernel)
    gaussfiltered = cv.GaussianBlur(meanfiltered, (31,31), 6)


    #Subtract dilated mask from initial binary mask to retreive only the edges
    edges = cv.absdiff(mask, gaussfiltered)
    #edges = cv.Canny(meanfiltered, 100, 200)
    cv.imshow('edges', edges)
    edge_px = np.column_stack(np.where(edges>0))
    
    Centers = ransac(edges,70, 20, 250, 200)
    #print(f"center: {Centers} and radius {radius}")
    cv.waitKey(10)
cv.destroyAllWindows()