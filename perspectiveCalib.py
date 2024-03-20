import numpy as np
import cv2 as cv

#Load in initial camera calibration parameters
savedir = 'calibration_data/'

cam_mtx = np.load(savedir+'optimalIntrinsic.npy')
rvecs = np.load(savedir+'rvecs.npy')
tvecs = np.load(savedir+'tvecs.npy')
#print(rvecs)

# Initialize an identity matrix to accumulate rotations
combined_rotation_matrix = np.eye(3)
print(combined_rotation_matrix)

# Initialize a zero vector to accumulate translations
combined_translation_vector = np.zeros((1,3, 1))
# Loop through each rotation vector
for rvec, tvec in zip(rvecs, tvecs):
    # Convert rotation vector to rotation matrix using Rodrigues formula
    rotation_matrix, _ = cv.Rodrigues(rvec)
    # Accumulate rotations by multiplying rotation matrices
    combined_rotation_matrix = np.dot(combined_rotation_matrix, rotation_matrix)
    combined_translation_vector += tvec
print("combined rotation matrix from all sample frames")
print(combined_rotation_matrix)
print("combined translation vector")
print(combined_translation_vector)
# Construct transformation matrix using cv.composeRT()
# Note: The composeRT function expects translation vector in shape (3, 1), not (1, 3, 1)
combined_translation_vector = combined_translation_vector.reshape(3, 1)
transform_matrix = np.hstack((combined_rotation_matrix, combined_translation_vector))

print("testing print of extrinsic parameters: ")
print(transform_matrix)

ProjectionMtx = cam_mtx.dot(transform_matrix)
print(ProjectionMtx)

#to find scaling factor
nickel_d = 21.2 #mm
nick_radius = nickel_d/2

pixel_radius = 43.1

s = pixel_radius/nick_radius

#
print(s)
np.save(savedir+'scalingfactor.npy', s)
np.save(savedir+'RT.npy', transform_matrix)
np.save(savedir+'PMtx.npy', ProjectionMtx)
np.save(savedir+'combinedRot.npy', combined_rotation_matrix)
np.save(savedir+'combinedTranslation.npy', combined_translation_vector)

