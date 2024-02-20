import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import os
from ransac import ransac
from imageProcessor import imageProcessor
# Import necessary modules for 3D plotting
from mpl_toolkits.mplot3d import Axes3D

# Create lists to store coordinates


filename = "videos/coin.mov"
capture = cv.VideoCapture(filename)
framecnt = 0

if not os.path.exists('Frame_Dump'):
    os.mkdir('Frame_Dump')
else:
    print("Directory already exists, proceeding with overwriting directory\n")

frame_count_list = []
center_x_list = []  # Make sure this list is defined

plt.ion()  # Turn on interactive mode

try:
    while capture.isOpened():
        state, frame = capture.read()
        if state:
            framecnt += 1
            center_x = imageProcessor(frame, framecnt)

            # If center x-coordinate is found, append it to the list
            if center_x is not None:
                frame_count_list.append(framecnt)
                center_x_list.append(center_x)

                # Plot the center x-coordinate with respect to frame count
                plt.clf()  # Clear the previous plot
                plt.plot(frame_count_list, center_x_list, label='Center X Coordinate', marker='o', linestyle='-')
                plt.xlabel('Frame Count')
                plt.ylabel('Center Position')
                plt.title('Center Position over Frame Count')
                plt.draw()
                plt.pause(0.1)  # Adjust the pause duration as needed

            print('FrameCount:' + str(framecnt) + '\n')
        else:
            print("No remaining frames to process\n")
            break

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    plt.ioff()  # Turn off interactive mode
    capture.release()
    plt.show()