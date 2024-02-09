import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import os
from ransac import ransac
#Currently converts image to HSV to test functionality. We can build algorithm here.
img = 'coin_dimlight.'
def imageProcessor(img, framecnt):
    print('processing image...\n')
    #show the original image
    cv.imshow('video reader', img)

    #Defining region of interest, middle of image:
    roi_x = img.shape[1] // 3  # Adjust as needed
    roi_y = img.shape[0] // 3 # Adjust as needed
    roi_width = img.shape[1] // 2  # Adjust as needed
    roi_height = img.shape[0]// 2# Adjust as needed

    #Applying ROI mask
    roi = img[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]

    #Convert to HSV and display HSV image frame by frame. 
    imgHSV= cv.cvtColor(roi, cv.COLOR_BGR2HSV)
   #Convert to grayscale
    imgHSVGS = cv.cvtColor(imgHSV, cv.COLOR_BGR2GRAY)
   
   #extract individual channels
    imgSat= imgHSV[:,:,1]
    imgVal = imgHSV[:,:,0]
    imgHue = imgHSV[:,:,2]
   
    #Apply initial binary mask using Saturation image channel
    ret, mask = cv.threshold(imgSat, 90, 200, cv.THRESH_BINARY)

    #create structuring element and use it to perform opening mask
    disc = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5,5))
    
    #dilate, erode, and dilate again.
    eroded_mask = cv.erode(mask, disc,100)
    dilated_mask = cv.dilate(eroded_mask, disc, iterations = 100)
    
    #additional filtering
    avgkernel = np.ones((3,3),np.float32)/(9)
    meanfiltered = cv.filter2D(eroded_mask, -1, avgkernel)
    gaussfiltered = cv.GaussianBlur(meanfiltered, (31,31), 5)

    dilated_2 = cv.dilate(gaussfiltered, disc, iterations=100)
    #Subtract dilated mask from initial binary mask to retreive only the edges
    edges = cv.absdiff(mask, dilated_2)
    #edges = cv.Canny(dilate2, 50, 150)
    #stack locations of edge detected pixels in the binary image
    edge_px = np.column_stack(np.where(edges>0))
    





    circs = ransac(edge_px, 70.0, 100, 20)
    
    # Create an empty image to draw lines
    img_with_circs = edges.copy()

    for circ in circs:
        center, radius = circ
        print(circ)
        #convert center to integer value
        center = center.astype(int); 
        radius = int(radius)

        print(str(radius))
        cv.circle(img_with_circs, center, radius, (255,255,255), 2)

        # Display the position of the center
        cv.putText(img_with_circs, f'Center: {center}', (center[0] + 10, center[1] - 10),
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Display images
    cv.imshow('Original Image', imgVal)
    cv.imshow('Masked image', eroded_mask)        
    cv.imshow('Edge Detection', edges)
    #cv.imshow('Region of Interest', roi)
    cv.imshow('Image with Circles', img_with_circs)
    #cv.imwrite('Frame_Dump/Frame_' + str(framecnt) + '.png', img_with_lines)
    cv.waitKey(100)
    #With Edge detection performed now we get the contour lines

    
cv.destroyAllWindows()