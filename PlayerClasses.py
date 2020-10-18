'''This module defines the Player class. To get a brief description of the class,
use the following syntax: <module name as imported>.Player.__doc__'''

import pygame, random, math
import LineParams as line
import MoveFunctionsUpdated as move
import NonplayerClasses as np

class Player(np.Game):
    '''This class is a child class of Game, which is defined in the
    module NonplayerClass.py. It's also the parent class of Goalkeeper
    and Outfielder. Player has the following methods: __init__, load,
    setFootStartPos, adjustFootStartPos, blitFeet, blitBody,
    getStartPos, getCenter, setCenterPos, getCenterPos, getCorners,
    getRotation, getShoulderAngle, getBodyAngle, getFootAngle,
    setMovingRotation, getMovingRotation, getDistanceMoved,
    getDistanceToBall, getEnding, feetToFront, move, chooseKickingFoot,
    kickBall, checkBallTouch, updateFeet, and updateAll.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Player.<method name>.__doc__'''
    def __init__(self, screenSize):
        '''This function initializes the class and sets its core attributes.'''
        np.Game.__init__(self, screenSize)   # initialize the parent class
        self.lFoot, self.rFoot, self.body = [None] * 3
        self.strongFoot = random.choice(['lFoot', 'rFoot'])
        
    def load(self, imageName1, imageName2):
        '''This function loads images of the player's foot and body into PyGame
        and rotates them 90 degrees counterclockwise.'''
        self.lFoot = self.loadImage(imageName1, 35, 30)
        self.body = self.loadImage(imageName2, 48, 70)
        # rotate 90 degrees clockwise
        self.lFoot = pygame.transform.rotate(self.lFoot, 90)
        self.rFoot = self.lFoot
        self.body = pygame.transform.rotate(self.body, 90)
        # holder variables for values at the start of the program (i.e.,
        # before any change/movement has been made)
        self.footStart, self.bodyStart = self.lFoot, self.body
        self.footStartCenter = self.footStart.get_rect().center
        self.bodyStartCenter = self.bodyStart.get_rect().center

    def setFootStartPos(self):
        '''This function sets the positions where the feet will be drawn,
        assuming that the player will be facing upward at the start of
        the program.'''
        self.getCenter()   # center points
        # coordinates of the body center at the start of the program (i.e.,
        # before any change/movement has been made)
        self.bodyCenterPos = (self.bodyStartPos[0]+self.bodyStartCenter[0],
                              self.bodyStartPos[1]+self.bodyStartCenter[1])
        # position of the feet
        self.lFootStartPos = (self.bodyCenterPos[0]-self.footCenter[0]*2-3,
                              self.bodyStartPos[1]+2)
        self.rFootStartPos = self.bodyCenterPos[0]+3, self.lFootStartPos[1]
        # coordinates of the foot centers at the start of the program
        self.lFootCenterPos = (self.lFootStartPos[0]+self.footStartCenter[0],
                               self.lFootStartPos[1]+self.footStartCenter[1])
        self.rFootCenterPos = (self.rFootStartPos[0]+self.footStartCenter[0],
                               self.rFootStartPos[1]+self.footStartCenter[1])

    def adjustFootStartPos(self):
        '''This function adjusts the positions where the feet will be drawn at
        the start of the program. To do that, both the coordinates of the body
        center and those of the foot centers are adjusted.'''
        newBodyCenterPos = (self.bodyStartPos[0]+self.getCenter()[1][0],
                            self.bodyStartPos[1]+self.getCenter()[1][1])
        # distance from the old coordinates
        moveX, moveY = self.getDistanceMoved(newBodyCenterPos)
        self.setCenterPos('body', newBodyCenterPos[0], newBodyCenterPos[1])
        self.setCenterPos('lFoot', self.getCenterPos()[0][0]+moveX,
                          self.getCenterPos()[0][1]+moveY)
        self.setCenterPos('rFoot', self.getCenterPos()[1][0]+moveX,
                          self.getCenterPos()[1][1]+moveY)
        self.setMovingRotation(self.startRot)
        self.feetToFront()
        self.lFootStartPos = (
            self.getCenterPos()[0][0]-self.getCenter()[0][0],
            self.getCenterPos()[0][1]-self.getCenter()[0][1])
        self.rFootStartPos = (
            self.getCenterPos()[1][0]-self.getCenter()[0][0],
            self.getCenterPos()[1][1]-self.getCenter()[0][1])

    def blitFeet(self):
        '''This function rotates both the feet and the body and then draws only
        the feet onto the screen.
        rotate is the angle (measured in degrees) by which the feet will be
        rotated from the original upward rotation.'''
        self.setFootStartPos()   # where the feet will be drawn
        # rotate both feet and body
        self.lFoot = pygame.transform.rotate(self.lFoot, self.startRot)
        self.rFoot = pygame.transform.rotate(self.rFoot, self.startRot)
        self.body = pygame.transform.rotate(self.body, self.startRot)
        self.adjustFootStartPos()
        # draw feet
        self.screen.blit(self.lFoot, self.lFootStartPos)
        self.screen.blit(self.rFoot, self.rFootStartPos)
        self.things = [self.lFoot, self.rFoot]
        
    def blitBody(self):
        '''This function draws the body onto the screen.
        rotate is the angle (measured in degrees) by which the image will be
        rotated from the original upward rotation.'''
        self.screen.blit(self.body, self.bodyStartPos)
        self.things += [self.body]
        # coordinates of the body center at the start of the program (i.e.,
        # before any change/movement has been made)
        self.bodyStartCenterPos = self.bodyCenterPos

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
        '''This function returns the coordinates of the centers of the feet
        and of the body.'''
        return self.lFootCenterPos, self.rFootCenterPos, self.bodyCenterPos

    def getCorners(self):
        '''This function returns a list containing the coordinates of the
        four corners of the player's body. The corners are listed in the
        following order: front left, front right, back left, and back right.
        Note that the size of the original image (before resizing) was
        (31, 22), and and that the image of the body has extra pixels along
        both the front and the back to account for the player's head.'''
        # number of extra pixels along each side (front/back)
        extraPix = 3 / 22 * self.bodyStart.get_rect().height
        # coordinates of the body center
        bodyCenterPos = self.getCenterPos()[2]
        # coordinates of the corners if the player were/is facing upward
        corner1 = (bodyCenterPos[0]-self.bodyStartCenter[0],
                   bodyCenterPos[1]-self.bodyStartCenter[1]+extraPix)
        corner2 = corner1[0]+self.bodyStartCenter[0]*2, corner1[1]
        corner3 = corner1[0], corner1[1]+(self.bodyStartCenter[1]-extraPix)*2
        corner4 = corner2[0], corner3[1]
        corners = [corner1, corner2, corner3, corner4]
        # account for player's current rotation
        for i in range(len(corners)):
            corners[i] = move.rotate('right', corners[i], bodyCenterPos,
                                     step=self.getRotation())[0]
        return corners

    def getRotation(self):
        '''This function returns the player's current rotation, i.e., the
        direction the player is currently facing. It is an angle (measured in
        degrees) formed by two lines: (1) the line connecting the body center
        and the midpoint between the two foot centers, and (2) the y-axis
        pointing downward.'''
        # coordinates of the midpoint between the two foot centers
        midpoint = ((self.getCenterPos()[0][0]+self.getCenterPos()[1][0])/2,
                    (self.getCenterPos()[0][1]+self.getCenterPos()[1][1])/2)
        # current rotation
        currentRot = line.getParams(midpoint, self.getCenterPos()[2])[3]
        return currentRot

    def getShoulderAngle(self):
        '''This function returns the angle (between 0 and 90 degrees)
        between the line connecting the player's shoulders and the y-axis.'''
        frontCorners = self.getCorners()[:2]
        shoulderAngle = line.getIntersect(frontCorners[0], frontCorners[1],
                                          (0,0), (0,1))[2]
        return shoulderAngle
        
    def getBodyAngle(self, ball):
        '''This function returns the angle (measured in degrees) of the body
        with respect to the y-axis pointing downward from the ball.'''
        return line.getParams(ball.getCenterPos(), self.getCenterPos()[2])[3]

    def getFootAngle(self, ball):
        '''This function returns the angles (measured in degrees) of the feet
        with respect to the y-axis pointing downward from the ball.'''
        lFootAngle = line.getParams(ball.getCenterPos(),
                                    self.getCenterPos()[0])[3]
        rFootAngle = line.getParams(ball.getCenterPos(),
                                    self.getCenterPos()[1])[3]
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

    def getDistanceMoved(self, newCenterPos):
        '''This function returns the change in the position of the body
        after a movement.
        newCenterPos is the new coordinates of the center of the body.'''
        moveX, moveY = line.getParams(newCenterPos, self.getCenterPos()[2])[:2]
        return moveX, moveY

    def getDistanceToBall(self, ball):
        '''This function returns the distance between each foot and the ball.'''
        lFootToBall = line.getParams(ball.getCenterPos(),self.getCenterPos()[0])[2]
        rFootToBall = line.getParams(ball.getCenterPos(),self.getCenterPos()[1])[2]
        return lFootToBall, rFootToBall

    def getEnding(self, bodyPart, ball):
        '''This function returns the point to which the body will move when
        it's headed for the ball, along with the direction the body/foot will
        face when it reaches the endpoint (angle measured in degrees).'''
        if 'Foot' in bodyPart:
            finalDist = self.footStartCenter[1] + ball.center[1]
            if bodyPart == 'lFoot':
                angle = self.getFootAngle(ball)[0]
            else:
                angle = self.getFootAngle(ball)[1]
        else:
            finalDist = self.bodyStartCenter[1] + ball.center[1]
            angle = self.getBodyAngle(ball)
        # point to which the body will move
        endPointX = ball.getCenterPos()[0] + finalDist * np.getTrig(angle)[0]
        endPointY = ball.getCenterPos()[1] + finalDist * np.getTrig(angle)[1]
        endPoint = endPointX, endPointY
        # final rotation, i.e., direction the body will face when it reaches
        # the endpoint (measured in degrees)
        endAngle = line.getParams(ball.getCenterPos(), endPoint)[3]
        return endPoint, endAngle

    def feetToFront(self):
        '''This function moves the feet to the front of the body.
        target is either the coordinates of the point around which the player
        rotates or the coordinates of the point to which the player moves.'''
        currentRot = self.getRotation()   # measured in degrees
        # move feet
        self.lFootCenterPos = move.rotate(
            'right', self.getCenterPos()[0], self.getCenterPos()[2],
            step=self.getMovingRotation()-currentRot)[0]
        self.rFootCenterPos = move.rotate(
            'right', self.getCenterPos()[1], self.getCenterPos()[2],
            step=self.getMovingRotation()-currentRot)[0]

    def move(self, moveType, direction, ball):
        '''This function moves the player in one of three ways: in a straight
        line, straight toward the ball, or in a circle around the ball.'''
        # move body
        if moveType == 'straight':
            newCenterPos, rotate = move.straight(
                direction,self.getCenterPos()[2],objCenter=self.getCenter()[1],
                screenSize=(self.screenWidth,self.screenHeight))
        elif moveType == 'to ball':
            endPoint, endAngle = self.getEnding('body', ball)
            newCenterPos, rotate = move.toPoint(self.getCenterPos()[2],
                                                endPoint, endAngle, 3)
        elif moveType == 'circle':
            bodyAngle = self.getBodyAngle(ball)
            newCenterPos, rotate = move.rotate(
                direction, self.getCenterPos()[2], ball.getCenterPos(),
                screenSize=(self.screenWidth,self.screenHeight),
                objCenter=self.getCenter()[1])
        if newCenterPos != self.getCenterPos()[2]:
            self.moved = True
            moveX, moveY = self.getDistanceMoved(newCenterPos)
            self.setCenterPos('body', newCenterPos[0], newCenterPos[1])
            self.setMovingRotation(rotate)
            # move feet at the same distance as body
            self.setCenterPos('lFoot', self.getCenterPos()[0][0]+moveX,
                              self.getCenterPos()[0][1]+moveY)
            self.setCenterPos('rFoot', self.getCenterPos()[1][0]+moveX,
                              self.getCenterPos()[1][1]+moveY)
            if self.getRotation() != self.getMovingRotation():
                # player facing the wrong direction
                self.feetToFront()

    def chooseKickingFoot(self, ball):
        '''This function chooses the foot that will kick the ball and returns:
        (1) a string indicating the foot,
        (2) the coordinates of the foot's center point, and
        (3) the distance between the ball and that foot.'''
        lFootToBall, rFootToBall = self.getDistanceToBall(ball)
        if lFootToBall < rFootToBall:
            return 'lFoot', self.getCenterPos()[0], lFootToBall
        elif lFootToBall > rFootToBall:
            return 'rFoot', self.getCenterPos()[1], rFootToBall
        else:   # ball is equidistant from both feet
            if self.strongFoot == 'lFoot':
                return self.strongFoot, self.getCenterPos()[0], lFootToBall
            else:
                return self.strongFoot, self.getCenterPos()[1], rFootToBall

    def kickBall(self, ball, gk=False):
        '''This function moves one of the feet to kick the ball.
        gk denotes whether or not the player is the goalkeeper.
        If he is, he only kicks the ball when it's nearby. If not, he
        only kicks the ball when it's not in the goalkeeper's possession.'''
        currentRot = self.getRotation()   # measured in degrees
        kickingFoot, kFootCenterPos, distToBall = self.chooseKickingFoot(ball)
        if kickingFoot == 'lFoot':
            endAngle = self.getFootAngle(ball)[0]
        else:
            endAngle = self.getFootAngle(ball)[1]
        if distToBall <= self.footStartCenter[1] + ball.center[1]:
            # foot is already very close to the ball
            endPoint = kFootCenterPos
        else:
            endPoint = self.getEnding(kickingFoot, ball)[0]
        # move foot
        newKFootCenterPos, kFootRotate = move.toPoint(kFootCenterPos,
                                                      endPoint, endAngle)
        if newKFootCenterPos == endPoint:
            self.touchedBall = True
        else:
            self.touchedBall = False
        if (gk and self.touchedBall) or ((not gk) and (not ball.gkCaught)):
            if kickingFoot == 'lFoot':
                newCenterPos = newKFootCenterPos, self.getCenterPos()[1]
                rotate = kFootRotate, currentRot
            else:
                newCenterPos = self.getCenterPos()[0], newKFootCenterPos
                rotate = currentRot, kFootRotate
            self.updateFeet(kickingFoot, newCenterPos, rotate)
            self.updateDisplay()
            pygame.time.wait(100)   # pause program for 100 ms
            # bring foot back to its position and rotation before the kick
            if kickingFoot == 'lFoot':   # left foot is the kicking foot
                newCenterPos = kFootCenterPos, self.getCenterPos()[1]
            else:   # right foot is the kicking foot
                newCenterPos = self.getCenterPos()[0], kFootCenterPos
            self.updateFeet(kickingFoot, newCenterPos, (currentRot,)*2)
        
    def updateFeet(self, foot, newCenterPos, rotate):
        '''This function updates the positions and rotations of only the feet.
        newCenterPos is a tuple/list of the new coordinates of the center
        of each foot.
        rotate is an array of the angles (measured in degrees) by which
        the rotations of the feet have changed from those at the start of
        the program.'''
        moved = self.lFoot, self.rFoot, self.footStart, self.footStart
        lFootIndex = self.allThings.index(self.lFoot)
        move.update(self.screen, self.allThings, self.allPos, moved,
                    newCenterPos, rotate)
        self.lFoot, self.rFoot = self.allThings[lFootIndex:lFootIndex+2]
        if self.strongFoot == 'lFoot':
            self.strongFoot = self.lFoot
        else:
            self.strongFoot = self.rFoot
        self.footCenter = self.getCenter()[0]   # new center point

    def updateAll(self):
        '''This function updates the positions and rotations of both the body
        and the feet.'''
        moved = (self.lFoot, self.rFoot, self.body,
                 self.footStart, self.footStart, self.bodyStart)
        newCenterPos = self.getCenterPos()
        lFootIndex = self.allThings.index(self.lFoot)
        bodyIndex = self.allThings.index(self.body)
        move.update(self.screen, self.allThings, self.allPos, moved,
                    newCenterPos, rotate=(self.getMovingRotation(),)*3)
        # new values
        self.lFoot, self.rFoot = self.allThings[lFootIndex:lFootIndex+2]
        self.body = self.allThings[bodyIndex]
        self.footCenter, self.bodyCenter = self.getCenter()

class Goalkeeper(Player):
    '''This class is a child class of Player and has the following methods:
    __init__ and moveAcross.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Goalkeeper.<method name>.__doc__'''
    def __init__(self, screenSize):
        '''This function initializes the class and sets its core attributes.'''
        Player.__init__(self, screenSize)   # initialize the parent class
        self.bodyStartPos = (self.screenWidth-76)/2, 80
        self.startRot = 180   # measured in degrees
        self.direction = random.choice([1, -1])   # right or left
        self.speed = 5   # number of pixels per movement

    def moveAcross(self, goal):
        '''This function makes the goalkeeper move between the goal posts,
        only stopping when he catches the ball (i.e., when the ball hits
        the front of his body).'''
        currentRot = self.getRotation()   # measured in degrees
        # points to which the player will move
        lEndPoint = goal.getPosts()[0] + self.getCenter()[1][0]
        rEndPoint = goal.getPosts()[1] - self.getCenter()[1][0]
        if self.direction == 1:   # playing moving to the right
            if self.getCenterPos()[2][0] >= rEndPoint:   # reached right post
                self.direction = -1
        else:   # player moving left
            if self.getCenterPos()[2][0] <= lEndPoint:   # reached left post
                self.direction = 1
        # move player
        self.setCenterPos('body',
                          self.getCenterPos()[2][0]+self.speed*self.direction,
                          self.getCenterPos()[2][1])
        self.setCenterPos('lFoot',
                          self.getCenterPos()[0][0]+self.speed*self.direction,
                          self.getCenterPos()[0][1])
        self.setCenterPos('rFoot',
                          self.getCenterPos()[1][0]+self.speed*self.direction,
                          self.getCenterPos()[1][1])

class Outfielder(Player):
    '''This class is a child class of Player and has only one method: __init__.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Outfielder.<method name>.__doc__'''
    def __init__(self, screenSize):
        '''This function initializes the class and sets its core attributes.'''
        Player.__init__(self, screenSize)   # initialize the parent class
        bodyStartPosX = random.uniform(20, self.screenWidth-96)
        bodyStartPosY = random.uniform(self.screenHeight-150,
                                       self.screenHeight-100)
        self.bodyStartPos = bodyStartPosX, bodyStartPosY
        self.startRot = 0
        self.moved = False
