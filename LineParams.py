'''This module defines the following functions: getParams(), getLine(),
getIntersect(), getDistToLine(), isBetween(), and checkSide().
To get a brief description of each function, use the following syntax:
    <module name as imported>.<function name>.__doc__'''

import math, random

def getParams(point1, point2):
    '''This function takes in two points and returns five values:
    (1) the difference in x-coordinates between the two points,
    (2) the difference in y-coordinates between the two points,
    (3) the distance between the two points,
    (4) the angle (measured in degrees) formed by the line connecting the
    two points and the y-axis pointing down from the first point, and
    (5) the quarter in the xy-plane in which the second point belongs, with
    the first point being the origin of that plane.
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
    '''This function returns the slope of the line connecting two given
    points, along with the y-intercept and the x-intercept of that line.'''
    # difference in coordinates of the two given points
    Xdiff, Ydiff = getParams(point1, point2)[:2]
    if Xdiff == 0:   # line parallel to the y-axis --> undefined slope
        slope = None
    else:
        slope = Ydiff / Xdiff
    # x- and y-intercepts
    if slope == None:   # line is parallel to the y-axis
        yIntercept, xIntercept = None, point1[0]
    elif slope == 0:   # line is parallel to the x-axis
        yIntercept, xIntercept = point1[1], None
    else:
        xIntercept = -point1[1] / slope + point1[0]
        yIntercept = slope * (-point1[0]) + point1[1]
    return slope, yIntercept, xIntercept

def getIntersect(point1, point2, point3, point4):
    '''This function returns the coordinates and angle (between 0 & 90 degrees)
    of the intersection of two lines, one formed by the first two given points
    (point1 and point2) and the other formed by the last two given points
    (point3 and point4). The two lines are assumed to be separate lines.'''
    slope1, yIntercept1, xIntercept1 = getLine(point1, point2)
    slope2, yIntercept2, xIntercept2 = getLine(point3, point4)
    if slope1 == slope2:   # the lines are parallel to each other
        intersectX, intersectY, angle = None, None, 0
    elif slope1 == None or slope2 == None:  # one line is parallel to the y-axis
        if slope1 == None:
            intersectX = xIntercept1
            intersectY = slope2 * intersectX + yIntercept2    
        else:
            intersectX = xIntercept2
            intersectY = slope1 * intersectX + yIntercept1
        angle = math.atan(abs((xIntercept1-xIntercept2)/intersectY))
    else:
        intersectX = (yIntercept2 - yIntercept1) / (slope1 - slope2)
        intersectY = slope1 * intersectX + yIntercept1
        if slope1 * slope2 == -1:   # the lines are perpendicular
            angle = math.pi   # measured in radians
        else:
            angle = math.atan(abs((slope1-slope2)/(1+slope1*slope2)))
    angle *= 180/math.pi   # measured in degrees
    return intersectX, intersectY, angle

def getDistToLine(point0, linePoint1, linePoint2):
    '''This function returns the distance from a point (point0) to a line,
    along with the differences in x- and y-coordinates between point0 and
    the intersection point of two lines: (1) the given line, and (2) the
    line perpendicular to that line and passing through point0.'''
    slope, yIntercept, xIntercept = getLine(linePoint1, linePoint2)
    if slope == None:   # line is parallel to the y-axis
        Xdiff, Ydiff = point0[0]-xIntercept, 0
        dist = abs(Xdiff)
    elif slope == 0:   # line is parallel to the x-axis
        Xdiff, Ydiff = 0, point0[1]-yIntercept
        dist = abs(Ydiff)
    else:
        # y-intercept of the line perpendicular to the given line 
        # and passing through point0
        yIntercept2 = point0[1] - (-1/slope) * point0[0]
        # intersection point of the two lines
        intersectX, intersectY = getIntersect(point0, (0,yIntercept2),
                                              linePoint1, linePoint2)[:2]
        # distance
        Xdiff, Ydiff, dist = getParams(point0, (intersectX,intersectY))[:3]
    return Xdiff, Ydiff, dist

def isBetween(point0, point1, point2):
    '''This function takes in three different points and checks if
    the points are only the same line, and if one of them (point0)
    lies between the other two (point1 and point2).'''
    isBetween = False
    if getDistToLine(point0, point1, point2)[2] == 0:
        # differences in coordinates
        Xdiff1, Ydiff1 = getParams(point0, point1)[:2]
        Xdiff2, Ydiff2 = getParams(point0, point2)[:2]
        if Xdiff1 == 0:   # line is parallel to the y-axis
            if Ydiff1 * Ydiff2 <= 0:
                isBetween = True
        else:
            if Xdiff1 * Xdiff2 <= 0:
                isBetween = True
    return isBetween

def checkSide(point1, point2, linePoint1, linePoint2):
    '''This function checks if two given points (point1 and point2) are on
    the same side or different sides of the line connecting the other two
    given points (linePoint1 and linePoint2). The function returns:
    • 1 if point1 and point2 are on the same side of the line,
    • -1 if the points are on different sides of the line, or
    • 0 if at least one of the points is on the line.'''
    # intersection of the given line and the line connecting point1 and point2
    intersectX, intersectY = getIntersect(point1, point2,
                                          linePoint1, linePoint2)[:2]
    if intersectX == None:   # the lines are parallel to each other
        return 1
    elif (intersectX,intersectY) == point1 or (intersectX,intersectY) == point2:
        return 0
    else:
        if isBetween((intersectX,intersectY), point1, point2):
            return -1
        else:
            return 1
