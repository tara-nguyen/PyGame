<<<<<<< HEAD
'''This module defines the Player class. To get a brief description of the class,
use the following syntax: <module name as imported>.Player.__doc__'''

=======
>>>>>>> add-goalkeeper
import pygame, random, math
import LineParams as line
import MoveFunctions as move
import NonplayerClasses as np

class Player(np.Game):
    '''This class is a child class of Game, which is defined in the module
    NonplayerClass.py. It's also the parent class of Goalkeeper and Outfielder.
    This class has the following methods: __init__, load, getFootSize, 
    getBodySize, setStartPos, adjustStartPos, blitFeet, blitBody, getStartPos, 
    getCenter, setCenterPos, getCenterPos, getMidpoint, getRotation, 
    setMovingRotation, getMovingRotation, getBodyAngle, getFootAngle, 
    feetToFront, setStep, getDistanceMoved, getDistanceToBall, getSinCos, 
    getEnding, moveAroundBall, moveStraight, moveToBall, move, updatePlayer,
    and updateFoot.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Player.<method name>.__doc__'''
    def __init__(self, screenSize):
        '''This function initializes the class and sets its core attributes.'''
        np.Game.__init__(self, screenSize)   # initialize the parent class
        self.lFoot = None   # contains nothing
        self.rFoot = None
        self.body = None
        
    def load(self, imageName1, imageName2):
        '''This function loads images of the player's feet and body into PyGame
        and rotates them 90 degrees counterclockwise.'''
        footWidth, footHeight = 44, 30
        bodyWidth, bodyHeight = 52, 76
        self.lFoot = np.Game.loadImage(self, imageName1, footWidth, footHeight)
        self.rFoot = self.lFoot
        self.body = np.Game.loadImage(self, imageName2, bodyWidth, bodyHeight)
        # rotate
        self.lFoot = pygame.transform.rotate(self.lFoot, 90)
        self.rFoot = pygame.transform.rotate(self.rFoot, 90)
        self.body = pygame.transform.rotate(self.body, 90)
        # duplicates to hold the images at the start of the program (i.e.,
        # before any change/movement has been made)
        self.footStart = self.lFoot
        self.bodyStart = self.body
<<<<<<< HEAD

=======
        
>>>>>>> add-goalkeeper
    def getFootSize(self):
        '''This function returns the size of the feet.'''
        self.footWidth = self.lFoot.get_rect().width
        self.footHeight = self.lFoot.get_rect().height
        return self.footWidth, self.footHeight
    
    def getBodySize(self):
        '''This function returns the size of the body.'''
        self.bodyWidth = self.body.get_rect().width
        self.bodyHeight = self.body.get_rect().height
        return self.bodyWidth, self.bodyHeight

    def setStartPos(self):
        '''This function sets the positions where the feet and the body will be
        drawn, assuming that the player will be facing upward at the start of
        the program.'''
        self.footCenter, self.bodyCenter = self.getCenter()   # center points
        # holder variables for the centers at the start of the program
        self.footCenterStart = self.footCenter
        self.bodyCenterStart = self.bodyCenter
        # coordinates of the body center at the start of the program
        self.bodyCenterPos = (self.bodyStartPos[0]+self.bodyCenterStart[0],
                              self.bodyStartPos[1]+self.bodyCenterStart[1])
        # how many pixels of the feet stick out from the front of the body
        self.feetOut = 1   
        # position of the feet
        self.lFootStartPos = (self.bodyCenterPos[0]-self.getFootSize()[0]-1,
                              self.bodyStartPos[1]-self.feetOut)
        self.rFootStartPos = self.bodyCenterPos[0]+1, self.lFootStartPos[1]
        # coordinates of the foot centers at the start of the program
        self.lFootCenterPos = (self.lFootStartPos[0]+self.footCenterStart[0],
                               self.lFootStartPos[1]+self.footCenterStart[1])
        self.rFootCenterPos = (self.rFootStartPos[0]+self.footCenterStart[0],
                               self.rFootStartPos[1]+self.footCenterStart[1])

    def adjustStartPos(self, rotate):
        '''This function adjusts the positions where the feet will be drawn at
        the start of the program, by first adjusting both the coordinates of the
        body center and those of the centers of the feet.
        rotate is the direction the player will be facing, i.e., the angle
        (measured in degrees) by which the player will rotate from the original
        upward rotation.'''
        newBodyCenterPos = (self.bodyStartPos[0]+self.getCenter()[1][0],
                            self.bodyStartPos[1]+self.getCenter()[1][1])
        # distance from the old coordinates
        moveX, moveY = self.getDistanceMoved(newBodyCenterPos)
        # new coordinates of the body center
        self.setCenterPos('body', newBodyCenterPos[0], newBodyCenterPos[1])
        # new coordinates of the centers of the feet
        self.setCenterPos('lFoot', self.getCenterPos()[0][0]+moveX,
                          self.getCenterPos()[0][1]+moveY)
        self.setCenterPos('rFoot', self.getCenterPos()[1][0]+moveX,
                          self.getCenterPos()[1][1]+moveY)
        self.setMovingRotation(rotate)   # rotation (angled measured in degrees)
        self.feetToFront(self.getCenterPos()[2])   # move feet to front of body
        # new positions at which the feet will be drawn
        self.lFootStartPos = (self.getCenterPos()[0][0]-self.getCenter()[0][0],
                              self.getCenterPos()[0][1]-self.getCenter()[0][1])
        self.rFootStartPos = (self.getCenterPos()[1][0]-self.getCenter()[0][0],
                              self.getCenterPos()[1][1]-self.getCenter()[0][1])

    def blitFeet(self, rotate=0):
        '''This function rotates both the feet and the body and then draws only
        the feet onto the screen.
        rotate is the angle (measured in degrees) by which the feet will be
        rotated from the original upward rotation.'''
        self.setStartPos()   # where the feet and the body will be drawn
        # rotate both the feet and the body
        self.lFoot = pygame.transform.rotate(self.lFoot, rotate)
        self.rFoot = pygame.transform.rotate(self.rFoot, rotate)
        self.body = pygame.transform.rotate(self.body, rotate)
        self.adjustStartPos(rotate)   # adjust drawing positions
        # draw the feet
        self.screen.blit(self.lFoot, self.lFootStartPos)
        self.screen.blit(self.rFoot, self.rFootStartPos)
<<<<<<< HEAD

=======
        self.things = [self.lFoot, self.rFoot] 
        
>>>>>>> add-goalkeeper
    def blitBody(self, rotate=0):
        '''This function draws the body onto the screen.
        rotate is the angle (measured in degrees) by which the image will be
        rotated from the original upward rotation.'''
        self.screen.blit(self.body, self.bodyStartPos)
<<<<<<< HEAD
=======
        self.things += [self.body]
>>>>>>> add-goalkeeper
        
    def getStartPos(self):
        '''This function returns the positions of the feet and the body at the
        start of the program.'''
        return [self.lFootStartPos, self.rFootStartPos, self.bodyStartPos]

    def getCenter(self):
        '''This function returns the centers of the feet and the body.'''
        self.footCenter = self.lFoot.get_rect().center
        self.bodyCenter = self.body.get_rect().center
        return self.footCenter, self.bodyCenter

    def setCenterPos(self, bodyPart, X, Y):
        '''This function sets a new position for the center of one of the feet
        or the center of the body.'''
        if bodyPart == 'lFoot':
            self.lFootCenterPos = X, Y
        elif bodyPart == 'rFoot':
            self.rFootCenterPos = X, Y
        else:
            self.bodyCenterPos = X, Y
        
    def getCenterPos(self):
        '''This function returns the coordinates of the centers of the body
        and of the feet.'''
        return [self.lFootCenterPos, self.rFootCenterPos, self.bodyCenterPos]

    def getMidpoint(self):
        '''This function returns the coordinates of the midpoint of the line 
        connecting the two feet at their centers.'''
        self.midPoint = ((self.getCenterPos()[0][0]+self.getCenterPos()[1][0])/2,
                         (self.getCenterPos()[0][1]+self.getCenterPos()[1][1])/2)
        return self.midPoint

    def getRotation(self):
        '''This function returns the current rotation of the player, i.e., the
        direction the player is currently facing. It is an angle, measured in
        degrees, formed by two lines: (1) the line connecting the body center
        and the midpoint (the point at the middle of the line connecting the 
        two feet at their centers), and (2) the y-axis pointing down from
        the midpoint.'''
        self.currentRot = line.getParams(self.getMidpoint(),
                                         self.getCenterPos()[2])[3]
        return self.currentRot

    def setMovingRotation(self, rotate):
        '''This function sets the angle (measured in degrees) by which the 
        rotation of the player has changed, after a movement, from that at the
        start of the program.'''
        self.rotate = rotate
        
    def getMovingRotation(self):
        '''This function returns the angle (measured in degrees) by which the 
        rotation of the player has changed, after a movement, from that at the
        start of the program.'''
        return self.rotate

    def getBodyAngle(self, target):
        '''This function returns the angle (measured in degrees) of the body
        with respect to the y-axis pointing down from a point.
        target is either the coordinates of the target point or the coordinates
        of the center of an object (e.g., the ball).'''
        bodyAngle = line.getParams(target, self.getCenterPos()[2])[3]
        return bodyAngle

    def getFootAngle(self, target):
        '''This function returns the angles (measured in degrees) of the feet
        with respect to the y-axis pointing down from a point.
        target is either the coordinates of the target point or the coordinates
        of the center of an object (e.g., the ball).'''
        lFootAngle = line.getParams(target, self.getCenterPos()[0])[3]
        rFootAngle = line.getParams(target, self.getCenterPos()[1])[3]
        return lFootAngle, rFootAngle
    
    def feetToFront(self, target):
        '''This function moves the feet to the front of the body.
        target is either the coordinates of the point around which the player 
        rotates or the coordinates of the point to which the player moves.'''
        # direction the player is currently facing (angle measured in degrees)
        currentRot = self.getRotation()
        if target != self.getCenterPos()[2]:
            # player not at the target point
            if self.getBodyAngle(target) != currentRot:
                self.lFootCenterPos = move.moveCircle(
                    self.getCenterPos()[2], self.getCenterPos()[0], 'right',
                    step=self.getBodyAngle(target)-currentRot)[0]
                self.rFootCenterPos = move.moveCircle(
                    self.getCenterPos()[2], self.getCenterPos()[1], 'right',
                    step=self.getBodyAngle(target)-currentRot)[0]
        else:
            # player is already at the target point
            self.lFootCenterPos = move.moveCircle(
                self.getCenterPos()[2], self.getCenterPos()[0], 'right',
                step=self.getMovingRotation()-currentRot)[0]
            self.rFootCenterPos = move.moveCircle(
                self.getCenterPos()[2], self.getCenterPos()[1], 'right',
                step=self.getMovingRotation()-currentRot)[0]
            
    def setStep(self, stepX, stepY):
        '''This function sets the step size for the body's movements.'''
        self.stepX = stepX
        self.stepY = stepY

    def getDistanceMoved(self, newCenterPos):
        '''This function returns the change in the position of the body
        after a movement.
        newCenterPos is the new coordinates of the center of the body.'''
        moveX, moveY = line.getParams(newCenterPos, self.getCenterPos()[2])[:2]
        return moveX, moveY

    def getDistanceToBall(self, ballCenterPos):
        '''This function returns the distance between each foot and the ball.'''
        lFootToBall = line.getParams(ballCenterPos, self.getCenterPos()[0])[2]
        rFootToBall = line.getParams(ballCenterPos, self.getCenterPos()[1])[2]
        return lFootToBall, rFootToBall
        
    def getSinCos(self, angle):
        '''This function returns the sine and cosine of an angle.'''
        sine = math.sin(angle * math.pi/180)
        cosine = math.cos(angle * math.pi/180)
        return sine, cosine
        
    def getEnding(self, ballCenterPos, finalDist, angle):
        '''This function returns the point to which the body/foot will move when
        it's headed for the ball, along with the direction the body/foot will 
        face  when it reaches the endpoint (angle measured in degrees).
        ballCenterPos is the coordinates of the ball center.
        finalDist is the distance from the body to the ball when the body is at
        the target end point.
        angle is the current angle (measured in degrees) of the body/foot with
        respect to the y-axis pointing down from the ball.'''
        # point to which the body will move
        endPointX = ballCenterPos[0] + finalDist * self.getSinCos(angle)[0]
        endPointY = ballCenterPos[1] + finalDist * self.getSinCos(angle)[1]
        endPoint = endPointX, endPointY
        # final rotation, i.e., direction the body will face when it reaches
        # the endpoint (angle measured in degrees)
        endAngle = line.getParams(ballCenterPos, endPoint)[3]
        return endPoint, endAngle

    def moveAroundBall(self, ballCenterPos, direction):
        '''This function rotates both the feet and the body around the ball.
        ballCenterPos is the coordinates of the ball center.
        direction denotes which way the body/foot will move.'''
        self.setStep(10, 10)   # set step size
        # current angle (measured in degrees) of the body with respect to the 
        # y-axis pointing down from the ball
        bodyAngle = self.getBodyAngle(ballCenterPos)
        # rotate body
        newCenterPos, rotate = move.moveCircle(
            ballCenterPos, self.getCenterPos()[2], direction, step=self.stepX,
            boundaryX=[0,self.screenWidth], boundaryY=[0,self.screenHeight],
            objCenter=self.getCenter()[1])
        if newCenterPos != self.getCenterPos()[2]:   # body moving
            self.moved = True
            # new coordinates of the body center
            self.setCenterPos('body', newCenterPos[0], newCenterPos[1])
            # rotation (angled measured in degrees)
            self.setMovingRotation(rotate)
            # step size for rotation of the feet (between 0 and 180 degrees)
            if rotate - bodyAngle > 180:
                step = abs(rotate - bodyAngle - 360)
            elif rotate - bodyAngle < -180:
                step = abs(rotate - bodyAngle + 360)
            else:
                step = abs(rotate - bodyAngle)
            # rotate feet
            self.lFootCenterPos = move.moveCircle(
                ballCenterPos, self.getCenterPos()[0], direction, step=step)[0]
            self.rFootCenterPos = move.moveCircle(
                ballCenterPos, self.getCenterPos()[1], direction, step=step)[0]
            self.feetToFront(ballCenterPos)   # move feet to front of body

    def moveStraight(self, direction):
        '''This function moves both the feet and the body in a straight line.
        direction denotes which way the body/foot will move.'''
        self.setStep(10, 10)   # set step size
        # move body
        newCenterPos, rotate = move.moveStraight(
            self.getCenter()[1], self.getCenterPos()[2], direction,
            stepX=self.stepX, stepY=self.stepY,
            boundaryX=[self.feetOut,self.screenWidth-self.feetOut],
            boundaryY=[self.feetOut,self.screenHeight-self.feetOut])
        if newCenterPos != self.getCenterPos()[2]:   # body moving
            self.moved = True
            # distance moved
            moveX, moveY = self.getDistanceMoved(newCenterPos)
            # new coordinates of the body center
            self.setCenterPos('body', newCenterPos[0], newCenterPos[1])
            # rotation (angled measured in degrees)
            self.setMovingRotation(rotate)   
            # move feet at the same distance as body
            self.setCenterPos('lFoot', self.getCenterPos()[0][0]+moveX,
                              self.getCenterPos()[0][1]+moveY)
            self.setCenterPos('rFoot', self.getCenterPos()[1][0]+moveX,
                              self.getCenterPos()[1][1]+moveY)
            if self.getRotation() != self.getMovingRotation():
                # player facing the wrong direction
                self.feetToFront(newCenterPos)   # move feet to front of body

    def moveToBall(self, ballCenterPos, ballCenter):
        '''This function moves both the feet and the body toward the ball.
        ballCenterPos is the coordinates of the ball center.'''
        # point to which the body will move and the direction the body will
        # face when it reaches the endpoint (angle measured in degrees)
        endPoint, endAngle = self.getEnding(
            ballCenterPos, self.bodyCenterStart[1]+self.feetOut+ballCenter[1],
            self.getBodyAngle(ballCenterPos))
        # move body
        newCenterPos, rotate = move.moveToPoint(
            endPoint, self.getCenterPos()[2], endAngle=endAngle, speedBoost=3)
        if newCenterPos != self.getCenterPos()[0]:   # body moving
            self.moved = True
            # distance moved
            moveX, moveY = self.getDistanceMoved(newCenterPos)
            # new coordinates of the body center
            self.setCenterPos('body', newCenterPos[0], newCenterPos[1])
            # rotation (angled measured in degrees)
            self.setMovingRotation(rotate)   
            # move feet at the same distance as body
            self.setCenterPos('lFoot', self.getCenterPos()[0][0]+moveX,
                              self.getCenterPos()[0][1]+moveY)
            self.setCenterPos('rFoot', self.getCenterPos()[1][0]+moveX,
                              self.getCenterPos()[1][1]+moveY)
            self.feetToFront(endPoint)   # move feet to front of body

    def move(self, moveType, direction, ballCenter, ballCenterPos):
        '''This function moves the player according to the specified type
        of movement.
        ballCenter is the ball center and ballCenterPos is its coordinates.'''
        if moveType == 'circle':
            self.moveAroundBall(ballCenterPos, direction)
        elif moveType == 'straight':
            self.moveStraight(direction)
        else:
            self.moveToBall(ballCenterPos, ballCenter)
        
<<<<<<< HEAD
    def updatePlayer(self, allThings, allPos, lFootIndex, bodyIndex):
        '''This function updates the positions and rotations of both the body
        and the feet.
        allThings is a list of everything on the screen.
        allPos is a list of the positions of everything on the screen.
        lFootIndex, rFootIndex, bodyIndex are the indexes of the left foot and
        of the body, respectively, in allThings and in allPos.'''
=======
    def updatePlayer(self, lFootIndex, bodyIndex):
        '''This function updates the positions and rotations of both the body
        and the feet.
        lFootIndex and bodyIndex are the indexes of the left foot and of the
        body, respectively, in allThings and in allPos.'''
>>>>>>> add-goalkeeper
        moved = (self.lFoot, self.rFoot, self.body,
                 self.footStart, self.footStart, self.bodyStart)
        # new coordinates of the centers of the feet and the body
        newCenterPos = self.getCenterPos()
<<<<<<< HEAD
        move.update(self.screen, allThings, allPos, moved, newCenterPos,
                    rotate=(self.getMovingRotation(),)*3)
        self.lFoot, self.rFoot = allThings[lFootIndex:lFootIndex+2]
        self.body = allThings[bodyIndex]
        # new center points
        self.footCenter, self.bodyCenter = self.getCenter()

    def updateFoot(self, foot, newCenterPos, rotate,
                   allThings, allPos, lFootIndex):
=======
        move.update(self.screen, self.allThings, self.allPos, moved,
                    newCenterPos, rotate=(self.getMovingRotation(),)*3)
        self.lFoot, self.rFoot = self.allThings[lFootIndex:lFootIndex+2]
        self.body = self.allThings[bodyIndex]
        # new center points
        self.footCenter, self.bodyCenter = self.getCenter()

    def updateFoot(self, foot, newCenterPos, rotate, lFootIndex):
>>>>>>> add-goalkeeper
        '''This function updates the positions and rotations of only the feet.
        newCenterPos is a tuple/list of the new coordinates of the center of 
        each foot.
        rotate is a tuple/list of the angles (measured in degrees) by which 
        the rotations of the feet have changed from those at the start of
        the program.
<<<<<<< HEAD
        allThings is a list of everything on the screen.
        allPos is a list of the positions of everything on the screen.
        lFootIndex is the indexes of the left foot in allThings and in allPos.'''
        moved = self.lFoot, self.rFoot, self.footStart, self.footStart
        move.update(self.screen, allThings, allPos, moved, newCenterPos, rotate)
        self.lFoot, self.rFoot = allThings[lFootIndex:lFootIndex+2]
        self.footCenter = self.getCenter()[0]   # new center point
        
class Goalkeeper(Player):
    '''This class is a child of the Player class. This class has the following
    methods: __init__, ...
=======
        lFootIndex is the index of the left foot in allThings and in allPos.'''
        moved = self.lFoot, self.rFoot, self.footStart, self.footStart
        move.update(self.screen, self.allThings, self.allPos, moved,
                    newCenterPos, rotate)
        self.lFoot, self.rFoot = self.allThings[lFootIndex:lFootIndex+2]
        self.footCenter = self.getCenter()[0]   # new center point
        
class Goalkeeper(Player):
    '''This class is a child class of Player and has the following methods:
    __init__, ...
>>>>>>> add-goalkeeper
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Goalkeeper.<method name>.__doc__'''
    def __init__(self, screenSize):
        '''This function initializes the class and sets its core attributes.'''
        Player.__init__(self, screenSize)   # initialize the parent class
        # body position at the start of the program
        self.bodyStartPosX = (self.screenWidth - 76) / 2
        self.bodyStartPosY = 80
        self.bodyStartPos = self.bodyStartPosX, self.bodyStartPosY
        
class Outfielder(Player):
<<<<<<< HEAD
    '''This class is a child of the Player class. This class has the following
    methods: __init__, chooseKickingFoot, and kickBall.
=======
    '''This class is a child class of Player and has the following methods:
    __init__, chooseKickingFoot, and kickBall.
>>>>>>> add-goalkeeper
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Outfielder.<method name>.__doc__'''
    def __init__(self, screenSize):
        '''This function initializes the class and sets its core attributes.'''
        Player.__init__(self, screenSize)   # initialize the parent class
        # body position at the start of the program
        self.bodyStartPosX = random.uniform(20, self.screenWidth-96)
        self.bodyStartPosY = random.uniform(self.screenHeight-150,
                                            self.screenHeight-100)
        self.bodyStartPos = self.bodyStartPosX, self.bodyStartPosY
        
    def chooseKickingFoot(self, ballCenterPos):
        '''This function chooses the foot that will kick the ball, gets the
        angle (measured in degrees) of the foot with respect to the y-axis
        pointing down from the ball, and returns a string indicating which foot.
        ballCenterPos is the coordinates of the ball center.'''
        # distance between the ball and each of the player's feet
        lFootToBall, rFootToBall = self.getDistanceToBall(ballCenterPos)
        # the foot closer to the ball will be the one that kicks the ball
        # get the coordinates of the foot center and the angle (measured in 
        # degrees) with respect to the y-axis pointing down from the ball
        if lFootToBall < rFootToBall:
            self.kFootCenterPos = self.getCenterPos()[0]
            self.kFootAngle = self.getFootAngle(ballCenterPos)[0]
            return 'lFoot'   # left foot is the kicking foot
        elif lFootToBall > rFootToBall:
            self.kFootCenterPos = self.getCenterPos()[1]
            self.kFootAngle = self.getFootAngle(ballCenterPos)[1]
            return 'rFoot'   # right foot is the kicking foot
        else:
            # ball is equidistant from both feet --> make a random pick
            feet = [self.getCenterPos()[0], self.getCenterPos()[1]]
            self.kFootCenterPos = random.choice(feet)
            if self.kFootCenterPos == feet[0]:
                self.kFootAngle = self.getFootAngle(ballCenterPos)[0]
                return 'lFoot'   # left foot is the kicking foot
            else:
                self.kFootAngle = self.getFootAngle(ballCenterPos)[1]
                return 'rFoot'   # right foot is the kicking foot
        
<<<<<<< HEAD
    def kickBall(self, ballCenterPos, ballCenter, allThings, allPos, lFootIndex):
        '''This function moves a foot to make the player kick the ball.
        ballCenter is the ball center and ballCenterPos is its coordinates.
        allThings is a list of everything on the screen.
        allPos is a list of the positions of everything on the screen.
=======
    def kickBall(self, ballCenterPos, ballCenter, lFootIndex):
        '''This function moves a foot to make the player kick the ball.
        ballCenter is the ball center and ballCenterPos is its coordinates.
>>>>>>> add-goalkeeper
        lFootIndex is the indexes of the left foot in allThings and in allPos.'''
        # direction the player is currently facing (angle measured in degrees)
        currentRot = self.getRotation()
        # distance between the ball and each of the player's feet
        lFootToBall, rFootToBall = self.getDistanceToBall(ballCenterPos)
        # choose the foot that will kick the ball
        kickingFoot = self.chooseKickingFoot(ballCenterPos)
        # point to which the kicking foot will move
        endPoint = self.getEnding(
            ballCenterPos, self.footCenterStart[1]+ballCenter[1],
            self.kFootAngle)[0]
        # If the foot is already very close to the ball then the foot won't
        # need to move, so the foot's center is the endpoint.
        if kickingFoot == 'lFoot':   # left foot is the kicking foot
            if lFootToBall <= self.footCenterStart[1] + ballCenter[1]:
                endPoint = self.kFootCenterPos
        else:   # right foot is the kicking foot
            if rFootToBall <= self.footCenterStart[1] + ballCenter[1]:
                endPoint = self.kFootCenterPos
        # move foot
        newCenterPos, rotate = move.moveToPoint(endPoint, self.kFootCenterPos,
                                                endAngle=currentRot)
        if newCenterPos == endPoint:
            # foot has touched the ball
            self.touchedBall = True
        else:
            self.touchedBall = False
        if kickingFoot == 'lFoot':   # left foot is the kicking foot
            newCenterPos = newCenterPos, self.getCenterPos()[1]
            rotate = rotate, currentRot
        else:   # right foot is the kicking foot
            newCenterPos = self.getCenterPos()[0], newCenterPos
            rotate = currentRot, rotate
        # update display to show movement
<<<<<<< HEAD
        self.updateFoot(kickingFoot, newCenterPos, rotate,
                        allThings, allPos, lFootIndex)
=======
        self.updateFoot(kickingFoot, newCenterPos, rotate, lFootIndex)
>>>>>>> add-goalkeeper
        self.updateDisplay()
        pygame.time.wait(100)   # pause program for 100 ms
        # bring foot back to the position and rotation before the kick
        if kickingFoot == 'lFoot':   # left foot is the kicking foot
            newCenterPos = self.kFootCenterPos, self.getCenterPos()[1]
        else:   # right foot is the kicking foot
            newCenterPos = self.getCenterPos()[0], self.kFootCenterPos
<<<<<<< HEAD
        self.updateFoot(kickingFoot, newCenterPos, (currentRot,)*2,
                        allThings, allPos, lFootIndex)
=======
        self.updateFoot(kickingFoot, newCenterPos, (currentRot,)*2, lFootIndex)
>>>>>>> add-goalkeeper
        self.updateDisplay()
