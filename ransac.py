import numpy as np
from matplotlib import pyplot as plt
#img = binary image with only edges
#threshold = depends on noise level in the image, the lower the stricter it is
#max_iterations = how many times you want the algo to repeat
#min_inline = the minimum number of lines that need to intersect for a line to be valid



def ransac(img, threshold, max_iterations, min_inline):
    #Preallocate variables
    best_fit = None
    best_inliers = 0
    num_points = len(img)
    #Accumulator array
    detected_lines = []
    for i in range(max_iterations):
        #pick two random sample points to get slope info
        sample_ind = np.random.randint(0, num_points, size=2)
        sample = img[sample_ind]
        #Check to ensure divide-by-zero does not occur
        if sample[0, 0] == sample[1, 0]:
            continue
        #get straight line info from point to point y=mx+b
        x1, y1 = sample[0]
        x2, y2 = sample[1]
        m = (y2-y1)/(x2-x1)
        b = y1 - (m*x1)

        #Compute line distance
        dist = np.abs(img[:,1] - (m*img[:,0]+b))

        #identify inliers
        inline = img[dist < threshold]

        if len(inline >= min_inline):
            detected_lines.append((m,b))
    
    return detected_lines