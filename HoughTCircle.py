import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('coin_dimlight.jpg')
# Convert the image to grayscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# Use HoughCircles to detect circles in the image
circles = cv.HoughCircles(
    gray,
    cv.HOUGH_GRADIENT,
    dp=1,  # Inverse ratio of accumulator resolution to image resolution
    minDist=50,  # Minimum distance between detected centers
    param1=50,  # Higher threshold for Canny edge detector
    param2=30,  # Accumulator threshold for circle detection
    minRadius=10,  # Minimum radius of the circles
    maxRadius=100  # Maximum radius of the circles
)

# If circles are found, draw them on the original image
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # Draw the outer circle
        cv.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # Draw the center of the circle
        cv.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

# Display the result
cv.imshow('frame', cv.cvtColor(img, cv.COLOR_BGR2RGB))
plt.title('Detected Circles')
plt.show()
