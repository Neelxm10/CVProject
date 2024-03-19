import cv2 as cv
import numpy as np

def ransac(img, threshold, max_iterations, min_inline, framecnt, orig):
    #Collect number of edge points
    num_points = np.column_stack(np.where(img > 0))

    #check to ensure there are edge points present in the image.
    if len(num_points) == 0:
        print("No edge points found in the binary image.")
        return None

    #preallocate memory for variables such as best circle, max_inliers, and the accumulator array.
    accumulator = np.zeros_like(img, dtype=int)
    best_circle = None
    max_inliers = 0

    #Iterate through the desired number of RANSAC iterations
    for i in range(max_iterations):
        #randomly sample x-number of points. Best number of points is related to the accuracy of the RANSAC.
        sample_index = np.random.choice(len(num_points), size=3)
        sample_points = num_points[sample_index]

        #append the randomly sampled points
        xi, yi = sample_points[:, 1], sample_points[:, 0]

        #create a circle in parameter space around the sampled points.
        c = np.array([np.mean(xi), np.mean(yi)])
        r = np.mean(np.sqrt((xi - c[0]) ** 2 + (yi - c[1]) ** 2))

        #ensure that the sampled circles are within image bounds.
        if c[0] < img.shape[1] and  c[1] < img.shape[0] and 0 < r < min(img.shape[0], img.shape[1]) / 2:
            #in image space, a and b are the center of the circle. In parameter space, it will be the circular edge coordinates with distinct sample points.
            th = np.arange(0, 2 * np.pi, 0.01)
            a = c[0] + (r * np.cos(th))
            b = c[1] + (r * np.sin(th))

            #ensures that the generated circle coordinates are converted to integers, and any potential coordinates close to the image boundaries are clipped within a safe margin 
            #to prevent the circle from going outside the valid image region. 
            #This is crucial for subsequent operations, such as updating the accumulator with votes for the circle in the Hough space.
            margin = 5  # Adjust this margin as required (found experimentally)
            a_idx = np.clip(a.astype(int), 0 + margin, img.shape[1] - 1 - margin)
            b_idx = np.clip(b.astype(int), 0 + margin, img.shape[0] - 1 - margin)
            #Increment the accumulator at the circle coordinates
            accumulator[b_idx, a_idx] += 1

            # Non-maximal suppression: enhance local maxima in accumulator array (dilation), and  apply logical mask to accumulator array to only retain local maxima. 
            accumulator = cv.convertScaleAbs(accumulator)
            local_max = cv.dilate(accumulator, np.ones((3, 3)), iterations=1)
            lmax_mask = (local_max == accumulator)
            accumulator *= lmax_mask
    
    #Iterate through the coordinates of the local maxima in the parameter space (max_coords). 
    for max_coords in np.argwhere(accumulator > 0):
        
        #The radius and center of the circle are calculated based on the relationship between the sampled points (xi and yi) and the coordinates of the local maxima. 
        radius = np.mean(np.sqrt((xi - max_coords[1]) ** 2 + (yi - max_coords[0]) ** 2))
        center = (max_coords[1], max_coords[0])
        #Generate the coordinates of the circle and clip them to ensure they are within the image bounds
        th = np.arange(0, 2 * np.pi, 0.01)
        x_circle = (center[0] + radius * np.cos(th)).astype(int)
        y_circle = (center[1] + radius * np.sin(th)).astype(int)

        x_circle = np.clip(x_circle, 0, img.shape[1] - 1)
        y_circle = np.clip(y_circle, 0, img.shape[0] - 1)

    #Count the number of inliers (edge points inside the circle)
        inliers = np.sum(img[y_circle, x_circle] > 0)
    #if the circle meets the criteria for a valid circle (minimum inliers, radius within threshold, and more inliers than the current best),
    #update the best circle if needed
        if inliers >= min_inline and radius <= threshold and inliers > max_inliers:
            #print(f"Found Circle with radius {radius} px and center {center}")
            best_circle = (center, radius)
            max_inliers = inliers

    #if there is a best circle detected that satisfies all aformentioned criteria, visualize it and save it as an image. 
    if best_circle is not None:
        # Visualize the best circle
        circ = orig.copy()
        cv.circle(circ, best_circle[0], int(best_circle[1]), [0, 255, 0], 2)
        cv.circle(circ, best_circle[0], 5, [0, 0, 255], -1)
        cv.putText(circ, f'Center: ({best_circle[0][0]}, {best_circle[0][1]})', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1,
                   (0, 255, 255), 2)

        cv.imshow('Best Circle', circ)
        cv.imwrite(f"Frame_Dump/Best_Circle_Detected{framecnt}.png", circ)
        cv.waitKey(10)
        
    else:
        print("No circles found")

    return best_circle