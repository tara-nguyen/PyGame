'''This module defines three functions: getParams(), getLine(), and checkSide().
To get a brief description of each function, use the following syntax:
    <module name as imported>.<function name>.__doc__'''

import math, random

def getParams(point1, point2):
    '''This function takes in two points and returns five values:
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
    if dist == 0:   # the two points are the same --> can't compute angle
        angle, quarter = None, None
    else:
        if point2[1] >= point1[1]:   # bottom-right quarter of xy-plane
            quarter = 1
            angle = math.asin(abs(Xdiff)/dist)
        else:   # top-right quarter of xy-plane
            quarter = 2
            angle = math.pi/2 + math.asin(abs(Ydiff)/dist)
        if point2[0] < point1[0]:   # left of the y-axis
            quarter *= -1
            angle *= -1
        angle *= 180/math.pi   # angle measured in degrees
    return Xdiff, Ydiff, dist, angle, quarter

def getLine(point1, point2):
    '''This function returns the slope of the line connecting two given points,
    along with the x-intercept and the y-intercept of that line.'''
    # difference in coordinates of the two given points
    Xdiff, Ydiff = getParams(point1, point2)[:2]
    if Xdiff == 0:   # line parallel to the y-axis --> undefined slope
        slope = None
    else:
        slope = Ydiff / Xdiff
    # x- and y-intercepts
    if slope == 0:   # line is parallel to the x-axis
        xIntercept = None
        yIntercept = point1[1]
    elif slope == None:   # line is parallel to the y-axis
        xIntercept = point1[0]
        yIntercept = None
    else:
        xIntercept = -point1[1] / slope + point1[0]
        yIntercept = slope * (-point1[0]) + point1[1]
    return slope, xIntercept, yIntercept

def checkSide(point1, point2, linePoint1, linePoint2):
    '''This function checks if two given points are on the same side or
    different sides of the line connecting the other two given points.
    The former two points are on the same side of the line if the value
    returned by the function is positve, and are on different sides if the
    value is negative.
    If the function returns 0, at least one of the points is on the line.'''
    d = []
    for point in (point1, point2):
        d.append((point[0]-linePoint1[0])*(linePoint2[1]-linePoint1[1])-\
                 (point[1]-linePoint1[1])*(linePoint2[0]-linePoint1[0]))
    return d[0] * d[1]
