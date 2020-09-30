'''The following classes are defined: Movement, Straight, Circle, and ToPoint.
To get a brief description of each class, use the following syntax:
    <module name as imported>.<class name>.__doc__
One function, update(), is also defined at the end of the program. To get a
brief description, use the following syntax:
    <module name as imported>.update.__doc__'''

import pygame, math
import LineParams as line

class Movement:
    '''This class has one method: setBoundaries.
    To get a brief description of the method, use the following syntax:
        <module name as imported>.Movement.setBoundaries.__doc__'''

    def setBoundaries(objCenter, screenSize):
        '''This function sets the boundaries of the area in which an object is
        allowed to move.
        objCenter is the object's center point.
        screenSize is a tuple containing the width and height of the screen.'''
        boundaryLeft = objCenter[0]
        boundaryRight = screenSize[0] - objCenter[0]
        boundaryTop = objCenter[1]
        boundaryBottom = screenSize[1] - objCenter[1]
        
class Straight:
    '''This class has the following methods: setStep, setFinalStep,
    reachedBoundaries, and move.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Straight.<method name>.__doc__'''

    def setFinalStep(direction, stepX, stepY, centerPos):
        '''This function checks if a moving object is about to reach one of the
        screen boundaries, and sets the final step accordingly.
        stepX and stepY are the lateral and vertical step sizes, respectively,
        before making the final step.
        centerPos is the coordinates of the object's center.'''
        if direction == 'left' and stepX <= boundaryLeft - centerPos[0]:
            stepX = boundaryLeft-centerPos[0]
        if direction == 'right' and stepX >= boundaryRight - centerPos[0]:
            stepX = boundaryRight-centerPos[0]
        if direction == 'up' and stepY <= boundaryTop - centerPos[1]:
            stepY = boundaryTop-centerPos[1]
        if direction == 'down' and stepY >= boundaryBottom - centerPos[1]:
            stepY = boundaryBottom-centerPos[1]
        if direction == 'up left':
            if stepX <= boundaryLeft - centerPos[0]:
                stepX = boundaryLeft-centerPos[0]
            if stepY <= boundaryTop - centerPos[1]:
                stepY = boundaryTop-centerPos[1]
        if direction == 'up right':
            if stepX >= boundaryRight - centerPos[0]:
                stepX = boundaryRight-centerPos[0]
            if stepY <= boundaryTop - centerPos[1]:
                stepY = boundaryTop-centerPos[1]
        if direction == 'down left':
            if stepX <= boundaryLeft - centerPos[0]:
                stepX = boundaryLeft-centerPos[0]
            if stepY >= boundaryBottom - centerPos[1]:
                stepY = boundaryBottom-centerPos[1]
        if direction == 'down right':
            if stepX >= boundaryRight - centerPos[0]:
                stepX = boundaryRight-centerPos[0]
            if stepY >= boundaryBottom - centerPos[1]:
                stepY = boundaryBottom-centerPos[1]
        return stepX, stepY

    def reachedBoundaries(direction, centerPos):
        '''This function checks if a moving object has gone or will be going
        beyond the screen boundaries.
        centerPos is the coordinates of the object's center.'''
        if direction == 'left':
            if centerPos[0] <= boundaryLeft:
                return True
            else:
                return False
        elif direction == 'right':
            if centerPos[0] >= boundaryRight:
                return True
            else:
                return False
        elif direction == 'up':
            if centerPos[1] <= boundaryTop:
                return True
            else:
                return False
        elif direction == 'down':
            if centerPos[1] >= boundaryBottom:
                return True
            else:
                return False
        elif direction == 'up left':
            if centerPos[0] <= boundaryLeft or \
               centerPos[1] <= boundaryTop:
                return True
            else:
                return False
        elif direction == 'up right':
            if centerPos[0] >= boundaryRight or \
               centerPos[1] <= boundaryTop:
                return True
            else:
                return False
        elif direction == 'down left':
            if centerPos[0] <= boundaryLeft or \
               centerPos[1] >= boundaryBottom:
                return True
            else:
                return False
        elif direction == 'down right':
            if centerPos[0] >= boundaryRight or \
               centerPos[1] >= boundaryBottom:
                return True
            else:
                return False

    def move(direction, centerPos, stepX=10, stepY=10,
             screenSize=None, objCenter=None):
        '''This function moves an object on a straight line.
        centerPos is the coordinates of the object's center point.
        stepX and stepY are the lateral and vertical step sizes, respectively.
        objCenter is the object's center point, only specified if screenSize
        is specified.'''
        if direction == 'left':
            # negative lateral step size; no vertical movement
            stepX, stepY = -stepX, 0
            rotate = 90   # new angle (measured in degrees)
        elif direction == 'right':
            stepY = 0   # no vertical movement
            rotate = -90   # new angle (measured in degrees)
        elif direction == 'up':
            # no lateral movement; negative vertical step size
            stepX, stepY = 0, -stepY
            rotate = 0   # new angle (measured in degrees)
        elif direction == 'down':
            stepX = 0   # no lateral movement
            rotate = 180   # new angle (measured in degrees)
        else:   # diagonal movement
            if direction == 'up left':
                # negative lateral and vertical step sizes
                stepX, stepY = -stepX, -stepY
                rotate = 45   # new angle (measured in degrees)
            elif direction == 'up right':
                stepY = -stepY   # negative vertical step size
                rotate = -45   # new angle (measured in degrees)
            elif direction == 'down left':
                stepX = -stepX   # negative lateral step size
                rotate = 135   # new angle (measured in degrees)
            elif direction == 'down right':
                rotate = -135   # new angle (measured in degrees)
        if screenSize != None:
            # set boundaries
            Movement.setBoundaries(objCenter, screenSize)
            # set final step before reaching boundary
            stepX, stepY = setFinalStep(direction, stepX, stepY, centerPos)
            # stop moving if object has reached one of the screen boundaries
            if reachedBoundaries(direction, centerPos):
                stepX, stepY = 0, 0
        # new coordinates of the object's center
        newCenterPos = centerPos[0]+stepX, centerPos[1]+stepY
        return newCenterPos, rotate

class Circle:
    '''This class has the following methods: checkMaxRot, setFinalStep,
    reachedBoundaries, setRot, setNewPos, and move.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Circle.<method name>.__doc__'''

    def checkMaxRot(angle, maxRot):
        '''This function checks if a moving object has gone or will be going
        beyond the maximum rotation allowed.
        angle is the angle (measured in degrees) formed by two lines:
        (1) the line connecting the object's center point and the point around
        which it moves, and
        (2) the positive y-axis pointing downward from the latter point.
        maxRot is the maximum angle (between 0 and 180 degrees) to which the
        object is allowed to move.'''
        # make sure maxRot is between 0 and 180 degrees
        if maxRot < 0:
            while abs(maxRot) > 180:
                maxRot += 360
        elif maxRot > 180:
            while maxRot > 180:
                maxRot -= 360
        maxRot = abs(maxRot)
        # check angle and step size
        if abs(angle) >= maxRot:
            return 'reached'
        elif abs(step) >= maxRot - abs(angle):
            return 'reaching'
        else:
            return 'not reaching'

    def setFinalStep(direction, step):
        '''This function checks if a moving object is about to reach one
        of the screen boundaries, and sets the final step accordingly.
        step is the step size before making the final step.'''
        if direction == 'counterclockwise' or direction == 'right':
            step -= .01
        elif direction == 'clockwise' or direction == 'left':
            step += .01
        return step

    def reachedBoundaries(direction, centerPos, quarter):
        '''This function checks if a moving object has gone or will be going
        beyond the screen boundaries.
        centerPos is the coordinates of the object's center.
        quarter is the quarter in the xy-plane (with the y-axis pointing
        downward) in which the object is currently staying.'''
        if direction == 'counterclockwise' or direction == 'right':
            if quarter == 3 and centerPos[0] <= boundaryLeft:
                return True
            elif quarter == 1 and centerPos[0] >= boundaryRight:
                return True
            elif quarter == 2 and centerPos[1] <= boundaryTop:
                return True
            elif quarter == 4 and centerPos[1] >= boundaryBottom:
                return True
            else:
                return False
        elif direction == 'clockwise' or direction == 'left':
            if quarter == 4 and centerPos[0] <= boundaryLeft:
                return True
            elif quarter == 2 and centerPos[0] >= boundaryRight:
                return True
            elif quarter == 3 and centerPos[1] <= boundaryTop:
                return True
            elif quarter == 1 and centerPos[1] >= boundaryBottom:
                return True
            else:
                return False

    def setRot(angle, step):
        '''This function sets the new rotation of an object that is moving
        around a point.
        angle is the angle (measured in degrees) formed by two lines:
        (1) the line connecting the object's center point and the point around
        which it moves, and
        (2) the positive y-axis pointing downward from the latter point.
        step is the step size before making the final step.'''
        rotate = angle + step
        # make sure the angle is between -180 and 180 degrees
        if rotate > 180:
            rotate -= 360
        elif rotate < -180:
            rotate += 360
        return rotate

    def setNewPos(rotCenter, r, angle, step):
        '''This function sets the new coordinates of the center of an object
        is moving around a point.
        rotCenter is the point around which the object moves.
        r is the distance between the object's center point and rotCenter.
        angle is the angle (measured in degrees) formed by two lines:
        (1) the line connecting the object's center point and rotCenter, and
        (2) the positive y-axis pointing downward from rotCenter.
        step is the step size before making the final step.'''
        rotate = setRot(angle, step)   # new angle (measured in degrees)
        # new coordinates of the object's center
        newX = rotCenter[0] + r * math.sin(rotate*math.pi/180)
        newY = rotCenter[1] + r * math.cos(rotate*math.pi/180)
        newCenterPos = newX, newY
        return newCenterPos, rotate

    def move(direction, centerPos, rotCenter, step=10,
             maxRot=None, screenSize=None, objCenter=None):
        '''This function rotates an object around a point.
        step is the step size (i.e., the number of degrees in each movement).
        centerPos is the coordinates of the object's center point.
        rotCenter is the point around which the object moves.
        maxRot is the maximum angle (measured in degrees) to which the
        object is allowed to move. If specified, the angle must be between 0 &
        180 degrees.
        objCenter is the object's center point, only specified if screenSize
        is specified.'''
        # relationship between the object's center point and the point around
        # which the object moves:
        # radius, angle (measured in degrees), and quarter in the xy-plane
        r, angle, quarter = line.getParams(rotCenter, centerPos)[2:]
        # check maximum rotation
        if maxRot != None:
            if checkMaxRot(angle, maxRot) == 'reached':
                # object has reached maximum rotation --> stop moving
                step = 0
            elif checkMaxRot(angle, maxRot) == 'reaching':
                # final step before reaching maximum rotation
                step = maxRot - abs(angle)
        if step != 0:
            # check direction
            if direction == 'clockwise' or direction == 'left':
                step *= -1   # negative step size
            # new coordinates of the object's center and new angle (in degrees)
            newCenterPos, rotate = setNewPos(rotCenter, r, angle, step)
            if screenSize != None:
                # set boundaries
                Movement.setBoundaries(objCenter, screenSize)
                # set final step before reaching boundary
                while reachedBoundaries(direction, newCenterPos, quarter):
                    setFinalStep(direction, step)
                    # new coordinates of the object's center and new angle
                    newCenterPos,rotate = setNewPos(rotCenter,r,angle,step)
                # stop moving if object has reached one of the screen boundaries
                if reachedBoundaries(direction, centerPos, quarter):
                    step = 0
        if step == 0:   # no change in either position or angle
            newCenterPos, rotate = centerPos, angle
        return newCenterPos, rotate

class ToPoint:
    '''This class has one method: move.
    To get a brief description of the method, use the following syntax:
        <module name as imported>.ToPoint.move.__doc__'''

    def move(centerPos, endPoint, endAngle, speedBoost=1):
        '''This function moves an object to a specified end point.
        centerPos is the coordinates of the object's center point.
        endAngle is the direction the front of the object will face after
        the object has reached the end point. The default has the object
        facing upward.
        speedBoost adjusts the step size and must not be negative.'''
        if endPoint == centerPos:   # object has reached end point
            # stop moving and rotate to end angle
            stepX = 0
            stepY = 0
            rotate = endAngle   # measured in degrees
        else:
            # distance from end point and current angle (measured in degrees)
            Xdiff, Ydiff, dist, currentAngle = line.getParams(endPoint,
                                                              centerPos)[:4]
            # step size
            stepX = Xdiff
            stepY = Ydiff
            stepDiag = dist   # total travel distance per step
            # adjust step size
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
        # new coordinates of object center
        newCenterPos = centerPos[0]+stepX, centerPos[1]+stepY
        return newCenterPos, rotate

def update(screen, things, thingsPos, moved, newCenterPos, rotate=False):
    '''This function redraws things on the screen to show movements.
    things is a list of objects on the screen.
    thingsPos is a list of the positions of the objects.
    moved is a tuple/list of objects that will be moved after the redrawing, 
    along with the original surfaces containing the moved objects at the 
    beginning of the program.
    newCenterPos is a tuple/list of the new coordinates of the moved
    objects' center points after being redrawn.
    rotate, if specified, is a tuple/list of the angles (measured in
    degrees) by which the moved objects will rotate. The default is that
    there is no change from the original rotation.'''
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
    # count number moved objects found in things
    count = [0] * numThings
    for i in range(numThings):
        for j in range(numMoved):
            if movedFound[i][i][j] != 'no match':
                count[i] += 1
    # redraw objects
    thingsRedrawn = [0] * numThings
    objMovedRedrawn = [0] * numMoved
    for i in range(numThings):
        if count[i] == 0:
            # unmoved object
            screen.blit(things[i], thingsPos[i])
            thingsRedrawn[i] += 1
        else:
            # moved object
            for j in range(numMoved):
                if thingsRedrawn[i] == 0 and objMovedRedrawn[j] == 0:
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
                        # redraw object
                        screen.blit(things[i], thingsPos[i]) 
                        thingsRedrawn[i] += 1
                        objMovedRedrawn[j] += 1
                        break
