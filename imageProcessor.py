import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import os
from ransac import ransac
#Currently converts image to HSV to test functionality. We can build algorithm here.

def imageProcessor(img, framecnt):
    print('processing image...\n')
    #show the original image
    cv.imshow('video reader', img)

    #Defining region of interest, middle of image:
    roi_x = img.shape[1] // 4  # Adjust as needed
    roi_y = img.shape[0] // 4  # Adjust as needed
    roi_width = img.shape[1] // 2  # Adjust as needed
    roi_height = img.shape[0] // 4 # Adjust as needed

    #Applying ROI mask
    roi = img[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]

    #Convert to HSV and display HSV image frame by frame. 
    imgHSV= cv.cvtColor(roi, cv.COLOR_BGR2HSV)
    imgHSVGS = cv.cvtColor(imgHSV, cv.COLOR_BGR2GRAY)
    imgSat= imgHSV[:,:,1]
    imgVal = imgHSV[:,:,0]
    imgHue = imgHSV[:,:,2]
    #Apply initial binary mask using Saturation image channel
    ret, mask = cv.threshold(imgVal, 90, 190, cv.THRESH_BINARY)

    #create structuring element and use it to perform opening mask
    disc = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7,7))
    
    dilated_mask = cv.dilate(mask, disc)
    eroded_mask = cv.erode(dilated_mask, disc, 10)
    dilate2 = cv.dilate(eroded_mask, disc, 10)
    #Subtract dilated mask from initial binary mask to retreive only the edges
    edges = cv.absdiff(mask, eroded_mask)

    #stack locations of edge detected pixels in the binary image
    edge_px = np.column_stack(np.where(edges>0))




    lines = ransac(edge_px, 1.0, 50, 10)

    # Create an empty image to draw lines
    img_with_lines = edges.copy()

    if lines is not None:
        for line in lines:
            m, b = line
            x1 = 0
            y1 = int(b)
            x2 = img.shape[1] - 1  # Width of the image
            y2 = int(m * x2 + b)
                    # Ensure y1 and y2 are within the image boundaries
            y1 = max(0, min(y1, roi.shape[0] - 1))
            y2 = max(0, min(y2, roi.shape[0] - 1))
            cv.line(img_with_lines, (x1, y1), (x2, y2), (255, 255, 255), 2)
            print(line)
    # Display images
    #v.imshow('Original Image', img)
    cv.imshow('Masked image', mask)        
    cv.imshow('Edge Detection', edges)
    cv.imshow('Region of Interest', roi)
    cv.imshow('Image with Lines', img_with_lines)
    #cv.imwrite('Frame_Dump/Frame_' + str(framecnt) + '.png', img_with_lines)
    cv.waitKey(100)
    #With Edge detection performed now we get the contour lines

    
cv.destroyAllWindows()