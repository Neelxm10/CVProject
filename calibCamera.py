import cv2 as cv
import numpy as np
import glob

#PREWORK 
filedir = "calibration_data/"
def calibCamera(frame):
#kmeans clustering for determining corners
    crit = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 50, 0.00001)

    # Prepare object points in 3D space (pre-allocate based on checkerboard)
    objPoints = np.zeros((6*9, 3), np.float32)
    # Create a mesh grid based on checkerboard dimensions and flatten into a 2D array
    objPoints[:,:2] = np.mgrid[0:9, 0:6].T.reshape(-1,2)

    #now preallocate memory for object points and image points
    objPArray = []
    imgPArray = []


    #win_name="Verify"
    #cv.namedWindow(win_name, cv.WND_PROP_FULLSCREEN)
    #cv.setWindowProperty(win_name,cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)
   
    img = cv.imread(frame)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (9,6), None)
        # If found, add object points, image points (after refining them)
    if ret == True:
        # Refine the corners
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), crit)
        # Append the object points for this image
        objPArray.append(objPoints)
        imgPArray.append(corners2)
        # Draw and display the corners
        cv.drawChessboardCorners(img, (9,6), corners2, ret)
        img = cv.resize(img, (500,500))
        cv.imshow("verify", img)
        cv.waitKey(1500)
        
        imgMod = img       
        cv.destroyAllWindows()
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objPArray, imgPArray, gray.shape[::-1], None, None)
        print(mtx)
        #[fx 0 Cx]
        #[0 fy Cy]
        #[0  0  1]

        #Fetch the optimal camera parameters based on the camera matrix and the distortion coefficients
        h,  w = img.shape[:2]
        optimalmtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))



        #Now we take our images and undistort the image
        undistorted = cv.undistort(img, mtx, dist, None, optimalmtx)

        #using the roi found from the getOptimalNewCameraMatrix function. we apply a mask based on the roi to crop the image to the roi
        x, y, w, h = roi
        undistorted = undistorted[y: y+h, x: x+h]
        cv.imshow('distorted image?', undistorted)
    

        mean_error = 0
        for i in range(len(objPArray)):
            imgpoints2, _ = cv.projectPoints(objPArray[i], rvecs[i], tvecs[i], mtx, dist)
            error = cv.norm(imgPArray[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
            mean_error += error
 
        print( "total error: {}".format(mean_error/len(objPArray)))
        cv.waitKey(1500)
        cv.destroyAllWindows()
        np.save(filedir+'originalIntrinsic.npy', mtx)
        np.save(filedir+'optimalIntrinsic.npy', optimalmtx)
        np.save(filedir+'rvecs.npy', rvecs)
        np.save(filedir+'tvecs.npy', tvecs)
        np.save(filedir+'roi.npy', roi)
    else:
        print("No corners detected in frame:", frame)
        return None