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
        A_idx, B_idx, C_idx = np.random.randint(0, num_points, size=3)
        A, B, C = img[A_idx], img[B_idx], img[C_idx]
        sample = img[A]
        #Check to ensure divide-by-zero does not occur
        if sample[0, 0] == sample[1, 0]:
            continue

        midABx, midABy = (A + B) / 2
        midBCx, midBCy = (B + C) / 2

        m_AB = (B[1] - A[1]) / (B[0] - A[0])
        intAB = A[1] - m_AB * A[0]
        m_BC = (C[1] - B[1]) / (C[0] - B[0])
        intBC = B[1] - m_BC * B[0]

        m_midAB = -1.0*m_AB
        m_midBC = -1.0*m_BC
        intMidAB = midABy - (m_midAB * midABx)
        intMidBC = midBCy - (m_midBC * midBCx)

        centerX = (intMidBC - intMidAB)/(m_midAB - m_midBC)
        centerY = (m_midAB * centerX) -intMidAB

        center = np.array[centerX, centerY]

        diffradiusx, diffradiusy = center - A

        radius = np.sqrt((diffradiusx*diffradiusx)+(diffradiusy*diffradiusy))
        circumference = 2.0 * 3.14 * radius

        #get straight line info from point to point y=mx+b
        #x1, y1 = sample[0]
        #x2, y2 = sample[1]
        #m = (y2-y1)/(x2-x1)
       # b = y1 - (m*x1)

        #Compute line distance
        dist = np.sqrt()
        print(str(dist)+ ' px\n')
        #identify inliers
        inline = img[dist < threshold]

        if len(inline >= min_inline):
            detected_lines.append((m,b))
    
    return detected_lines