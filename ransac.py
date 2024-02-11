import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv
#img = binary image with only edges
#threshold = depends on noise level in the image, the lower the stricter it is
#max_iterations = how many times you want the algo to repeat
#min_inline = the minimum number of lines that need to intersect for a line to be valid



def ransac(img, threshold, max_iterations, min_inline):
    #Preallocate variables
    best_fit = None
    best_inliers = 0
    num_points = np.column_stack(np.where(img > 0))
    # Accumulator array
    accumulator = np.zeros_like(img, dtype=int)
    for i in range(max_iterations):
        #pick three random sample points to get slope info
        sample_index = np.random.choice(len(num_points)-1)
        xi, yi = num_points[sample_index]
    
        #print("Random px coords: x: "+str(xi)+",  y: "+str(yi)+" (px)\n")

        # Ensure the sampled points are distinct
        th = np.arange(0, 2*np.pi, 0.01)

        #Make the randomly sampled points the center and build radius off center
        c = np.array([np.mean(xi), np.mean(yi)])
        r = np.mean(np.sqrt((xi - np.mean(xi))**2 + (yi - np.mean(yi))**2))

        #in image space a,b is the center of the circle. In parameter space, it will be the circular edge coordiantes
        a = c[0] + (r * np.cos(th))
        b = c[1] + (r * np.sin(th))

        #for the accumulator array we ensure index bounds do not exceed image size
        a_idx = np.clip(a.astype(int), 0, img.shape[1] - 1)
        b_idx = np.clip(b.astype(int), 0, img.shape[0] - 1)
        accumulator[a_idx, b_idx] += 1

        # Find the maximum value (peak) and its index in the accumulator array
        max_value = accumulator[0, 0]
        max_coords = (0, 0)
        for i in range(accumulator.shape[0]):
            for j in range(accumulator.shape[1]):
                if accumulator[i, j] > max_value:
                    max_value = accumulator[i, j]
                    max_coords = (i, j)


      # Calculate radius based on the randomly sampled edge points and maximum coordinates
        radius = np.mean(np.sqrt((xi - max_coords[0])**2 + (yi - max_coords[1])**2))
        Center = (max_coords[1], max_coords[0])

        # Count inliers by checking the number of edge points inside the circle
        inliers = 0
        for k in th:
            x = int(Center[0] + radius * np.cos(k))
            y = int(Center[1] + radius * np.sin(k))
            # Ensure indices are within image bounds
            x = np.clip(x, 0, img.shape[1] - 1)
            y = np.clip(y, 0, img.shape[0] - 1)
            if img[y, x] > 0:
                inliers += 1

        #User defines minimum number of edge points to be fit
        if inliers > min_inline:
            # If enough inliers, adjust threshold dynamically
            threshold *= 0.9  # You can adjust this scaling factor based on your needs
        else:
            # If not enough inliers, increase threshold
            threshold *= 1.1
        
        if radius <= threshold:
            #draw circle
            circ = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
            #print(f"Found Circle with radius {radius} px and center {Center}")
            cv.circle(circ, Center, int(radius), [0, 255, 0], 2)
            cv.circle(circ, Center, 5, [0, 0, 255], -1)  # Draw center in green
            cv.imshow('Object Tracker', circ)
            cv.waitKey(20)
        else:
            continue
