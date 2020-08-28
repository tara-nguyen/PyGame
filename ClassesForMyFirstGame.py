'''The following classes are defined: Game, Background, Goal, Player, and Ball.'''

import pygame, random, math
import CroppingImages as crop
import LineParams as line
import MoveFunctions as move

class Game:
    '''This class is the parent of classes Background, Goal, Player, and Ball.
    This class has the following methods: __init__, updateDisplay, getFile,
    loadImage, and processMoveKeys.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Game.<method name>.__doc__'''
    def __init__(self, screenSize):
        '''This function initializes the class and sets its core attributes.'''
        # screen size
        self.screenWidth = screenSize[0]
        self.screenHeight = screenSize[1]
        self.screen = pygame.display.set_mode(screenSize)
        self.screenCenter = self.screenWidth/2, self.screenHeight/2
        self.fps = 30   # maxmium number of frames per second
        self.frame = pygame.time.Clock()   # initialize clock
        
    def updateDisplay(self):
        '''This function updates the display and sets the maximum number of
        frames per second.'''
        pygame.display.flip()   # update/clear display
        self.frame.tick(self.fps)   # maximum number of frames per second
        
    def getFile(self, imageName):
        '''This function returns the link to the images stored in the computer.'''
        file = './ImagesInPyGame/' + imageName + '.png'
        return file

    def loadImage(self, imageName, newWidth=False, newHeight=False):
        '''This function loads an image into PyGame and resizes it if required.'''
        image = pygame.image.load(self.getFile(imageName)).convert_alpha()
        if newWidth != False and newHeight == False:
            # change the width but not the height
            newHeight = image.get_rect().height
        if newWidth == False and newHeight != False:
            # change the height but not the width
            newWidth = image.get_rect().width
        if newWidth != False or newHeight != False:
            # resize image
            image = pygame.transform.scale(image, (newWidth, newHeight))
        return image

    def processMoveKeys(self, pressedKeys):
        '''This function processes pressed keys that will initiate
        player movements.'''
        # keys used for player movements
        self.moveKeys = ('left', 'left-rshift', 'right', 'right-rshift',
                         'up', 'down','space')
        pressed, direction, moveType = [None] * 3
        if pressedKeys[pygame.K_LEFT] == 1:
            # left arrow key has been pressed
            direction = 'left'   # movement direction
            if pressedKeys[pygame.K_RSHIFT] == 1:
                # right shift key has also been pressed at the same time
                pressed = 'left-rshift'
                moveType = 'circle'   # type of movement
            else:
                # right shift key not pressed
                pressed = 'left'
                moveType = 'straight'   # type of movement
        if pressedKeys[pygame.K_RIGHT] == 1:
            # right arrow key has been pressed
            direction = 'right'   # movement direction
            if pressedKeys[pygame.K_RSHIFT] == 1:
                # right shift key has also been pressed  at the same time
                pressed = 'right-rshift'
                moveType = 'circle'   # type of movement
            else:
                # right shift key not pressed 
                pressed = 'right'
                moveType = 'straight'   # type of movement
        if pressedKeys[pygame.K_UP] == 1:
            # up arrow key has been pressed
            pressed = 'up'
            direction = 'up'   # movement direction
            moveType = 'straight'   # type of movement
        if pressedKeys[pygame.K_DOWN] == 1:
            # down arrow key has been pressed
            pressed = 'down'
            direction = 'down'   # movement direction
            moveType = 'straight'   # type of movement
        if pressedKeys[pygame.K_SPACE] == 1:
            # spacebar has been pressed
            pressed = 'space'
            direction = None
            moveType = 'to ball'
        return pressed, direction, moveType
        
class Background(Game):
    '''This class is a child of the Game class. This class has two methods:
    __init__ and blit.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Background.<method name>.__doc__'''
    def __init__(self, screenSize):
        '''This function initializes the class and sets its core attributes.'''
        Game.__init__(self, screenSize)   # initialize the parent class
        self.grass = None   # contains nothing

    def blit(self, imageName):
        '''This function loads and draws the background image onto the screen.'''
        self.grass = Game.loadImage(self, imageName,
                                    self.screenWidth, self.screenHeight)
        self.pos = 0, 0   # where the image will be drawn
        self.screen.blit(self.grass, self.pos)
        
class Goal(Game):
    '''This class is a child of the Game class. This class has the following
    methods: __init__, crop, load, setPos, blit, getPos, getCenter, and
    getCenterPos.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Goal.<method name>.__doc__'''
    def __init__(self, screenSize):
        '''This function initializes the class and sets its core attributes.'''
        Game.__init__(self, screenSize)   # initialize the parent class
        self.left = None
        self.middle = None
        self.right = None
        self.sideWidth = 60   # final width of the left and right goal parts
        self.middleWidth = 120   # final width of the middle goal part
        self.height = self.screenHeight / 7   # final goal height

    def crop(self, image, newWidth, newHeight, shiftLeft):
        '''This function crops an image and returns the new surface on which
        the final image will be pasted.'''
        newSurface = crop.cropImage(image, 'pixels', newWidth, newHeight,
                                    shiftLeft=shiftLeft, shiftUp=33)
        return newSurface

    def load(self, imageName1, imageName2, imageName3):
        '''This function loads images of the goal parts into PyGame
        and crops them.'''
        scale = 130, 250   # used to resize the images
        self.left = Game.loadImage(self, imageName1, scale[0], scale[1])
        self.middle = Game.loadImage(self, imageName2, scale[0], scale[1])
        self.right = Game.loadImage(self, imageName3, scale[0], scale[1])
        # crop
        self.left = self.crop(self.left, self.sideWidth, self.height,
                              shiftLeft=11)
        self.middle = self.crop(self.middle, self.middleWidth, self.height,
                                shiftLeft=(scale[0]-self.middleWidth)/2)
        self.right = self.crop(self.right, self.sideWidth, self.height,
                               shiftLeft=scale[0]-self.sideWidth-11)

    def setPos(self):
        '''This function sets the positions where the goal parts will be drawn.'''
        self.lCenter, self.mCenter, self.rCenter = self.getCenter()
        self.mPos = self.screenCenter[0]-self.mCenter[0], 0
        self.lPos = self.mPos[0]-self.sideWidth, 0
        self.rPos = self.mPos[0]+self.middleWidth, 0

    def blit(self, imageName1, imageName2, imageName3):
        '''This function draws the goal parts onto the screen.'''
        self.load(imageName1, imageName2, imageName3)
        self.setPos()
        self.screen.blit(self.left, self.lPos)
        self.screen.blit(self.middle, self.mPos)
        self.screen.blit(self.right, self.rPos)
        
    def getPos(self):
        '''This function returns the positions of the all three goal parts.'''
        return [self.lPos, self.mPos, self.rPos]

    def getCenter(self):
        '''This function returns the centers of the goal parts.'''
        self.lCenter = self.left.get_rect().center
        self.mCenter = self.middle.get_rect().center
        self.rCenter = self.right.get_rect().center
        return self.lCenter, self.mCenter, self.rCenter

    def getCenterPos(self):
        '''This function returns the coordinates of the center of each
        goal part.'''
        # positions of the goal parts (i.e., where they were drawn)
        self.lPos, self.mPos, self.rPos = self.getPos()
        # centers of the goal parts
        self.lCenter, self.mCenter, self.rCenter = self.getCenter()
        # coordinates of the centers
        self.lCenterPos = (self.lPos[0]+self.lCenter[0],
                           self.lPos[1]+self.lCenter[1])
        self.mCenterPos = (self.mPos[0]+self.mCenter[0],
                           self.mPos[1]+self.mCenter[1])
        self.rCenterPos = (self.rPos[0]+self.rCenter[0],
                           self.rPos[1]+self.rCenter[1])
        return [self.lCenterPos, self.mCenterPos, self.rCenterPos]

    def getPosts(self):
        '''This function returns the x-coordinates & the size of the goal posts.'''
        leftPost, rightPost = self.lPos[0], self.rPos[0]+self.sideWidth
        postWidth, postHeight = 11, self.height
        return leftPost, rightPost, postWidth, postHeight

class Player(Game):
    '''This class is a child of the Game class. This class has the following
    methods: __init__, load, setStartPos, blit, getPos, getCenter, setCenterPos,
    getCenterPos, getMidpoint, getRotation, setMovingRotation, getMovingRotation,
    getBodyAngle, getFootAngle, feetToFront, setStep, getDistanceMoved, 
    getSinCos, getEnding, moveAroundBall, moveStraight, moveToBall, move, 
    updatePlayer, updateFoot, getDistanceToBall, chooseKickingFoot, and kickBall.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Player.<method name>.__doc__'''
    def __init__(self, screenSize):
        '''This function initializes the class and sets its core attributes.'''
        Game.__init__(self, screenSize)   # initialize the parent class
        self.lFoot = None   # contains nothing
        self.rFoot = None
        self.body = None
        self.footWidth = 44
        self.footHeight = 30
        self.bodyWidth = 52
        self.bodyHeight = 76
        
    def load(self, imageName1, imageName2):
        '''This function loads images of the player's feet and body into PyGame
        and rotates them 90 degrees counterclockwise.'''
        self.lFoot = Game.loadImage(self, imageName1,
                                    self.footWidth, self.footHeight)
        self.rFoot = Game.loadImage(self, imageName1,
                                    self.footWidth, self.footHeight)
        self.body = Game.loadImage(self, imageName2,
                                   self.bodyWidth, self.bodyHeight)
        # rotate
        self.lFoot = pygame.transform.rotate(self.lFoot, 90)
        self.rFoot = pygame.transform.rotate(self.rFoot, 90)
        self.body = pygame.transform.rotate(self.body, 90)
        # sizes of the feet and the body after the rotation
        self.footWidth = self.lFoot.get_rect().width
        self.footHeight = self.lFoot.get_rect().height
        self.bodyWidth = self.body.get_rect().width
        self.bodyHeight = self.body.get_rect().height
        # duplicates to hold the images at the start of the program (i.e.,
        # before any change/movement has been made)
        self.footStart = self.lFoot
        self.bodyStart = self.body
        
    def setStartPos(self):
        '''This function sets the positions where the feet and the body will be
        drawn at the start of the program.'''
        self.footCenter, self.bodyCenter = self.getCenter()
        # holder variables for the centers at the start of the program
        self.footCenterStart = self.footCenter
        self.bodyCenterStart = self.bodyCenter
        # position of the body
        bodyPosX = random.uniform(0, self.screenWidth-self.bodyCenter[0]*2)
        bodyPosY = random.uniform(self.screenHeight/7,
                                  self.screenHeight-self.bodyCenter[1]*2)
        self.bodyPos = bodyPosX, bodyPosY
        # coordinates of the body center at the start of the program
        self.bodyCenterPos = (bodyPosX+self.bodyCenterStart[0],
                              bodyPosY+self.bodyCenterStart[1])
        # how many pixels of the feet stick out from the front of the body
        self.feetOut = 1   
        # position of the feet
        self.lFootPos = (self.bodyCenterPos[0]-self.footWidth-1,
                         bodyPosY-self.feetOut)
        self.rFootPos = self.bodyCenterPos[0]+1, self.lFootPos[1]
        # coordinates of the foot centers at the start of the program
        self.lFootCenterPos = (self.lFootPos[0]+self.footCenterStart[0],
                               self.lFootPos[1]+self.footCenterStart[1])
        self.rFootCenterPos = (self.rFootPos[0]+self.footCenterStart[0],
                               self.rFootPos[1]+self.footCenterStart[1])

    def blit(self, imageName1, imageName2, bodyPart):
        '''This function draws the feet and the body onto the screen.'''
        if bodyPart == 'feet':
            self.load(imageName1, imageName2)
            self.setStartPos()
            self.screen.blit(self.lFoot, self.lFootPos)
            self.screen.blit(self.rFoot, self.rFootPos)
        else:
            self.screen.blit(self.body, self.bodyPos)
        
    def getPos(self):
        '''This function returns the positions of the feet and the body at the
        start of the program.'''
        return [self.lFootPos, self.rFootPos, self.bodyPos]

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
                newCenterPos = move.moveCircle(
                    self.getCenterPos()[2], self.getCenterPos()[0], 'right',
                    step=self.getBodyAngle(target)-currentRot)[0]
                self.setCenterPos('lFoot', newCenterPos[0], newCenterPos[1])
                newCenterPos = move.moveCircle(
                    self.getCenterPos()[2], self.getCenterPos()[1], 'right',
                    step=self.getBodyAngle(target)-currentRot)[0]
                self.setCenterPos('rFoot', newCenterPos[0], newCenterPos[1])
        else:
            # player is already at the target point
            newCenterPos = move.moveCircle(
                self.getCenterPos()[2], self.getCenterPos()[0], 'right',
                step=self.getMovingRotation()-currentRot)[0]
            self.setCenterPos('lFoot', newCenterPos[0], newCenterPos[1])
            newCenterPos = move.moveCircle(
                self.getCenterPos()[2], self.getCenterPos()[1], 'right',
                step=self.getMovingRotation()-currentRot)[0]
            self.setCenterPos('rFoot', newCenterPos[0], newCenterPos[1])
    
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
        # distance moved
        moveX, moveY = self.getDistanceMoved(newCenterPos)
        if round(moveX, 5) != 0 or round(moveY, 5) != 0:
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
            newCenterPos = move.moveCircle(
                ballCenterPos, self.getCenterPos()[0], direction, step=step)[0]
            # new coordinates of the center of the left foot
            self.setCenterPos('lFoot', newCenterPos[0], newCenterPos[1])
            newCenterPos = move.moveCircle(
                ballCenterPos, self.getCenterPos()[1], direction, step=step)[0]
            # new coordinates of the center of the right foot
            self.setCenterPos('rFoot', newCenterPos[0], newCenterPos[1])
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
        if newCenterPos != self.getCenterPos()[2]:
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
                # player is facing the wrong direction --> move feet around body
                self.feetToFront(newCenterPos)

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
        if newCenterPos != self.getCenterPos()[0]:
            self.moved = True
            # distance moved
            moveX, moveY = self.getDistanceMoved(newCenterPos)
            # new coordinates of the body center
            self.setCenterPos('body', newCenterPos[0], newCenterPos[1])
            self.setMovingRotation(rotate)   # rotation (angled measured in degrees)
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
        
    def updatePlayer(self, allThings, allPos):
        '''This function updates the positions and rotations of both the body
        and the feet.
        allThings is a list of everything on the screen.
        allPos is a list of the positions of everything on the screen.'''
        moved = (self.lFoot, self.rFoot, self.body,
                 self.footStart, self.footStart, self.bodyStart)
        # new coordinates of the centers of the feet and the body
        newCenterPos = self.getCenterPos()
        move.update(self.screen, allThings, allPos, moved, newCenterPos,
                    rotate=(self.getMovingRotation(),)*3)
        self.lFoot, self.rFoot = allThings[-4:-2]
        self.body = allThings[-1]
        # new center points
        self.footCenter, self.bodyCenter = self.getCenter()

    def updateFoot(self, foot, newCenterPos, rotate, allThings, allPos):
        '''This function updates the positions and rotations of only the feet.
        newCenterPos is a tuple/list of the new coordinates of the center of 
        each foot.
        rotate is a tuple/list of the angles (measured in degrees) by which 
        the rotations of the feet have changed from those at the start of
        the program.
        allThings is a list of everything on the screen.
        allPos is a list of the positions of everything on the screen.'''
        moved = self.lFoot, self.rFoot, self.footStart, self.footStart
        move.update(self.screen, allThings, allPos, moved, newCenterPos, rotate)
        self.lFoot, self.rFoot = allThings[-4:-2]
        self.footCenter = self.getCenter()[0]   # new center point
        
    def getDistanceToBall(self, ballCenterPos):
        '''This function returns the distance between each foot and the ball.'''
        lFootToBall = line.getParams(ballCenterPos, self.getCenterPos()[0])[2]
        rFootToBall = line.getParams(ballCenterPos, self.getCenterPos()[1])[2]
        return lFootToBall, rFootToBall
        
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
        
    def kickBall(self, ballCenterPos, ballCenter, allThings, allPos):
        '''This function moves a foot to make the player kick the ball.
        ballCenter is the ball center and ballCenterPos is its coordinates.
        allThings is a list of everything on the screen.
        allPos is a list of the positions of everything on the screen.'''
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
        self.updateFoot(kickingFoot, newCenterPos, rotate, allThings, allPos)
        self.updateDisplay()
        pygame.time.wait(100)   # pause program for 100 ms
        # bring foot back to the position and rotation before the kick
        if kickingFoot == 'lFoot':   # left foot is the kicking foot
            newCenterPos = self.kFootCenterPos, self.getCenterPos()[1]
        else:   # right foot is the kicking foot
            newCenterPos = self.getCenterPos()[0], self.kFootCenterPos
        self.updateFoot(kickingFoot, newCenterPos, (currentRot,)*2,
                        allThings, allPos)
        self.updateDisplay()
        
class Ball(Game):
    '''This class is a child of the Game class. This class has the following
    methods: __init__, blit, getPos, setCenterPos, getCenterPos, setMovingAngle,
    getMovingAngle, getSinCos, setFirstStep, setStep, getStep, setVelocity, 
    getVelocity, decrementStep, getExtremes, setFinalStep1, setFinalStep2, 
    hitGoalPosts, bounceBack, checkBouncing, hitPlayer, checkGoal, moveBall, 
    resetBall, and updateBall.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Ball.<method name>.__doc__'''
    def __init__(self, screenSize):
        '''This function initializes the class and sets its core attributes.'''
        Game.__init__(self, screenSize)   # initialize the parent class
        self.ball = None   # contains nothing
        self.diameter = 36
        
    def blit(self, imageName):
        '''This function loads and draws the ball onto the screen.'''
        self.ball = Game.loadImage(self, imageName, self.diameter, self.diameter)
        X = random.uniform(0, self.screenWidth-self.diameter)
        Y = random.uniform(self.screenHeight/2, self.screenHeight-self.diameter)
        self.pos = X, Y   # where the ball will be drawn
        self.screen.blit(self.ball, self.pos)
        self.center = self.ball.get_rect().center   # center of the ball
        # coordinates of the center at the start of the program
        self.centerPos = X+self.center[0], Y+self.center[1]
        
    def getPos(self):
        '''This function returns the position of the ball at the start of
        the program.'''
        return self.pos

    def setCenterPos(self, X, Y):
        '''This function sets a new position for the ball center.'''
        self.centerPos = X, Y

    def getCenterPos(self):
        '''This function returns the coordinates of the ball center.'''
        return self.centerPos

    def setMovingAngle(self, angle):
        '''This function sets the angle (measured in degrees) at which the ball
        will move, with respect to the negative y-axis pointing up from the
        current ball center.'''
        self.movingAngle = angle

    def getMovingAngle(self):
        '''This function returns the angle (measured in degrees) at which the
        ball is currently moving, with respect to the negative y-axis pointing 
        up from the current ball center.'''
        return self.movingAngle

    def getSinCos(self):
        '''This function returns the sine and cosine of the moving angle.'''
        sine = math.sin(self.movingAngle * math.pi/180)
        cosine = math.cos(self.movingAngle * math.pi/180)
        return sine, cosine
        
    def setFirstStep(self, stepSize):
        '''This function sets the size of the first step that ball will make.'''
        self.stepX = stepSize * self.getSinCos()[0]
        self.stepY = stepSize * self.getSinCos()[1]

    def setStep(self, stepX, stepY):
        '''This function sets the step size for the ball's movements.'''
        self.stepX = stepX
        self.stepY = stepY

    def getStep(self):
        '''This function returns the step size for the ball's movements.'''
        return self.stepX, self.stepY

    def setVelocity(self):
        '''This function sets the velocity of the ball.'''
        self.velocity = self.getStep()
    
    def getVelocity(self):
        '''This function returns the current velocity of the ball.'''
        return self.velocity

    def decrementStep(self):
        '''This function decrements the step size to make the ball move slower.'''
        factor = random.uniform(1.03, 1.05)   # a random real number
        self.setStep(self.stepX/factor, self.stepY/factor)

    def getExtremes(self):
        '''This function returns the coordinates of the leftmost, rightmost, top, 
        and bottom points of the ball'''
        left = self.getCenterPos()[0] - self.center[0]
        right = left + self.diameter
        top = self.getCenterPos()[1] - self.center[1]
        bottom = top + self.diameter
        return left, right, top, bottom

    def setFinalStep1(self, direction, distance):
        '''This function sets the size of the final step before the ball 
        reaches either the screen boundaries or the goal posts.
        direction denotes which way the ball is moving (x-direction or
        y-direction).
        distance is the distance from the ball to the boundary/goal post.'''
        if direction == 'x':
            self.stepX = distance
            self.stepY = self.stepX / (self.getSinCos()[0]/self.getSinCos()[1])
        else:
            self.stepY = distance
            self.stepX = self.stepY * (self.getSinCos()[0]/self.getSinCos()[1])

    def setFinalStep2(self, goalPosts):
        '''This function checks if the ball is about to reach either the screen
        boundaries or the goal posts, and sets the step size accordingly.
        goalPosts denotes the x-coordinates and size of the goal posts.'''
##        print('entered setFinalStep2')
        # the leftmost, rightmost, top, and bottom points on the ball
        left, right, top, bottom = self.getExtremes()
        # set the size of the final step before the ball reaches the
        # screen boundaries
        if self.stepX > left:
##            print('approaching left screen boundary')
            self.setFinalStep1('x', left)
        if self.stepX < right - self.screenWidth:
            self.setFinalStep1('x', right - self.screenWidth)
        if self.stepY > top:
            self.setFinalStep1('y', top)
        if self.stepY < bottom - self.screenHeight:
            self.setFinalStep1('y', bottom - self.screenHeight)
        # set the size of the final step before the ball reaches the goal posts
        if top < goalPosts[-1]:
            if right < goalPosts[0] and self.stepX < right-goalPosts[0]:
                self.setFinalStep1('x', right-goalPosts[0])
            if left > goalPosts[1] and self.stepX > left-goalPosts[1]:
                self.setFinalStep1('x', left-goalPosts[1])
            if left > goalPosts[0]+goalPosts[2] and \
               self.stepX > left-(goalPosts[0]+goalPosts[2]):
                self.setFinalStep1('x', left-(goalPosts[0]+goalPosts[2]))
            if right < goalPosts[1]-goalPosts[2] and \
               self.stepX < right-(goalPosts[1]-goalPosts[2]):
                self.setFinalStep1('x', right-(goalPosts[1]-goalPosts[2]))
##        print('step size',self.stepX,self.stepY)
##        print('ball center pos',self.getCenterPos())
    
    def hitGoalPosts(self, goalPosts):
        '''This function checks if the ball has hit the goal posts.
        goalPosts denotes the x-coordinates and size of the goal posts.
        currentRot is the current rotation of the player (angle measured in
        degrees).'''
        hitOut, hitIn = False, False
        # leftmost, rightmost, top, and bottom points on the ball
        left, right, top, bottom = self.getExtremes()
        # conditions for hitting the outside of the posts
        hitLPFromOut = top < goalPosts[-1] and left < goalPosts[0] and \
                       right >= goalPosts[0] and self.getMovingAngle() < 0 and \
                       self.getMovingAngle() > -180
        hitRPFromOut = top < goalPosts[-1] and right > goalPosts[1] and \
                       left <= goalPosts[1] and self.getMovingAngle() > 0 and \
                       self.getMovingAngle() < 180
        # conditions for hitting the inside of the posts
        hitLPFromIn = top < goalPosts[-1] and \
                      right > goalPosts[0]+goalPosts[2] and \
                      left <= goalPosts[0]+goalPosts[2] and \
                      self.getMovingAngle() > 0 and self.getMovingAngle() < 180
        hitRPFromIn = top < goalPosts[-1] and \
                      left < goalPosts[1]-goalPosts[2] and \
                      right >= goalPosts[1]-goalPosts[2] and \
                      self.getMovingAngle() < 0 and self.getMovingAngle() > -180
        if hitLPFromOut or hitRPFromOut:
            hitOut = True
        elif hitLPFromIn or hitRPFromIn:
            hitIn = True
        return hitOut, hitIn
    
    def bounceBack(self, switch):
        '''This function modifies the velocity and angle to make the ball bounce
        back from a boundary (e.g., one of the screen boundaries or one of the
        goal posts).
        switch denotes whether the direction in which the ball is moving will be
        flipped laterally or vertically.'''
##        print('entered bounceBack')
        factor = random.uniform(1.03, 1.05)   # a random real number
        if switch == 'x':
##            print('ball bouncing back in the x-direction')
            # ball bouncing back in the x-direction
            self.setStep(self.getVelocity()[0]/-factor,
                         self.getVelocity()[1]/factor)
            self.setMovingAngle(-self.getMovingAngle())
        elif switch == 'y':
            # ball bouncing back in the y-direction
            self.setStep(self.getVelocity()[0]/factor,
                         self.getVelocity()[1]/-factor)
            if self.getMovingAngle() < 0:
                self.setMovingAngle(-180 - self.getMovingAngle())
            else:
                self.setMovingAngle(180 - self.getMovingAngle())

    def checkBouncing(self, goalPosts):
        '''This function checks if the ball has reached either the screen
        boundaries or the goal posts, in which case the ball will bounce back
        and the function will return True. Otherwise the function will return
        False.
        goalPosts denotes the x-coordinates and size of the goal posts.'''
##        print('entered checkBouncing')
        # leftmost, rightmost, top, and bottom points on the ball
        left, right, top, bottom = self.getExtremes()
        stepX, stepY = self.getStep()   # current step size
        # After reaching the screen boundaries, the ball will bounce back
        # and continue moving at a reduced speed.
        if left == 0 or right == self.screenWidth or \
           top == 0 or bottom == self.screenHeight:
            if left == 0 or right == self.screenWidth:
##                print('reached screen boundary')
                self.bounceBack('x')
            else:
                self.bounceBack('y')
        # Ball will also bounce back if it hits the goal posts.
        if self.hitGoalPosts(goalPosts)[0]:
            if self.getCenterPos()[1] > goalPosts[-1] and \
               abs(self.getMovingAngle()) < 90:
                # ball bouncing back in the y direction
                self.bounceBack('y')
            else:
                # ball bouncing back in the x direction
                self.bounceBack('x')
        if self.hitGoalPosts(goalPosts)[1]:
            # ball bouncing back in the x direction
            self.bounceBack('x')
##        print('step size',self.stepX,self.stepY)
##        print('ball center pos',self.getCenterPos())
        # return True if the step size has been modified
        if self.stepX != stepX or self.stepY != stepY:
            return True
        else:
            return False
    
    def hitPlayer(self, playerRot, feetMidpoint, minDist):
        '''This function handles ball movements when it runs into the player.
        The ball will stop moving if it hits the player from the front, but will
        bounce back if it hits the player from the back.
        playerRot is the current rotation of the player (angle measured 
        in degrees).
        feetMidpoint is the midpoint of the line connecting the player's feet
        at their centers.
        minDist is the nearest distance to the player that the ball can get.'''
        # distance from ball to the midpoint, and angle (measured in degrees) of
        # the ball with respect to the y-axis pointing down from the midpoint
        dist, angle = line.getParams(feetMidpoint, self.getCenterPos())[2:4]
        # difference between the current rotation of the player and the angle
        # just computed
        angleDiff = abs(playerRot - angle)
        if dist <= minDist:
            if angleDiff >= 100 and angleDiff <= 260:
                # ball reaches the front of the player's body --> stop moving
                self.stepX = 0
                self.stepY = 0
            else:
                # ball reaches the back of the player's body --> bounce back
                self.bounceBack(random.choice(['x','y']))
                
    def checkGoal(self, goalPosts):
        '''This function checks if the player has scored.
        goalPosts denotes the x-coordinates and size of the goal posts.''' 
        # leftmost, rightmost, top, and bottom points on the ball
        left, right, top, bottom = self.getExtremes()
        # Player scores if the ball is between the goal posts.
        if bottom<=goalPosts[-1] and left>=goalPosts[0] and right<=goalPosts[1]:
            return True
        else:
            return False
                
    def moveBall(self, bodyAngle, stepSize, goalPosts, playerRot, feetMidpoint,
                 minDist, allThings, allPos, pressedKeys):
        '''This function handles ball movements when the ball is kicked.
        bodyAngle is the angle (measured in degrees) of the body with respect to
        the y-axis pointing down from the ball.
        goalPosts denotes the x-coordinates and size of the goal posts.
        playerRot is the current rotation of the player (angle measured in
        degrees).
        feetMidpoint is the midpoint of the line connecting the player's feet
        at their centers.
        minDist is the nearest distance to the player that the ball can get.
        allThings is a list of everything on the screen.
        allPos is a list of the positions of everything on the screen.
        pressedKeys is pygame.key.get_pressed(), which tells us which key has
        been pressed.'''
        # angle (measured in degrees) at which the ball will move, with respect
        # to the y-axis pointing up from the current ball center
        self.setMovingAngle(random.uniform(bodyAngle-1, bodyAngle+1))
        self.setFirstStep(stepSize)   # initial step size
        scored = False
        while round(stepSize) > 0:
            self.setVelocity()
##            print('velocity',self.getVelocity())
##            print('ball center pos',self.getCenterPos())
            if self.checkGoal(goalPosts):   # player has scored
                scored = True
            # set the size of the final step before the ball reaches either the
            # screen boundaries or the goal posts
            self.setFinalStep2(goalPosts)
            # new coordinates of the ball center
            self.setCenterPos(self.getCenterPos()[0]-self.stepX,
                              self.getCenterPos()[1]-self.stepY)
            #update ball position and display to show movement
            self.updateBall(allThings, allPos)
            stepX, stepY = self.getStep()   # current step size
##            print('current step size',self.getStep())
            if self.checkBouncing(goalPosts):
                # ball bouncing back after hitting either the screen boundaries
                # or the goal posts
                # new coordinates of the ball center
                self.setCenterPos(self.getCenterPos()[0]-self.stepX,
                                  self.getCenterPos()[1]-self.stepY)
                # update ball position and display to show movement
                self.updateBall(allThings, allPos)
            # movement when ball hits player
            self.hitPlayer(playerRot, feetMidpoint, minDist)
            if self.stepX == 0 and self.stepY == 0:   # ball has stopped moving
                break   # get out of while loop
            elif self.stepX != stepX or self.stepY != stepY:
                # new coordinates of the ball center
                self.setCenterPos(self.getCenterPos()[0]-self.stepX,
                                  self.getCenterPos()[1]-self.stepY)
                # update ball position and display to show movement
                self.updateBall(allThings, allPos)
##            print('decrementing step size')
            self.decrementStep()   # decrement step size
##            print()
            stepSize = math.sqrt(self.stepX**2+self.stepY**2)   # new step size
        # If the player scores, the ball will be placed at a random position
        # after it has stopped moving.
        if scored:
            self.resetBall(allThings, allPos)

    def resetBall(self, allThings, allPos):
        '''This function puts the ball at a random place on the screen in the
        middle of the game.
        allThings is a list of everything on the screen.
        allPos is a list of the positions of everything on the screen.'''
        X = random.uniform(0, self.screenWidth-self.diameter)
        Y = random.uniform(self.screenHeight/2, self.screenHeight-self.diameter)
        # new coordinates of the ball center
        self.setCenterPos(X+self.center[0], Y+self.center[1])
        self.updateBall(allThings, allPos)   # update ball position

    def updateBall(self, allThings, allPos):
        '''This function updates the position of the ball and updates the
        display to show movements.
        allThings is a list of everything on the screen.
        allPos is a list of the positions of everything on the screen.'''
        move.update(self.screen, allThings, allPos, (self.ball,self.ball),
                    (self.getCenterPos(),))
        self.updateDisplay()
