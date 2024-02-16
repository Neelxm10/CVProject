#The purpose of this code is to monitor and identify objects in a video stream using an image processing pipeline. 
#The original image is first shown, followed by the definition of a region of interest (ROI) inside the image. 
#The saturation channel is the main focus of the ROI extraction and conversion to the HSV colour system. 
#Areas of interest are first isolated using binary masking, and then noise is reduced by erosion and dilation procedures. 
#Gaussian blurring and averaging are used for additional filtering. To remove edges, the dilated mask is then subtracted from the original binary mask. 
#Circles within the edge-discovered picture circle are detected using the RANSAC method.
import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import os
from ransac import ransac
import csv

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

# Convert BGR image to HSV and Extract individual channels that we want to use(Sat)
    imgHSV = cv.cvtColor(roi, cv.COLOR_BGR2HSV)

    imgSat = imgHSV[:, :, 1]


    #Apply initial binary mask using Saturation image channel and create a disk for masking
    ret, mask = cv.threshold(imgSat, 70, 220, cv.THRESH_BINARY)
    disc = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5,5))
    
    eroded_mask = cv.erode(mask, disc,100)
    dilated_mask = cv.dilate(eroded_mask, disc, iterations = 100)
    
    #additional filtering
    avgkernel = np.ones((3,3),np.float32)/(9)
    meanfiltered = cv.filter2D(eroded_mask, -1, avgkernel)
    gaussfiltered = cv.GaussianBlur(meanfiltered, (31,31), 5)


    #Subtract dilated mask from initial binary mask to retreive only the edges
    edges = cv.absdiff(mask, gaussfiltered)

    #edge_px = np.column_stack(np.where(edges>0))
    
    Centre, radius= ransac(edges, 150, 50, 2)
    
    
# Print the values in the same line by frame 
    print(f"Frame: {framecnt}, Center : {Centre}")


#track Object based on the center point using CSRT method
  #  tracker = cv.TrackerCSRT_create()
  #  tracker.init(img, Centre)

    cv.waitKey(10)
cv.destroyAllWindows()



