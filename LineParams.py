'''This module defines two functions (getParams() and getLine()) that return
information about given points and about the line connecting those points.
To get a brief description of each function, use the following syntax:
    <module name as imported>.<function name>.__doc__'''

import math, random

def getParams(point1, point2):
    '''This function takes in two points and returns 5 values:
    (1) the difference in x-coordinates between the two points,
    (2) the difference in y-coordinates between the two points,
    (3) the distance between the two points,
    (4) the angle (measured in degrees) formed by the line connecting the two
    points and the y-axis pointing down from the first point, and
    (5) the quarter in the xy-plane in which the second point belongs, with the
    first point being the origin of that plane.
    The angle is between -180 and 180 degrees, with negative values denoting
    that the object is to the left of the y-axis, and positive values otherwise.'''
    # distance
    Xdiff = point1[0] - point2[0]
    Ydiff = point1[1] - point2[1]
    dist = math.sqrt(Xdiff**2 + Ydiff**2)
    if dist == 0:
        # the two points are the same --> can't compute angle
        angle, quarter = None, None
    else:
        # two different points --> can compute angle
        # angle measured in radians
        if point2[1] >= point1[1]:
            # bottom-right quarter of xy-plane
            angle = math.asin(abs(Xdiff)/dist)
        else:
            # top-right quarter of xy-plane
            angle = math.pi/2 + math.asin(abs(Ydiff)/dist)
        if point2[0] < point1[0]:
            # left of the y-axis
            angle *= -1
        # angle measured in degrees
        angle *= 180/math.pi
        # quarter in which second point belongs
        if angle >= 0:
            if angle <= 90:
                quarter = 1
            elif angle <= 180:
                quarter = 2
        else:
            if angle >= -90:
                quarter = 4
            elif angle >= -180:
                quarter = 3
    return Xdiff, Ydiff, dist, angle, quarter

def getLine(point0, point1):
    '''This function returns the slope of the line connecting two given points,
    along with the x-intercept and the y-intercept of that line.'''
    # difference in coordinates of the two given points
    Xdiff, Ydiff = getParams(point0, point1)[:2]
    if Xdiff == 0:   # line parallel to the y-axis --> undefined slope
        slope = None
    else:
        slope = Ydiff / Xdiff
    # x- and y-intercepts
    if slope == 0:   # line is parallel to the x-axis
        xIntercept = None
        yIntercept = point0[1]
    elif slope == None:   # line is parallel to the y-axis
        xIntercept = point0[0]
        yIntercept = None
    else:
        xIntercept = -point0[1] / slope + point0[0]
        yIntercept = slope * (-point0[0]) + point0[1]
    return slope, xIntercept, yIntercept
