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
    num_points = np.sum(img)
    #Accumulator array
    detected_circles= []
    for i in range(max_iterations):
        #pick three random sample points to get slope info
        sample_indices = np.random.choice(np.where(img > 0)[0], size=3, replace=False)
        sample_points = np.column_stack(np.unravel_index(np.flatnonzero(img), img.shape))[sample_indices]

        if num_points < 3:
            continue
        # Ensure the sampled points are distinct

        A, B, C = sample_points

                # Check if the points are collinear (denominator is zero)
        if (C[0] - B[0]) == 0:
            continue
        midABx, midABy = (A + B) / 2
        midBCx, midBCy = (B + C) / 2

        if (B[0] - A[0]) != 0:
            m_AB = (B[1] - A[1]) / (B[0] - A[0])
        else:
        # Handle the case when the denominator is zero
            m_AB = 0  # or any other appropriate value or action

        intAB = A[1] - m_AB * A[0]
        m_BC = (C[1] - B[1]) / (C[0] - B[0])
        intBC = B[1] - m_BC * B[0]

        m_midAB = -1.0*m_AB
        m_midBC = -1.0*m_BC
        intMidAB = midABy - (m_midAB * midABx)
        intMidBC = midBCy - (m_midBC * midBCx)

    if (m_midAB - m_midBC) != 0:
        centerX = (intMidBC - intMidAB) / (m_midAB - m_midBC)
    else:
    # Handle the case when the denominator is zero
        centerX = 0  # or any other appropriate value or action
        centerY = (m_midAB * centerX) -intMidAB

        center = np.array([centerX, centerY])

        diffradiusx, diffradiusy = center - A

        radius = np.sqrt((diffradiusx*diffradiusx)+(diffradiusy*diffradiusy))
        circumference = 2.0 * 3.14 * radius


        #Compute line distance
        dist = np.sqrt(np.sum((sample_points - center)**2) - radius)
        #print(str(dist)+ ' px\n')
        #identify inliers
        inline = img[dist < threshold]
        #print('test made it here \n')
        if len(inline) >= min_inline:
            detected_circles.append((center,radius))
            print('made it in here\n')
    return detected_circles