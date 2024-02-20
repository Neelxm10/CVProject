import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import os
from ransac import ransac

#Currently converts image to HSV to test functionality. We can build algorithm here.
img = cv.imread('rond.jpg')
    
#show the original image
cv.imshow('video reader', img)

height, width = img.shape[:2]

# Define the ROI parameters
top_margin = height // 12  # 1/8th of the height from the top
bottom_margin = height // 12  # 1/8th of the height from the bottom
side_margin = width // 4  # 1/4th of the width from each side

# Applying ROI mask
roi = img[top_margin:height - bottom_margin, side_margin:width - side_margin]
avgkernel = np.ones((8,8),np.float32)/(64)

# Convert the image to grayscale
gray_img = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
cv.imshow('region of interest', gray_img)
# Ensure that the image is of type CV_8UC1
if gray_img.dtype != np.uint8:
    gray_img = cv.convertScaleAbs(gray_img)

#Apply Otsu's thresholding
ret, mask = cv.threshold(gray_img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
  
#create structuring element and use it to perform opening mask
disc = cv.getStructuringElement(cv.MORPH_RECT, (5,5))
cv.imshow('mask', mask)  

#dilate, erode, and dilate again.
eroded_mask = cv.erode(mask, disc,100)
dilated_mask = cv.dilate(eroded_mask, disc, 5)
cv.imshow('mask', dilated_mask)
    

edges = cv.Canny(dilated_mask, 50, 200)
cv.imshow('edges', edges)

ransac(edges,350, 3000,10)

cv.waitKey(2000)
cv.destroyAllWindows()