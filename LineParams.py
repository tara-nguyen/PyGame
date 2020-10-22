'''This module defines the following functions: getParams(), getLine(),
getDistToLine(), getIntersect(), isBetween(), and checkSide().
To get a brief description of each function, use the following syntax:
    <module name as imported>.<function name>.__doc__'''

import math, random

def getParams(point1, point2):
    '''This function takes in two points and returns five values:
    (1) the difference in x-coordinates between the two points,
    (2) the difference in y-coordinates between the two points,
    (3) the distance between the two points,
    (4) the angle (measured in degrees) formed by the line connecting
    the two points and the y-axis pointing down from the first point, and
    (5) the quarter in the xy-plane in which the second point belongs,
    with the first point being the origin of that plane.
    The angle is between -180 and 180 degrees, with negative values
    denoting that the object is to the left of the y-axis, and
    non-negative values otherwise.'''
    # distance
    Xdiff = point2[0] - point1[0]
    Ydiff = point2[1] - point1[1]
    dist = math.sqrt(Xdiff**2 + Ydiff**2)
    # angle (measured in degrees) and quarter
    if dist == 0:   # the two points are the same
        angle, quarter = None, None
    elif Ydiff == 0:   # the points form a horizontal line
        quarter = Xdiff / abs(Xdiff)
        angle = 90 * quarter
    else:
        angle = math.atan(Xdiff/Ydiff) * 180 / math.pi
        if angle >= 0:
            quarter = 1   # bottom-right quarter, unless Ydiff < 0
        else:
            quarter = -1   # bottom-left quarter, unless Ydiff < 0
        if Ydiff < 0:   # top-right and top-left quarters
            angle = (180 - abs(angle)) * -quarter
            quarter *= -2
    return Xdiff, Ydiff, dist, angle, quarter

def getLine(point1, point2):
    '''This function returns the coefficients in the line
    ax + by + c = 0 (a and b are not both zero) passing 
    through two given points.'''
    a, b = point2[1]-point1[1], point1[0]-point2[0]
    c = -a * point1[0] - b * point1[1]
    return a, b, c

def getDistToLine(point0, linePoint1, linePoint2):
    '''This function returns the distance from a point to a line.'''
    x0, x1, x2 = point0[0], linePoint1[0], linePoint2[0]
    y0, y1, y2 = point0[1], linePoint1[1], linePoint2[1]
    dNumer = abs((x2-x1)*(y1-y0) - (x1-x0)*(y2-y1))
    dDenom = getParams(linePoint1, linePoint2)[2]
    return dNumer / dDenom

def getIntersect(point1, point2, point3, point4):
    '''This function returns the coordinates of the intersection point
    of two lines, one formed by the first two given points (point1 and
    point2) and the other formed by the last two given points (point3
    and point4). The two lines are assumed to be separate lines.'''
    x1, x2, x3, x4 = point1[0], point2[0], point3[0], point4[0]
    y1, y2, y3, y4 = point1[1], point2[1], point3[1], point4[1]
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0:   # the lines are parallel to each other
        intersectX, intersectY = None, None
    else:
        det12 = x1 * y2 - y1 * x2
        det34 = x3 * y4 - x4 * y3
        xNumer = det12 * (x3 - x4) - (x1 - x2) * det34
        yNumer = det12 * (y3 - y4) - (y1 - y2) * det34
        intersectX, intersectY = xNumer/denom, yNumer/denom
    return intersectX, intersectY

def isBetween(point0, point1, point2):
    '''This function takes in three points on the same line and
    checks if one of them (point0) lies between the other two
    (point1 and point2).'''
    dist01 = getParams(point0, point1)[2]
    dist02 = getParams(point0, point2)[2]
    dist12 = getParams(point1, point2)[2]
    if dist01 <= dist12 and dist02 <= dist12:
        return True
    else:
        return False

def checkSide(point1, point2, linePoint1, linePoint2):
    '''This function checks if two given points (point1 and point2) are on
    the same side or different sides of the line connecting the other two
    given points (linePoint1 and linePoint2). The function returns:
    • 1 if point1 and point2 are on the same side of the line,
    • -1 if the points are on different sides of the line, or
    • 0 if at least one of the points is on the line.'''
    a, b, c = getLine(linePoint1, linePoint2)
    # plug point1 and point2 into the equation for the line
    f1 = a * point1[0] + b * point1[1] + c
    f2 = a * point2[0] + b * point2[1] + c
    if f1 == 0 or f2 == 0:
        return 0
    elif f1 * f2 > 0:
        return 1
    else:
        return -1
