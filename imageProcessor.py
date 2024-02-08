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
    ret, mask = cv.threshold(imgVal, 90, 220, cv.THRESH_BINARY)

    #create structuring element and use it to perform opening mask
    disc = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7,7))
    
    dilated_mask = cv.dilate(mask, disc)
    eroded_mask = cv.erode(dilated_mask, disc)
    #Subtract dilated mask from initial binary mask to retreive only the edges
    edges = cv.absdiff(mask, eroded_mask)
    lines = cv.HoughLines(edges, 1, np.deg2rad(1), 0)


    # Draw lines on a copy of the original image
     # Create an empty image to draw lines
    img_with_lines = np.zeros_like(img)

    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv.line(img_with_lines, (x1, y1), (x2, y2), (0, 90, 255), 2)

    # Display images
    #v.imshow('Original Image', img)
    cv.imshow('Edge Detection', edges)
    cv.imshow('Image with Lines', img_with_lines)
    cv.imwrite('Frame_Dump/Frame_' + str(framecnt) + '.png', img_with_lines)
    cv.waitKey(0)
    #With Edge detection performed now we get the contour lines

    
cv.destroyAllWindows()