import cv2 as cv
import numpy as np


def calculateXYZ(u, v):

    filename = 'calibration_data/'
    s  = np.load(filename+'scalingfactor.npy')
    newcam_mtx = np.load(filename+'optimalIntrinsic.npy')
    Pmtx = np.load(filename+'PMtx.npy')
    tvec = np.load(filename+'combinedTranslation.npy')
    RMtx = np.load(filename+'combinedRot.npy')
        #Solve: From Image Pixels, find World Points
    invCamMTX = np.linalg.inv(newcam_mtx)
    invR = np.linalg.inv(RMtx)
    uv_1=np.array([[u,v,1]], dtype=np.float32)
    uv_1=uv_1.T
    suv_1=s*uv_1
    xyz_c=invCamMTX.dot(suv_1)
    xyz_c=xyz_c-tvec
    XYZ=invR.dot(xyz_c)
    x, y, z = XYZ
    return x, y, z