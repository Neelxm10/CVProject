import cv2 as cv
import numpy as np
import random
import subprocess
import os
from calibCamera import calibCamera


cap = cv.VideoCapture(0)
####################################READ INPUT VIDEO STREAM###########################################
state,frame = cap.read()
h, w = frame.shape[:2]
output = cv.VideoWriter("coinTrack.avi", cv.VideoWriter_fourcc(*'MPEG'), 30, (w, h)) 
while cap.isOpened():
    state, frame = cap.read()
    if state == True:
        output.write(frame)
        cv.imshow('video feed',frame)
        #press s to save video
        if cv.waitKey(1) & 0xFF == ord('s'): 
            break
output.release()  
cap.release()    
cv.destroyAllWindows()
output_file = 'videos/coinTrack.mp4'
def convertVidFormat(output_file):
    command = ['ffmpeg', '-y', '-i', 'coinTrack.avi', '-vcodec', 'libx264', output_file]
    subprocess.run(command)


convertVidFormat(output_file)