'''This module defines the Player class. To get a brief description of the class,
use the following syntax: <module name as imported>.Player.__doc__'''

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
    getBodyAngle, getFootAngle, setMovingRotation, getMovingRotation,
    feetToFront, setStep, getDistanceMoved, getDistanceToBall, getEnding,
    moveAroundBall, moveStraight, moveToBall, updatePlayer, updateFeet,
    chooseKickingFoot, prepareBallKick, updateKickingFoot, and checkBallTouch.
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
        # temporary sizes of the feet and of the body
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
        self.things = [self.lFoot, self.rFoot] 
        
    def blitBody(self, rotate=0):
        '''This function draws the body onto the screen.
        rotate is the angle (measured in degrees) by which the image will be
        rotated from the original upward rotation.'''
        self.screen.blit(self.body, self.bodyStartPos)
        self.things += [self.body]
        
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
        '''This function returns the player's current rotation, i.e., the
        direction the player is currently facing. It is an angle, measured in
        degrees, formed by two lines: (1) the line connecting the body center
        and the midpoint (the point at the middle of the line connecting the 
        two feet at their centers), and (2) the y-axis pointing down from
        the midpoint.'''
        self.currentRot = line.getParams(self.getMidpoint(),
                                         self.getCenterPos()[2])[3]
        return self.currentRot

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
        endPointX = ballCenterPos[0] + finalDist * np.getTrig(angle)[0]
        endPointY = ballCenterPos[1] + finalDist * np.getTrig(angle)[1]
        endPoint = endPointX, endPointY
        # final rotation, i.e., direction the body will face when it reaches
        # the endpoint (angle measured in degrees)
        endAngle = line.getParams(ballCenterPos, endPoint)[3]
        return endPoint, endAngle

    def moveAroundBall(self, ballCenterPos, direction):
        '''This function rotates both the feet and the body around the ball.
        ballCenterPos is the coordinates of the ball's center.
        direction denotes which way the body/foot will move.'''
        self.setStep(10, 10)   # set step size
        # current angle (measured in degrees) of the body with respect to the 
        # y-axis pointing down from the target
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

    def moveToBall(self, ballCenter, ballCenterPos):
        '''This function moves both the feet and the body toward the ball.
        ballCenter is the ball's center and ballCenterPos is its coordinates.'''
        # point to which the body will move and direction the player will
        # face when he reaches that point
        endPoint, endAngle = self.getEnding(
            ballCenterPos,
            self.bodyCenterStart[1]+self.feetOut+ballCenter[1],
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

    def updatePlayer(self, lFootIndex, bodyIndex):
        '''This function updates the positions and rotations of both the body
        and the feet.
        lFootIndex and bodyIndex are the indexes of the left foot and of the
        body, respectively, in the list of everything on the screen.'''
        moved = (self.lFoot, self.rFoot, self.body,
                 self.footStart, self.footStart, self.bodyStart)
        # new coordinates of the centers of the feet and the body
        newCenterPos = self.getCenterPos()
        move.update(self.screen, self.allThings, self.allPos, moved,
                    newCenterPos, rotate=(self.getMovingRotation(),)*3)
        self.lFoot, self.rFoot = self.allThings[lFootIndex:lFootIndex+2]
        self.body = self.allThings[bodyIndex]
        # new center points
        self.footCenter, self.bodyCenter = self.getCenter()

    def updateFeet(self, foot, newCenterPos, rotate, lFootIndex):
        '''This function updates the positions and rotations of only the feet.
        newCenterPos is a tuple/list of the new coordinates of the center of 
        each foot.
        rotate is a tuple/list of the angles (measured in degrees) by which 
        the rotations of the feet have changed from those at the start of
        the program.
        lFootIndex is the index of the left foot in the list of everything on
        the screen.'''
        moved = self.lFoot, self.rFoot, self.footStart, self.footStart
        move.update(self.screen, self.allThings, self.allPos, moved,
                    newCenterPos, rotate)
        self.lFoot, self.rFoot = self.allThings[lFootIndex:lFootIndex+2]
        self.footCenter = self.getCenter()[0]   # new center point

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
        
    def prepareBallKick(self, kickingFoot, ballCenterPos, ballCenter):
        '''This function prepares the foot for the kicking motion and returns
        four values:
        (1) the player's current rotation (angle measured in degrees),
        (2) the point to which the kicking foot will move,
        (3) the new coordinates of the foot's center during the kicking motion, and
        (4) the foot's new rotation (angle measured in degrees).
        kickingFoot is the foot that will kick the ball.
        ballCenter is the ball center and ballCenterPos is its coordinates.'''
        # player's current rotation (angle measured in degrees)
        currentRot = self.getRotation()
        # distance between the ball and each of the player's feet
        lFootToBall, rFootToBall = self.getDistanceToBall(ballCenterPos)
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
        return currentRot, endPoint, newCenterPos, rotate

    def updateKickingFoot(self, kickingFoot, newCenterPos, rotate, currentRot,
                          lFootIndex):
        '''This function updates the position and rotation of the foot that will
        kick the ball during and after the kick.
        kickingFoot is the foot that will kick the ball.
        newCenterPos is the new coordinates of the foot's center during the
        kicking motion.
        rotate is the foot's new angle (measured in degrees) when it kicks the
        ball, with respect to the y-axis pointing down from the ball.
        currentRot is player's current rotation (angle measured in degrees).
        lFootIndex is the indexes of the left foot in the list of everything on
        the screen.'''
        if kickingFoot == 'lFoot':   # left foot is the kicking foot
            newCenterPos = newCenterPos, self.getCenterPos()[1]
            rotate = rotate, currentRot
        else:   # right foot is the kicking foot
            newCenterPos = self.getCenterPos()[0], newCenterPos
            rotate = currentRot, rotate
        # update foot position and update display to show movement
        self.updateFeet(kickingFoot, newCenterPos, rotate, lFootIndex)
        self.updateDisplay()
        pygame.time.wait(100)   # pause program for 100 ms
        # bring foot back to its position and rotation before the kick
        if kickingFoot == 'lFoot':   # left foot is the kicking foot
            newCenterPos = self.kFootCenterPos, self.getCenterPos()[1]
        else:   # right foot is the kicking foot
            newCenterPos = self.getCenterPos()[0], self.kFootCenterPos
        # update foot position to show movement
        self.updateFeet(kickingFoot, newCenterPos, (currentRot,)*2, lFootIndex)

    def checkBallTouch(self, newCenterPos, endPoint):
        '''This function checks if the foot has touched the ball.
        newCenterPos is the new coordinates of the foot's center when it kicks
        the ball.
        endPoint is the point to which the foot will move.'''
        if newCenterPos == endPoint:   # foot has touched ball
            self.touchedBall = True
        else:
            self.touchedBall = False

class Goalkeeper(Player):
    '''This class is a child class of Player and has two methods: __init__,
    move, and kickBall.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Goalkeeper.<method name>.__doc__'''
    def __init__(self, screenSize):
        '''This function initializes the class and sets its core attributes.'''
        Player.__init__(self, screenSize)   # initialize the parent class
        # body position at the start of the program
        self.bodyStartPosX = (self.screenWidth - 76) / 2
        self.bodyStartPosY = 80
        self.bodyStartPos = self.bodyStartPosX, self.bodyStartPosY
        self.movingDirection = random.choice([1, -1])   # left or right
        self.speed = 5   # number of pixels the goalkeeper moves per movement

    def move(self, goalPosts):
        '''This function makes the goalkeeper move between the goal posts, only
        stopping when he catches the ball (i.e., when the ball hits the front of
        his body).
        goalPosts denotes the x-coordinates and size of the goal posts.'''
        # player's current rotation (angle measured in degrees)
        currentRot = self.getRotation()
        # points to which the player will move
        lEndPoint = goalPosts[0]+goalPosts[2]+self.getCenter()[1][0]
        rEndPoint = goalPosts[1]-goalPosts[2]-self.getCenter()[1][0]
        if self.movingDirection == 1:   # playing is moving to the right
            if self.getCenterPos()[2][0] >= rEndPoint:   # reached right post
                self.movingDirection = -1   # change direction
        else:   # player is moving left
            if self.getCenterPos()[2][0] <= lEndPoint:   # reached left post
                self.movingDirection = 1   # change direction
        # move player
        self.setCenterPos(
            'body', self.getCenterPos()[2][0]+self.speed*self.movingDirection,
            self.getCenterPos()[2][1])
        self.setCenterPos(
            'lFoot', self.getCenterPos()[0][0]+self.speed*self.movingDirection,
            self.getCenterPos()[0][1])
        self.setCenterPos(
            'rFoot', self.getCenterPos()[1][0]+self.speed*self.movingDirection,
            self.getCenterPos()[1][1])
            
    def kickBall(self, ballCenterPos, ballCenter, lFootIndex):
        '''This function moves the foot to kick the ball.
        ballCenter is the ball center and ballCenterPos is its coordinates.
        lFootIndex is the index of the left foot in allThings and in allPos.'''
        # choose the foot that will kick the ball
        kickingFoot = self.chooseKickingFoot(ballCenterPos)
        # prepare the foot for the kicking motion
        currentRot, endPoint, newCenterPos, rotate = \
                    self.prepareBallKick(kickingFoot, ballCenterPos, ballCenter)
        # check if the foot has touched the ball
        self.checkBallTouch(newCenterPos, endPoint)
        if self.touchedBall:   # foot has touched ball --> update foot
            self.updateKickingFoot(kickingFoot, newCenterPos, rotate,
                                   currentRot, lFootIndex)
        
class Outfielder(Player):
    '''This class is a child class of Player and has two methods: __init__, move,
    and kickBall.
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

    def move(self, moveType, direction, ballCenter, ballCenterPos):
        '''This function moves the striker according to the specified type
        of movement.
        ballCenter is the ball's center and ballCenterPos is its coordinates.'''
        if moveType == 'circle':
            self.moveAroundBall(ballCenterPos, direction)
        elif moveType == 'straight':
            self.moveStraight(direction)
        else:
            self.moveToBall(ballCenter, ballCenterPos)
        
    def kickBall(self, ballCenterPos, ballCenter, gkHasBall, lFootIndex):
        '''This function moves the foot to kick the ball.
        ballCenter is the ball center and ballCenterPos is its coordinates.
        gkHasBall is whether or not the goalkeeper currently has the ball. If
        yes, the outfielder cannot perform the kicking motion.
        lFootIndex is the index of the left foot in the list of everything on
        the screen.'''
        # choose the foot that will kick the ball
        kickingFoot = self.chooseKickingFoot(ballCenterPos)
        # prepare the foot for the kicking motion
        currentRot, endPoint, newCenterPos, rotate = \
                    self.prepareBallKick(kickingFoot, ballCenterPos, ballCenter)
        if gkHasBall == False:
            # update foot
            self.updateKickingFoot(kickingFoot, newCenterPos, rotate,
                                   currentRot, lFootIndex)
        # check if the foot has touched the ball
        self.checkBallTouch(newCenterPos, endPoint)
