import math, random

def getParams(point1, point2):
    '''This function takes in two points and returns 5 values:
    (1) the difference in x-coordinates between the two points,
    (2) the difference in y-coordinates between the two points,
    (3) the distance between the two points,
    (4) the angle (measured in degrees) formed by the line connecting the two
    points and the y-axis pointing down from the first point, and
    (5) the quarter in the xy-plane in which the second point belongs.
    The angle is between -180 and 180 degrees, with negative values denoting
    that the object is to the left of the y-axis, and positive values otherwise.'''
    # distance
    Xdiff = point1[0] - point2[0]
    Ydiff = point1[1] - point2[1]
    dist = math.sqrt(Xdiff**2 + Ydiff**2)
    if dist == 0:
        # the two points are the same --> can't compute angle
        currentAngle, quarter = False, False
    else:
        # two different points --> can compute angle
        # angle measured in radians
        if point2[1] >= point1[1]:
            # bottom-right quarter of xy-plane
            currentAngle = math.asin(abs(Xdiff)/dist)
        else:
            # top-right quarter of xy-plane
            currentAngle = math.pi/2 + math.asin(abs(Ydiff)/dist)
        if point2[0] < point1[0]:
            # left of the y-axis
            currentAngle *= -1
        # angle measured in degrees
        currentAngle *= 180/math.pi
        # quarter in which second point belongs
        if currentAngle >= 0:
            if currentAngle <= 90:
                quarter = 1
            elif currentAngle <= 180:
                quarter = 2
        else:
            if currentAngle >= -90:
                quarter = 4
            elif currentAngle >= -180:
                quarter = 3
    return Xdiff, Ydiff, dist, currentAngle, quarter

def getLine(point0, point1, slope=False, point2X=False, point2Y=False):
    '''This function returns information about a line connecting two
    given points:
    (1) the slope,
    (2) the x-intercept,
    (3) the y-intercept,
    (4) the coordinates of a random point on the line, which, together with one
    of the given points, lies on opposite sides of the vertical line passing
    through the other given point, and
    (5) the coordinates of another point on the line, whose one of the
    coordinates is already given in the arguments (either point2X or point2Y).'''
    # difference in coordinates of the two given points
    Xdiff, Ydiff = getParams(point0, point1)[:2]
    # slope of line, if not given in the arguments
    if slope == False:
        slope = Ydiff / Xdiff
    # x- and y-intercepts
    if slope != 0:
        xIntercept = -point0[1] / slope + point0[0]
    else:
        # line is parallel to x-axis
        xIntercept = False
    yIntercept = slope * (-point0[0]) + point0[1]
    # random point on the line
    randomNum = random.uniform(1., 2.)
    randomPoint = point1[0]-Xdiff*randomNum, point1[1]-Ydiff*randomNum
    # another point on the line
    if point2X == False and point2Y != False:
        point2X = point2Y-point0[1] / slope + point0[0]
    if point2Y == False and point2X != False:
        point2Y = slope * (point2X-point0[0]) + point0[1]
    point2 = point2X, point2Y
    return slope, xIntercept, yIntercept, randomPoint, point2
