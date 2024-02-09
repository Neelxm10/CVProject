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

# Convert BGR image to HSV
    imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)

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
    #dilated_mask = cv.dilate(eroded_mask, disc, iterations = 100)
    
    #additional filtering
    avgkernel = np.ones((3,3),np.float32)/(9)
    meanfiltered = cv.filter2D(eroded_mask, -1, avgkernel)
    gaussfiltered = cv.GaussianBlur(meanfiltered, (31,31), 5)

    #dilated_2 = cv.dilate(gaussfiltered, disc, iterations=100)
    #Subtract dilated mask from initial binary mask to retreive only the edges
    edges = cv.absdiff(mask, gaussfiltered)
    #edges = cv.Canny(dilate2, 50, 150)
    #stack locations of edge detected pixels in the binary image
    edge_px = np.column_stack(np.where(edges>0))
    
    circs = ransac(edges, 5000, 300, 1)
    cv.imshow('Original Image', imgSat)
        #cv.imshow('Masked image', eroded_mask)        
    cv.imshow('Edge Detection', edges)
    cv.waitKey(20)
    if circs:
    # Create an empty image to draw lines
        img_with_circs = edges.copy()

        for circ in circs:
            center, radius = circ
            print(circ)
            #convert center to integer value
            print(str(radius))
            cv.circle(img_with_circs, (center[0].astype(int), center[1].astype(int)), int(radius), (255,255,255), 2)

            # Display the position of the center
            cv.putText(img_with_circs, f'Center: ({int(center[0])}, {int(center[1])})', (center[0] + 10, center[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Display images
        #cv.imshow('Region of Interest', roi)
        cv.imshow('Image with Circles', img_with_circs)
        #cv.imwrite('Frame_Dump/Frame_' + str(framecnt) + '.png', img_with_lines)
        cv.waitKey(20)
    else:
        print("No circles detected\n")

    
cv.destroyAllWindows()