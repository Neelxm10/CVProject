import numpy as np
import cv2 as cv

#Load in initial camera calibration parameters
savedir = 'calibration_data/'

cam_mtx = np.load(savedir+'optimalIntrinsic.npy')
rvecs = np.load(savedir+'rvecs.npy')
tvecs = np.load(savedir+'tvecs.npy')



RotMtx, _ = cv.Rodrigues(rvecs[0])
print(RotMtx)