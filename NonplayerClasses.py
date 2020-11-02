'''The following classes are defined: Game, Background, Goal, and Ball.
For neatness, the Player class, which is a child class of Game, is defined in
a different module named PlayerClasses.
To get a brief description of each class, use the following syntax:
    <module name as imported>.<class name>.__doc__
One function not belonging to any of the classes, getTrig(), is also defined
before the Ball class is defined. To get a brief description, use the
following syntax:
    <module name as imported>.getTrig.__doc__'''

import pygame, random, math
import CroppingImages as crop
import LineParams as line
import MoveFunctionsUpdated as move

class Game:
    '''This class is the parent class of Background, Goal, Ball, and Player.
    It has the following methods: __init__, updateDisplay, getFile, loadImage,
    processMoveKeys, and processMovements.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Game.<method name>.__doc__'''
    def __init__(self, screenSize):
        '''This function initializes the class and sets its core attributes.'''
        self.screenWidth = screenSize[0]
        self.screenHeight = screenSize[1]
        self.screen = pygame.display.set_mode(screenSize)
        self.screenCenter = self.screenWidth/2, self.screenHeight/2
        self.clock = pygame.time.Clock()   # Clock object
        
    def updateDisplay(self):
        '''This function updates the display and the clock.'''
        pygame.display.flip()
        self.clock.tick(30)
        
    def getFile(self, imageName):
        '''This function returns the link to the images stored in the computer.'''
        return 'ImagesInPyGame/' + imageName + '.png'

    def loadImage(self, imageName, newWidth=None, newHeight=None):
        '''This function loads an image into PyGame and resizes it if required.'''
        image = pygame.image.load(self.getFile(imageName)).convert_alpha()
        if newWidth != None and newHeight == None:
            newHeight = image.get_rect().height   # height not changed
        elif newWidth == None and newHeight != None:
            newWidth = image.get_rect().width   # width not changed
        if newWidth != None or newHeight != None:
            image = pygame.transform.scale(image, (newWidth, newHeight))
        return image

    def processMoveKeys(self, keypresses):
        '''This function processes pressed keys that will
        initiate player movements.'''
        moveType, direction = None, None
        directions = 'left', 'right', 'up', 'down'
        keys = (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN,
                pygame.K_SPACE, pygame.K_RSHIFT)
        pressed = []
        for key in keys:
                pressed.append(keypresses[key])
        if sum(pressed) == 1:   # only one key pressed
            if pressed.index(1) < 4:   # LEFT, RIGHT, UP, or DOWN key
                moveType = 'straight'
                direction = directions[pressed.index(1)]
            elif pressed.index(1) == 4:   # SPACE key
                moveType = 'to ball'
        elif sum(pressed) == 2:   # two keys pressed at the same time
            if pressed.index(1) < 2:   # LEFT or RIGHT key
                if 1 in pressed[2:4]:   # UP or DOWN key
                    moveType = 'straight'
                    direction = directions[pressed.index(1,2)] + \
                                directions[pressed.index(1)]
                elif pressed[5]:   # RSFHIT key
                    moveType = 'circle'
                    direction = directions[pressed.index(1)]
        return moveType, direction
        
    def processMovements(self, ball, goal, players, keypresses):
        '''This function processes the movements of both the ball
        and the players while the ball is moving.
        players is an array listing the players in the game. The
        goalkeeper must be listed first.'''
        nonkickers = []
        for player in players:
            if player.touchedBall:
                kicker = player
            else:
                nonkickers.append(player)
        bodyAngle = kicker.getBodyAngle(ball)
        ball.apprScrBound, ball.apprGoalPost = False, False
        ball.apprPlayer = [False] * len(players)
        ball.setMovingAngle(random.uniform(bodyAngle-.5, bodyAngle+.5))
        ball.speed = ball.initSpeed
        ball.moving = True
        while ball.moving and round(ball.speed) > 0:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    keypresses[event.key] = 1
                if event.type == pygame.KEYUP:
                    keypresses[event.key] = 0
            # outfielder movements
            movingOutfielder = nonkickers[1]
            minDistToBall = movingOutfielder.getDistToBall(ball)[2]
            for nonkicker in nonkickers[1:]:
                if nonkicker.getDistToBall(ball)[2] < minDistToBall:
                    movingOutfielder = nonkicker
                    minDistToBall = movingOutfielder.getDistToBall(ball)[2]
            moveType, direction = self.processMoveKeys(keypresses)
            movingOutfielder.move(moveType, direction, ball)
            if movingOutfielder.moved:
                movingOutfielder.updateAll()
            # goalkeeper movements
            if ball.getCenterPos()[1] <= goal.getPosts()[2]+self.screenHeight/6:
                players[0].moveAcross(goal)   
            # ball movements
            ball.setStep1()
            stepX, stepY = ball.getStep()   # step size before adjustment
            ball.move(goal, players)
            if not ball.moving:
                break
            ball.update()
            if ball.apprScrBound != False or ball.apprGoalPost != False or \
               sum(ball.apprPlayer) > 0:
                ball.setStep2(stepX, stepY)   # reset
            ball.speed /= random.uniform(1.03, 1.05)   # decrement speed
        kicker.touchedBall = False   # reset
        
class Background(Game):
    '''This class is a child class of Game and has the following methods:
    __init__, load, and blit.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Background.<method name>.__doc__'''
    def __init__(self, screenSize):
        '''This function initializes the class and sets its core attributes.'''
        Game.__init__(self, screenSize)   # initialize the parent class
        self.grass = None
        self.pos = 0, 0   # where the image will be drawn
        
    def load(self, imageName):
        '''This function loads the background image into PyGame.'''
        self.grass = self.loadImage(imageName, self.screenWidth,
                                    self.screenHeight)
        
    def blit(self):
        '''This function draws the background image onto the screen.'''
        self.screen.blit(self.grass, self.pos)
        self.things = [self.grass]

class Goal(Game):
    '''This class is a child class of Game and has the following methods:
    __init__, crop, load, setPos, blit, and getPos.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Goal.<method name>.__doc__'''
    def __init__(self, screenSize):
        '''This function initializes the class and sets its core attributes.'''
        Game.__init__(self, screenSize)   # initialize the parent class
        self.left, self.middle, self.right = [None] * 3
        # widths and height
        self.sideWidth = 60   # left and right parts
        self.middleWidth = 120   # middle part
        self.height = 80
        self.postWidth = 11
        
    def crop(self, image, newWidth, newHeight, shiftLeft):
        '''This function crops an image and returns the new surface on
        which the final image will be pasted.'''
        newSurface = crop.cropImage(image, 'pixels', newWidth, newHeight,
                                    shiftLeft=shiftLeft, shiftUp=53)
        return newSurface

    def load(self, imageName1, imageName2, imageName3):
        '''This function loads images of the goal parts into PyGame
        and crops them.'''
        scale = 130, 250   # used to resize the images
        self.left = self.loadImage(imageName1, scale[0], scale[1])
        self.middle = self.loadImage(imageName2, scale[0], scale[1])
        self.right = self.loadImage(imageName3, scale[0], scale[1])
        # crop
        self.left = self.crop(self.left, self.sideWidth, self.height, 11)
        self.middle = self.crop(self.middle, self.middleWidth, self.height,
                                (scale[0]-self.middleWidth)/2)
        self.right = self.crop(self.right, self.sideWidth, self.height,
                               scale[0]-self.sideWidth-11)
        
    def setPos(self):
        '''This function sets the positions where the goal parts will be drawn.'''
        self.mPos = self.screenCenter[0]-self.middle.get_rect().centerx, 0
        self.lPos = self.mPos[0]-self.sideWidth, 0
        self.rPos = self.mPos[0]+self.middleWidth, 0

    def blit(self):
        '''This function draws the goal parts onto the screen.'''
        self.setPos()
        self.screen.blit(self.left, self.lPos)
        self.screen.blit(self.middle, self.mPos)
        self.screen.blit(self.right, self.rPos)
        self.things = [self.left, self.middle, self.right]
        
    def getPos(self):
        '''This function returns the positions of the all three goal parts.'''
        return [self.lPos, self.mPos, self.rPos]

    def getPosts(self):
        '''This function returns the x-coordinates & the height of
        the goal posts.'''
        postWidth = 11
        leftPost = self.lPos[0] + postWidth / 2
        rightPost = self.rPos[0] + self.sideWidth - postWidth / 2
        return leftPost, rightPost, self.height

def getTrig(angle):
    '''This function returns the sine, cosine, and tangent of an angle.'''
    sin = math.sin(angle * math.pi / 180)
    cos = math.cos(angle * math.pi / 180)
    tan = math.tan(angle * math.pi / 180)
    return sin, cos, tan
    
class Ball(Game):
    '''This class is a child class of Game and has the following methods:
    __init__, load, blit, getStartPos, setCenterPos, getCenterPos,
    setMovingAngle, getMovingAngle, setStep1, setStep2, getStep,
    getNewStep1, getNewStep2, getExtremes, apprScrBounds, apprGoalPosts,
    apprPlayers, bounceOff, bounceOffPl, move, reset, and update.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Ball.<method name>.__doc__'''
    def __init__(self, screenSize):
        '''This function initializes the class and sets its core attributes.'''
        Game.__init__(self, screenSize)   # initialize the parent class
        self.ball, self.diameter = None, 30
##        self.startPos = (self.screenWidth-self.diameter)/2,self.screenHeight-200
        self.startPos = (self.screenWidth-self.diameter)/2,self.screenHeight-50
        self.gkCaught, self.inGoal = False, False
        self.initSpeed = random.uniform(18, 22)

    def load(self, imageName):
        '''This function loads the ball image into PyGame.'''
        self.ball = self.loadImage(imageName, self.diameter, self.diameter)
        
    def blit(self):
        '''This function draws the ball onto the screen.'''
        self.screen.blit(self.ball, self.startPos)
        self.center = self.ball.get_rect().center
        # coordinates of the center at the start of the program (i.e.,
        # before any change/movement has been made)
        self.centerPos = (self.startPos[0]+self.center[0],
                          self.startPos[1]+self.center[1])
        self.things = [self.ball]
        
    def getStartPos(self):
        '''This function returns the position of the ball at the start of
        the program.'''
        return [self.startPos]

    def setCenterPos(self, X, Y):
        '''This function sets a new position for the ball center.'''
        self.centerPos = X, Y

    def getCenterPos(self):
        '''This function returns the coordinates of the ball center.'''
        return self.centerPos

    def setMovingAngle(self, angle):
        '''This function sets the angle (measured in degrees) at which
        the ball will move, with respect to the negative y-axis pointing
        up from the current ball center.'''
        self.movingAngle = angle

    def getMovingAngle(self):
        '''This function returns the angle (measured in degrees) at
        which the ball is currently moving, with respect to the negative
        y-axis pointing up from the current ball center.'''
        return self.movingAngle

    def setStep1(self):
        '''This function sets the step sizes based on the total speed.'''
        self.stepX = self.speed * getTrig(self.getMovingAngle())[0]
        self.stepY = self.speed * getTrig(self.getMovingAngle())[1]

    def setStep2(self, stepX, stepY):
        '''This function sets the step sizes based on the
        changes in x- and y-coordinates.'''
        self.stepX = stepX
        self.stepY = stepY

    def getStep(self):
        '''This function returns the step size for the ball's movements.'''
        return self.stepX, self.stepY

    def getNewStep1(self, stepX):
        '''This function returns new lateral step size and new vertical
        vertical step size when only the former is given.'''
        return stepX, stepX/getTrig(self.getMovingAngle())[2]

    def getNewStep2(self, stepY):
        '''This function returns new lateral step size and new vertical
        vertical step size when only the latter is given.'''
        return stepY*getTrig(self.getMovingAngle())[2], stepY

    def getExtremes(self):
        '''This function returns the x-coordinates of the leftmost and
        rightmost points on the ball, and the y-coordinates of the top
        and bottom points on the ball.'''
        left = self.getCenterPos()[0] - self.center[0]
        right = left + self.diameter
        top = self.getCenterPos()[1] - self.center[1]
        bottom = top + self.diameter
        return left, right, top, bottom

    def apprScrBounds(self):
        '''This function checks if the ball is about to hit the 
        screen boundaries.'''
        approaching = False,
        if not self.apprScrBound:
            # the leftmost, rightmost, top, and bottom points on the ball
            left, right, top, bottom = self.getExtremes()
            if self.stepX > left:
                newStepX, newStepY = self.getNewStep1(left)
                approaching = 'vertb', newStepX, newStepY
            elif self.stepX < right - self.screenWidth:
                newStepX, newStepY = self.getNewStep1(right - self.screenWidth)
                approaching = 'vertb', newStepX, newStepY
            elif self.stepY > top:
                newStepX, newStepY = self.getNewStep2(top)
                approaching = 'horzb', newStepX, newStepY
            elif self.stepY < bottom - self.screenHeight:
                newStepX, newStepY = self.getNewStep2(bottom-self.screenHeight)
                approaching = 'horzb', newStepX, newStepY
        return approaching

    def apprGoalPosts(self, goal):
        '''This function checks if the ball is about to hit the goal posts.'''
        approaching = False,
        if not self.apprGoalPost:
            goalPosts = goal.getPosts()
            # the leftmost, rightmost, and top points on the ball
            left, right, top = self.getExtremes()[:3]
            newStepX, newStepY = self.getStep()
            if right < goalPosts[0] and self.stepX < right - goalPosts[0]:
                # left of left goal post and moving right
                newStepX = right - goalPosts[0]
            elif left > goalPosts[1] and self.stepX > left - goalPosts[1]:
                # right of right goal post and moving left
                newStepX = left - goalPosts[1]
            elif left > goalPosts[0] and self.stepX > left - goalPosts[0]:
                # right of left goal post and moving left
                newStepX = left - goalPosts[0]
            elif right < goalPosts[1] and self.stepX < right - goalPosts[1]:
                # left of right goal post and moving right
                newStepX = right - goalPosts[1]
            if newStepX != self.stepX:
                newStepX, newStepY = self.getNewStep1(newStepX)
                if top - newStepY < goalPosts[2]:
                    approaching = 'side', newStepX, newStepY
                elif newStepY > 0 and top - newStepY == goalPosts[2]:
                    approaching = 'bottom', newStepX, newStepY
            elif top > goalPosts[2] and self.stepY > top - goalPosts[2]:
                # below goal line and moving up
                newStepX, newStepY = self.getNewStep2(top - goalPosts[2])
                newLeft, newRight = left-newStepX, right-newStepX
                postRange = ([goalPosts[0]-goal.postWidth+1,
                              goalPosts[0]+goal.postWidth-1],
                             [goalPosts[1]-goal.postWidth+1,
                              goalPosts[1]+goal.postWidth-1])
                if (newRight>=postRange[0][0] and newRight<=postRange[0][1]) or \
                   (newLeft>=postRange[0][0] and newLeft<=postRange[0][1]) or \
                   (newRight>=postRange[1][0] and newRight<=postRange[1][1]) or \
                   (newLeft>=postRange[1][0] and newLeft<=postRange[1][1]):
                    approaching = 'bottom', newStepX, newStepY
        return approaching

    def apprPlayers(self, players):
        '''This function checks if the ball is about to hit a player.
        players is an array listing the players in the game.'''
        approaching = False,
        if sum(self.apprPlayer) == 0:
            for player in players:
                if player.touchedBall:   # this player just kicked the ball
                    continue   # skip the rest of the loop
                # the leftmost, rightmost, top, and bottom points on the ball
                leftP = (self.getExtremes()[0],
                         self.getExtremes()[2]+self.center[1])
                rightP = self.getExtremes()[1], leftP[1]
                topP = (self.getExtremes()[0]+self.center[0],
                        self.getExtremes()[2])
                bottomP = topP[0], self.getExtremes()[3]
                approachingPlayer = [False] * 4   # front, back, left, right
                apprPts = {}
                # player's body center position and body corners
                pCenterPos = player.getCenterPos()[2]
                pCorners = player.getCorners()
                # player's front, back, left, and right sides
                pSides = ([pCorners[0],pCorners[1]], [pCorners[2],pCorners[3]],
                          [pCorners[0],pCorners[2]], [pCorners[1],pCorners[3]])
                for p in (leftP, rightP, topP, bottomP):
                    newp = p[0]-self.stepX, p[1]-self.stepY
                    # points at which the line connecting p and newp
                    # intersects the player's sides
                    ints = []
                    for side in pSides:
                        ints += [line.getIntersect(p, newp, side[0], side[1])]
                    # check which side of the player the ball is approaching
                    for i in range(len(ints)):
                        if line.isBetween(ints[i], p, newp) and \
                           line.isBetween(ints[i], pSides[i][0], pSides[i][1]):
                            d1 = line.getParams(ints[i], pSides[i][0])[2]
                            d2 = line.getParams(ints[i], pSides[i][1])[2]
                            if min(d1, d2) > 1:
                                approachingPlayer[i] = True
                                apprPts[p] = ints[i]
                if 1 in approachingPlayer:
                    # find the point on the ball that will hit the player first
                    count = 0
                    for p in apprPts:
                        count += 1
                        if count == 1:
                            minDist = line.getParams(p, apprPts[p])[2]
                            closestp = p
                        else:
                            dist = line.getParams(p, apprPts[p])[2]
                            if dist < minDist:
                                minDist, closestp = dist, p
                    approaching = approachingPlayer.index(1)+1, minDist, player
                    break
        return approaching

    def bounceOff(self, bounceType):
        '''This function sets new parameters (moving angle, speed, and
        step size) for the movement of the ball when it bounces off
        either the screen boundary or the goal post.'''
        denom = 10
        if bounceType == 1:
            angleAdjust = abs(abs(self.getMovingAngle()) - 90) / denom
            baseNewAngle = -self.getMovingAngle()
        elif bounceType == 2:
            angleAdjust = abs(self.getMovingAngle()) / denom
            baseNewAngle = 180 - self.getMovingAngle()
        self.setMovingAngle(random.uniform(baseNewAngle-angleAdjust,
                                           baseNewAngle+angleAdjust))
        self.speed /= random.uniform(1.03, 1.05)   # decrement speed
        self.setStep1()

    def bounceOffPl(self, player, sideHit):
        '''This function sets new parameters (moving angle, speed, and
        step size) for the movement of the ball when it bounces off either
        a player's back (sideHit = 2) or a player's flank (sideHit = 3 for
        left or sideHit = 4 for right).'''
        pCenterPos = player.getCenterPos()[2]   # player's body center position
        pCorners = player.getCorners()   # player's body corners
        # player's back, left, and right sides
        pSides = ([pCorners[2],pCorners[3]], [pCorners[0],pCorners[2]],
                  [pCorners[1],pCorners[3]])
        # the leftmost, rightmost, top, and bottom points on the ball
        leftP = self.getExtremes()[0], self.getExtremes()[2]+self.center[1]
        rightP = self.getExtremes()[1], leftP[1]
        topP = self.getExtremes()[0]+self.center[0], self.getExtremes()[2]
        bottomP = topP[0], self.getExtremes()[3]
        # set new parameters (might not be the final values)
        bounceType = random.choice([1, 2])
        self.bounceOff(bounceType)
        speed = self.speed
        for p in (leftP, rightP, topP, bottomP):
            newp = p[0]-self.stepX, p[1]-self.stepY
            checkSide = line.checkSide(newp, pCenterPos, pSides[sideHit-2][0],
                                       pSides[sideHit-2][1])
            if checkSide == 1:
                # ball would be going inside the player's body
                self.bounceOff(3-bounceType)   # set new parameters again
                self.speed = speed   # reset
                break
       
    def move(self, goal, players):
        '''This function handles ball movements when the ball is kicked.
        players is an array listing the players in the game. The goalkeeper
        must be listed first.'''
        goalPosts = goal.getPosts()
        checkScrBounds = self.apprScrBounds()
        checkGoalPosts = self.apprGoalPosts(goal)
        checkPlayers = self.apprPlayers(players)
        if checkScrBounds[0] != False:   # ball approaching screen boundary
            self.setStep2(checkScrBounds[1], checkScrBounds[2])
            self.apprScrBound = checkScrBounds[0]
        elif checkGoalPosts[0] != False:   # ball approaching goal post
            self.setStep2(checkGoalPosts[1], checkGoalPosts[2])
            self.apprGoalPost = checkGoalPosts[0]
        elif checkPlayers[0] != False:   # ball approaching player
            self.speed = checkPlayers[1]
            self.setStep1()
            for i in range(len(players)):
                if players[i] == checkPlayers[-1]:
                    self.apprPlayer[i] = checkPlayers[0]
        elif self.apprScrBound == 'vertb' or self.apprGoalPost == 'side':
            # ball hit either the vertical boundary or the side of the goal post
            self.bounceOff(1)
            self.apprScrBound, self.apprGoalPost = False, False   # reset
            for player in players:
                player.touchedBall = False   # reset
        elif self.apprScrBound == 'horzb' or self.apprGoalPost == 'bottom':
            # ball hit either the horizontal boundary or
            # the bottom of the goal post
            self.bounceOff(2)
            self.apprScrBound, self.apprGoalPost = False, False   # reset
            for player in players:
                player.touchedBall = False   # reset
        elif sum(self.apprPlayer) > 0:
            for i in range(len(self.apprPlayer)):
                if self.apprPlayer[i] != 0:
                    if self.apprPlayer[i] == 1:   # ball hits player's front
                        self.setStep2(0, 0)
                        self.moving = False
                        if i == 0:
                            self.gkCaught = True
                    else:   # ball hits player's back or flank
                        self.bounceOffPl(players[i], self.apprPlayer[i])
                    break
            self.apprPlayer = [False] * len(players)   # reset
            for player in players:
                player.touchedBall = False   # reset
        elif self.getExtremes()[3] <= goalPosts[2] and \
             self.getExtremes()[0] >= goalPosts[0] and \
             self.getExtremes()[1] <= goalPosts[1]:
            self.inGoal = True
        # new coordinates of the ball center
        self.setCenterPos(self.getCenterPos()[0]-self.stepX,
                          self.getCenterPos()[1]-self.stepY)
        
    def reset(self):
        '''This function puts the ball at its original position after 
        the player scores.'''
        self.setCenterPos(self.getStartPos()[0][0]+self.center[0],
                          self.getStartPos()[0][1]+self.center[1])
        # update ball position and the display to show change
        self.update()
        self.inGoal = False

    def update(self):
        '''This function updates the position of the ball and updates the
        display to show movements.'''
        move.update(self.screen, self.allThings, self.allPos,
                    (self.ball,self.ball), (self.getCenterPos(),))
        self.updateDisplay()
