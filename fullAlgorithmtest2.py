import cv2
from matplotlib import pyplot as py
import numpy as np
import os
# Function to select initial bounding box
def select_roi(event, x, y, flags, param):
    global bbox, frame, frame_copy, tracking
    if event == cv2.EVENT_LBUTTONDOWN:
        bbox = (x, y, 1, 1)
        tracking = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if tracking:
            bbox = (bbox[0], bbox[1], x - bbox[0], y - bbox[1])
            frame_copy = frame.copy()
            cv2.rectangle(frame_copy, (bbox[0], bbox[1]), (x, y), (0, 255, 0), 2)
            cv2.imshow('Select ROI', frame_copy)
    elif event == cv2.EVENT_LBUTTONUP:
        tracking = False

# Open the video file
video_path = '/home/instructor/Documents/OpenCV/CVFInalProj/CVProject/CVProject/IMG_8866.mov'
cap = cv2.VideoCapture(video_path)

# Check if video file opened successfully
if not cap.isOpened():
    print("Error: Unable to open video file.")
    exit()

# Read the first frame
ret, frame = cap.read()
if not ret:
    print("Error: Unable to read the first frame.")
    exit()

# Select ROI (Region of Interest) for tracking
bbox = cv2.selectROI('Select ROI', frame, fromCenter=False, showCrosshair=True)
cv2.destroyAllWindows()

# Initialize CSRT tracker
tracker = cv2.TrackerCSRT_create()
ok = tracker.init(frame, bbox)

# Loop through the video frames
while True:
    # Read a new frame
    ret, frame = cap.read()
    if not ret:
        break

    # Update tracker
    ok, bbox = tracker.update(frame)

    # Draw bounding box
    if ok:
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

    # Display the frame
    cv2.imshow('Frame', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close all windows
cap.release()
cv2.destroyAllWindows()














