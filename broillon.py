import random
import math
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
Circle = namedtuple('Circle', ['xCenter', 'yCenter', 'radius'])

iterations = # Define the number of iterations
edgePoints = # Define the list of edge points
center = # Define the center point
radius = # Define the radius
radiusThreshold = # Define the radius threshold
circumference = # Define the circumference
onCircle = []
notOnCircle = []
bestCircles = []

for i in range(iterations):
    A = edgePoints[random.randint(0, len(edgePoints))]
    B = edgePoints[random.randint(0, len(edgePoints))]
    C = edgePoints[random.randint(0, len(edgePoints))]
    
    midpt_AB = Point((A.x + B.x) / 2, (A.y + B.y) / 2)
    midpt_BC = Point((B.x + C.x) / 2, (B.y + C.y) / 2)
    
    slope_AB = (B.y - A.y) / (B.x - A.x + 1e-10)
    intercept_AB = A.y - slope_AB * A.x
    slope_BC = (C.y - B.y) / (C.x - B.x + 1e-10)
    intercept_BC = B.y - slope_BC * B.x
    
    slope_midptAB = -1.0 / slope_AB
    slope_midptBC = -1.0 / slope_BC
    intercept_midptAB = midpt_AB.y - slope_midptAB * midpt_AB.x
    intercept_midptBC = midpt_BC.y - slope_midptBC * midpt_BC.x

for i in range(len(edgePoints)):
    diffCenter = Point(edgePoints[i].x - center.x, edgePoints[i].y - center.y)
    distanceToCenter = math.sqrt(diffCenter.x**2 + diffCenter.y**2)
    if abs(distanceToCenter - radius) < radiusThreshold:
        onCircle.append(i)
    else:
        notOnCircle.append(i)

if len(onCircle) >= circumference:
    circleFound = Circle(center.x, center.y, radius)
    toKeep = [edgePoints[i] for i in notOnCircle]
    edgePoints = toKeep
    bestCircles.append(circleFound)

if len(edgePoints) < 100:
    pass  # This would be a 'break' in a loop, but it's not clear from the context.

def drawCircles(img, bestCircles, limit):
    import cv2
    result = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    for i in range(limit):
        cv2.circle(result, (bestCircles[i].xCenter, bestCircles[i].yCenter),
                   bestCircles[i].radius, (0, 255, 255), 3)
    return result






#record point of each pixel of the edge !=0