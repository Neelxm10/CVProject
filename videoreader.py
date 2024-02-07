import cv2 as cv
from matplotlib import pyplot as py
import numpy as np
import os
## Import Sample video
filename = "lexusis300.mov"
capture = cv.VideoCapture(filename)

#frame counter initialization
framecnt = 0
os.mkdir('Frame_Dump')
while (capture.isOpened()):
    state,frame = capture.read()
    if state:
        cv.imshow('video reader', frame)
        cv.imwrite('Frame_Dump/Frame'+str(framecnt)+ '.png', frame)
        framecnt+=1
        print('Print....FrameCount:'+str(framecnt)+'\n')
        cv.waitKey(20)
    else:
        break




cv.destroyAllWindows()