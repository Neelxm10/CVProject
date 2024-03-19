import cv2 as cv
import subprocess


cap = cv.VideoCapture(2)
####################################READ INPUT VIDEO STREAM###########################################
state,frame = cap.read()
h, w = frame.shape[:2]
output = cv.VideoWriter("testVid.avi", cv.VideoWriter_fourcc(*'MPEG'), 30, (w, h)) 
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

output_file = 'testCAM1.mp4'
def convertVidFormat(output_file):
    command = ['ffmpeg', '-y', '-i', 'testVid.avi', '-vcodec', 'libx264', output_file]
    subprocess.run(command)


convertVidFormat(output_file)

cap2 = cv.VideoCapture(0)
####################################READ INPUT VIDEO STREAM###########################################
state1,frame2 = cap2.read()
h, w = frame2.shape[:2]
output2 = cv.VideoWriter("testVid2.avi", cv.VideoWriter_fourcc(*'MPEG'), 30, (w, h)) 
while cap.isOpened():
    state, frame = cap.read()
    if state == True:
        output2.write(frame)
        cv.imshow('video feed 2',frame2)
        #press s to save video
        if cv.waitKey(1) & 0xFF == ord('q'): 
            break
output2.release()  
cap2.release()    
cv.destroyAllWindows()
output_file2 = 'testCAM2.mp4'
def convertVidFormat2(output_file):
    command = ['ffmpeg', '-y', '-i', 'testVid2.avi', '-vcodec', 'libx264', output_file]
    subprocess.run(command)


convertVidFormat2(output_file2)

