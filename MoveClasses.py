'''The following classes are defined: Movement, Straight, Circle, and ToPoint.
To get a brief description of each class, use the following syntax:
    <module name as imported>.<class name>.__doc__'''

import pygame, math
import LineParams as line

class Movement:
    '''This class is the parent class of Straight, Circle, and ToPoint.
    It has the following methods: __init__, setBoundaries, and update.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Movement.<method name>.__doc__'''
    def __init__(self):
        '''This function initializes the class and sets its core attributes.'''
        self.boundaryLeft = None   # contains nothing
        self.boundaryRight = None
        self.boundaryTop = None
        self.boundaryBottom = None
        self.step = 10   # number of pixels/degrees in each movement

    def setBoundaries(self, objCenter, screenSize):
        '''This function sets the boundaries of the area in which an object is
        allowed to move.
        objCenter is the object's center point.
        screenSize is a tuple containing the width and height of the screen.'''
        self.boundaryLeft = objCenter[0]
        self.boundaryRight = screenSize[0] - objCenter[0]
        self.boundaryTop = objCenter[1]
        self.boundaryBottom = screenSize[1] - objCenter[1]
        
    def update(self, screen, things, thingsPos, moved, newCenterPos,
               rotate=False):
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

class Straight(Movement):
    '''This class is a child class of Movement and has the following methods:
    __init__, setStep, setFinalStep, reachedBoundaries, and move.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Straight.<method name>.__doc__'''
    def __init__(self):
        '''This function initializes the class and sets its core attributes.'''
        Movement.__init__(self)   # initializes the parent class
        # step size
        self.stepX = self.step
        self.stepY = self.step
    
    def setStep(self, stepX=self.stepX, stepY=self.stepY):
        '''This function sets the number of pixels in each movement.'''
        self.stepX = stepX
        self.stepY = stepY

    def setFinalStep(self, direction, centerPos):
        '''This function checks if a moving object is about to reach one of the
        screen boundaries, and sets the final step accordingly.
        centerPos is the coordinates of the object's center.'''
        if direction == 'left' and self.step <= self.boundaryLeft-centerPos[0]:
            self.setStep(stepX=self.boundaryLeft-centerPos[0], stepY=0)
        if direction == 'right' and self.step >= self.boundaryRight-centerPos[0]:
            self.setStep(stepX=self.boundaryRight-centerPos[0], stepY=0)
        if direction == 'up' and self.step <= self.boundaryTop-centerPos[1]:
            self.setStep(stepX=0, stepY=self.boundaryTop-centerPos[1])
        if direction == 'down' and self.step >= self.boundaryBottom-centerPos[1]:
            self.setStep(stepX=0, stepY=self.boundaryBottom-centerPos[1])

    def reachedBoundaries(self, direction, centerPos):
        '''This function checks if a moving object has gone or will be going
        beyond the screen boundaries.
        centerPos is the coordinates of the object's center.'''
        if direction == 'left':
            if centerPos[0] <= self.boundaryLeft:
                return True
            else:
                return False
        elif direction == 'right':
            if centerPos[0] >= self.boundaryRight:
                return True
            else:
                return False
        elif direction == 'up':
            if centerPos[1] <= self.boundaryTop:
                return True
            else:
                return False
        elif direction == 'down':
            if centerPos[1] >= self.boundaryBottom:
                return True
            else:
                return False

    def move(self, direction, centerPos, objCenter, screenSize=None):
        '''This function moves an object on a straight line.
        objCenter is the object's center point and centerPos is the coordinates
        of that point.'''
        if direction == 'left':
            # negative lateral step size; no vertical movement
            self.setStep(stepX=-self.stepX, stepY=0)
            rotate = 90
        elif direction == 'right':
            # no vertical movement
            self.setStep(stepY=0)
            rotate = -90
        elif direction == 'up':
            # no lateral movement; negative vertical step size
            self.setStep(stepX=0, stepY=-self.stepY)
            rotate = 0
        elif direction == 'down':
            # no lateral movement
            self.setStep(stepX=0)
            rotate = 180
        if screenSize != None:
            # set boundaries
            Movement.setBoundaries(self, objCenter, screenSize)
            # set final step before reaching boundary
            self.setFinalStep(direction, centerPos)
            # stop moving if object has reached one of the screen boundaries
            if self.reachedBoundaries(direction, centerPos):
                self.setStep(0, 0)
        # new coordinates of the object's center
        newCenterPos = centerPos[0]+self.stepX, centerPos[1]+self.stepY
        return newCenterPos, rotate

class Circle(Movement):
    '''This class is a child class of Movement and has the following methods:
    __init__, checkMaxRot, setFinalStep, reachedBoundaries,
    setRot, setNewPos, and move.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Circle.<method name>.__doc__'''
    def __init__(self):
        '''This function initializes the class and sets its core attributes.'''
        Movement.__init__(self)   # initializes the parent class
    
    def checkMaxRot(self, angle, maxRot):
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
        elif abs(self.step) >= maxRot - abs(angle):
            return 'reaching'
        else:
            return 'not reaching'

    def setFinalStep(self, direction):
        '''This function checks if a moving object is about to reach one
        of the screen boundaries, and sets the final step accordingly.'''
        if direction == 'counterclockwise' or direction == 'right':
            self.step -= .01
        elif direction == 'clockwise' or direction == 'left':
            self.step += .01

    def reachedBoundaries(self, direction, centerPos, quarter):
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

    def setRot(self, angle):
        '''This function sets the new rotation of an object that is moving
        around a point.
        angle is the angle (measured in degrees) formed by two lines:
        (1) the line connecting the object's center point and the point around
        which it moves, and
        (2) the positive y-axis pointing downward from the latter point.'''
        rotate = angle + self.step
        # make sure the angle is between -180 and 180 degrees
        if rotate > 180:
            rotate -= 360
        elif rotate < -180:
            rotate += 360
        return rotate

    def setNewPos(self, rotCenter, r, angle):
        '''This function sets the new coordinates of the center of an object
        is moving around a point.
        rotCenter is the point around which the object moves.
        r is the distance between the object's center point and rotCenter.
        angle is the angle (measured in degrees) formed by two lines:
        (1) the line connecting the object's center point and rotCenter, and
        (2) the positive y-axis pointing downward from rotCenter.'''
        rotate = self.setRot(angle)   # new angle (measured in degrees)
        # new coordinates of the object's center
        newX = rotCenter[0] + r * math.sin(rotate*math.pi/180)
        newY = rotCenter[1] + r * math.cos(rotate*math.pi/180)
        newCenterPos = newX, newY
        return newCenterPos, rotate

    def move(self, direction, centerPos, objCenter, rotCenter, maxRot=None,
             screenSize=None):
        '''This function rotates an object around a point.
        objCenter is the object's center point and centerPos is the coordinates
        of that point.
        rotCenter is the point around which the object moves.
        maxRot is the maximum angle (measured in degrees) to which the object is
        allowed to move. If specified, the angle must be between 0 & 180 degrees.'''
        # relationship between the object's center point and the point around
        # which the object moves:
        # radius, angle (measured in degrees), and quarter in the xy-plane
        r, angle, quarter = line.getParams(rotCenter, centerPos)[2:]
        # check maximum rotation
        if maxRot != None:
            if self.checkMaxRot(angle, maxRot) == 'reached':
                # object has reached maximum rotation --> stop moving
                self.step = 0
            elif self.checkMaxRot(angle, maxRot) == 'reaching':
                # final step before reaching maximum rotation
                self.step = maxRot - abs(angle)
        if self.step != 0:
            # check direction
            if direction == 'clockwise' or direction == 'left':
                self.step *= -1   # negative step size
            # new coordinates of the object's center and new angle (in degrees)
            newCenterPos, rotate = self.setNewPos(rotCenter, r, angle)
            if screenSize != None:
                # set boundaries
                Movement.setBoundaries(self, objCenter, screenSize)
                # set final step before reaching boundary
                while self.reachedBoundaries(direction, newCenterPos, quarter):
                    self.setFinalStep(direction)
                    # new coordinates of the object's center and new angle
                    newCenterPos, rotate = self.setNewPos(rotCenter, r, angle)
                # stop moving if object has reached one of the screen boundaries
                if self.reachedBoundaries(direction, centerPos, quarter):
                    self.step = 0
        if self.step == 0:   # no change in either position or angle
            newCenterPos, rotate = centerPos, angle
        return newCenterPos, rotate

class ToPoint:
    '''This class has the following methods: __init__ and move
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Circle.<method name>.__doc__'''
    def __init__(self):
        pass
    
    def move(self, centerPos, endPoint, endAngle=0, speedBoost=1):
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
