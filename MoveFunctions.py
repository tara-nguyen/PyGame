import pygame, math
import LineParams as line

def update(screen, things, thingsPos, moved, newCenterPos, rotate=False):
    '''This function redraws things on the screen to show movements.
    things is a list of objects on the screen.
    thingsPos is a list of the positions of the objects.
    moved is a tuple/list of objects that will be moved after the redrawing, 
    along with the original surfaces containing the moved objects at the 
    beginning of the program.
    newCenterPos is a tuple/list of the new coordinates of the moved objects' 
    center points after being redrawn.
    rotate, if specified, is a tuple/list of the angles (measured in degrees) by 
    which the moved objects will rotate. The default is that there is no change
    from the original rotation.'''
    # create 2 separate lists, one for the moved objects and the other for
    # their original surfaces
    objMoved = []
    objOrig = []
    for i in range(0, int(len(moved)/2)):
        objMoved.append(moved[i])
    for i in range(int(len(moved)/2), len(moved)):
        objOrig.append(moved[i])
    numMoved = len(objMoved)   # number of objects to be moved
    # check to see which objects in the list things are also in objMoved
    movedFound = []
    numThings = len(things)   # number of objects to be redrawn
    for i in range(numThings):
        movedFound.append({i:[]})
        for j in range(numMoved):
            if things[i] == objMoved[j]:
                movedFound[i][i].append(j)
            else:
                movedFound[i][i].append('no match')
##    print('movedFound',movedFound)
    # count number moved objects found in things
    count = [0] * numThings
    for i in range(numThings):
        for j in range(numMoved):
            if movedFound[i][i][j] != 'no match':
                count[i] += 1
##    print('count movedFound',count)
##    print()
    # redraw objects
    thingsRedrawn = [0] * numThings
    objMovedRedrawn = [0] * numMoved
    for i in range(numThings):
##        print('i=',i)
        if count[i] == 0:
            # unmoved object
            screen.blit(things[i], thingsPos[i])
            thingsRedrawn[i] += 1
##            print('thingsRedrawn',thingsRedrawn)
        else:
            # moved object
            for j in range(numMoved):
                if thingsRedrawn[i] == 0 and objMovedRedrawn[j] == 0:
##                    print('j=',j)
                    # object hasn't been redrawn
                    if movedFound[i][i][j] != 'no match':
                        if rotate != False:
                            # rotate object
                            things[i] = pygame.transform.rotate(objOrig[j],
                                                                rotate[j])
                        # new center point and new position
                        newCenter = things[i].get_rect().center
                        thingsPos[i] = (newCenterPos[j][0]-newCenter[0],
                                        newCenterPos[j][1]-newCenter[1])
                        screen.blit(things[i], thingsPos[i])   # object redrawn
                        thingsRedrawn[i] += 1
                        objMovedRedrawn[j] += 1
##                        print('thingsRedrawn',thingsRedrawn)
##                        print('objMovedRedrawn',objMovedRedrawn)
                        break
 
def moveCircle(rotCenter, currentCenterPos, direction,
               step=10, maxRotation=False,
               boundaryX=False, boundaryY=False, objCenter=False):
    '''This function rotates an object along an imaginary circle.
    rotCenter is the point around which the object moves.
    currentCenterPos refers to the current coordinates of the object's center.
    step is the change in the angle (measured in degrees) by which the object
    will move at each keypress.
    maxRotation is the maximum angle (measured in degrees) to which the object
    is allowed to move. Assign the argument a numerical value between -180 and
    180 to set a limit.
    boundaryX and boundaryY are lists representing the vertical and lateral
    ranges, respectively, of the area in which the object is allowed to move.
    objCenter is the object's center point.'''
    # check boundaries
    if boundaryX != False and objCenter != False:
        boundaryX[0] += objCenter[0]   # smallest possible x (left boundary)
        boundaryX[1] -= objCenter[0]   # largest possible x (right boundary)
    if boundaryY != False and objCenter != False:
        boundaryY[0] += objCenter[1]   # smallest possible y (upper boundary)
        boundaryY[1] -= objCenter[1]   # largest possible y (lower boundary)
    # radius, current angle (measured in degrees), and current quarter
    r, currentAngle, quarter = line.getParams(rotCenter, currentCenterPos)[2:]
    # check direction
    if direction == 'counterclockwise' or direction == 'right':
        if maxRotation != False:
            if currentAngle >= maxRotation:
                # object has reached maximum rotation --> stop moving
                step = 0
            elif step >= maxRotation - currentAngle:
                # final step before reaching maximum rotation
                step = maxRotation - currentAngle
        if boundaryX != False:
            if quarter == 1 and currentCenterPos[0] >= boundaryX[1]:
                # object has reached boundary --> stop moving
                step = 0
            elif quarter == 3 and currentCenterPos[0] <= boundaryX[0]:
                # object has reached boundary --> stop moving
                step = 0
        if boundaryY != False:
            if quarter == 2 and currentCenterPos[1] <= boundaryY[0]:
                # object has reached boundary --> stop moving
                step = 0
            elif quarter == 4 and currentCenterPos[1] >= boundaryY[1]:
                # object has reached boundary --> stop moving
                step = 0
    elif direction == 'clockwise' or direction == 'left':
        step *= -1
        if maxRotation != False:
            if currentAngle <= maxRotation:
                # object has reached maximum rotation --> stop moving
                step = 0
            elif step <= maxRotation - currentAngle:
                # final step before reaching maximum rotation
                step = maxRotation - currentAngle
        if boundaryX != False:
            if quarter == 2 and currentCenterPos[0] >= boundaryX[1]:
                # object has reached boundary --> stop moving
                step = 0
            elif quarter == 4 and currentCenterPos[0] <= boundaryX[0]:
                # object has reached boundary --> stop moving
                step = 0
        if boundaryY != False:
            if quarter == 1 and currentCenterPos[1] >= boundaryY[1]:
                # object has reached boundary --> stop moving
                step = 0
            elif quarter == 3 and currentCenterPos[1] <= boundaryY[0]:
                # object has reached boundary --> stop moving
                step = 0
    else:
        print('Invalid direction.')
    rotate = currentAngle + step   # new angle (measured in degrees)
    # check if the object has gone past the negative side of the y-axis
    if rotate > 180:
        rotate -= 360
    elif rotate < -180:
        rotate += 360
    rotateRad = rotate * math.pi/180   # new angle (measured in radians)
    # coordinates of new center of the object, relative to the screen
    newX = rotCenter[0] + r * math.sin(rotateRad)
    newY = rotCenter[1] + r * math.cos(rotateRad)
    newCenterPos = newX, newY
    return newCenterPos, rotate

def moveStraight(center, currentCenterPos, direction, stepX=10, stepY=10,
                 boundaryX=False, boundaryY=False):
    '''This function moves an object on a straight line.
    center is the object's center point.
    currentCenterPos refers to the current coordinates of the object's center.
    For each movement, stepX is the number of pixels by which the object will
    move horizontally, and stepY is the number of pixels by which the object
    will move vertically.
    boundaryX and boundaryY are lists representing the vertical and lateral
    ranges, respectively, of the area in which the object is allowed to move.
    objCenter is the object's center point.'''
    # check boundaries
    if boundaryX != False:
        boundaryX[0] += center[0]   # smallest possible x (left boundary)
        boundaryX[1] -= center[0]   # largest possible x (right boundary)
    if boundaryY != False:
        boundaryY[0] += center[1]   # smallest possible y (upper boundary)
        boundaryY[1] -= center[1]   # largest possible y (lower boundary)
    # check direction
    if direction == 'up':
        stepX = 0   # no lateral movement
        stepY *= -1   # negative step
        rotate = 0   # new angle (measured in degrees)
        if boundaryY != False:
            if currentCenterPos[1] <= boundaryY[0]:
                # object has reached boundary --> stop moving
                stepY = 0
            elif stepY <= boundaryY[0] - currentCenterPos[1]:
                # final step before reaching boundary
                stepY = boundaryY[0] - currentCenterPos[1]
    elif direction == 'down':
        stepX = 0   # no lateral movement
        rotate = 180   # new angle (measured in degrees)
        if boundaryY != False:
            if currentCenterPos[1] >= boundaryY[1]:
                # object has reached boundary --> stop moving
                stepY = 0
            elif stepY >= boundaryY[1] - currentCenterPos[1]:
                # final step before reaching boundary
                stepY = boundaryY[1] - currentCenterPos[1]
    elif direction == 'left':
        stepX *= -1   # negative step
        stepY = 0   # no vertical movement
        rotate = 90   # new angle (measured in degrees)
        if boundaryX != False:
            if currentCenterPos[0] <= boundaryX[0]:
                # object has reached boundary --> stop moving
                stepX = 0
            elif stepX <= boundaryX[0] - currentCenterPos[0]:
                # final step before reaching boundary
                stepX = boundaryX[0] - currentCenterPos[0]
    elif direction == 'right':
        stepY = 0   # no vertical movement
        rotate = -90   # new angle (measured in degrees)
        if boundaryX != False:
            if currentCenterPos[0] >= boundaryX[1]:
                # object has reached boundary --> stop moving
                stepX = 0
            elif stepX >= boundaryX[1] - currentCenterPos[0]:
                # final step before reaching boundary
                stepX = boundaryX[1] - currentCenterPos[0]
    else:
        print('Invalid direction.')
    # coordinates of new center of the object, relative to the screen
    newCenterPos = currentCenterPos[0]+stepX, currentCenterPos[1]+stepY
    return newCenterPos, rotate

def moveToPoint(endPoint, currentCenterPos, endAngle=0, speedBoost=1):
    '''This function moves an object to a specified end point.
    currentCenterPos refers to the current coordinates of the object's center.
    endAngle refers to the direction the front of the object will face after the
    object has reached the end point. The default has the object facing upward.
    speedBoost adjusts the step size and must not be negative.'''
    if endPoint == currentCenterPos:
        # object has reached end point --> stop moving and rotate to end angle
        stepX = 0
        stepY = 0
        rotate = endAngle   # measured in degrees
    else:
        # distance from end point and current angle (measured in degrees)
        Xdiff, Ydiff, dist, currentAngle = line.getParams(endPoint,
                                                          currentCenterPos)[:4]
        # step size
        stepX = Xdiff
        stepY = Ydiff
        stepDiag = dist   # total travel distance per step
        while stepDiag > 10.001:
            stepX /= 1.0001
            stepY /= 1.0001
            stepDiag = math.sqrt(stepX**2 + stepY**2)
        stepX *= abs(speedBoost)
        stepY *= abs(speedBoost)
        rotate = currentAngle   # angle not changed
        if abs(Xdiff) <= abs(stepX) or abs(Ydiff) <= abs(stepY):
            # final step before reaching the end point
            stepX = Xdiff
            stepY = Ydiff
            rotate = endAngle
    # coordinates of new center of the object, relative to the screen
    newCenterPos = currentCenterPos[0]+stepX, currentCenterPos[1]+stepY
    return newCenterPos, rotate
