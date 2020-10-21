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
        file = 'ImagesInPyGame/' + imageName + '.png'
        return file

    def loadImage(self, imageName, newWidth=None, newHeight=None):
        '''This function loads an image into PyGame and resizes it if required.'''
        image = pygame.image.load(self.getFile(imageName)).convert_alpha()
        if newWidth != None and newHeight == None:
            newHeight = image.get_rect().height   # height not changed
        if newWidth == None and newHeight != None:
            newWidth = image.get_rect().width   # width not changed
        if newWidth != None or newHeight != None:
            image = pygame.transform.scale(image, (newWidth, newHeight))
        return image

    def processMoveKeys(self, pressedKeys):
        '''This function processes pressed keys that will initiate
        player movements.'''
        moveType, direction = None, None
        directions = 'left', 'right', 'up', 'down'
        keys = (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN,
                pygame.K_SPACE, pygame.K_RSHIFT)
        pressed = []
        for key in keys:
            pressed.append(pressedKeys[key])
        if sum(pressed) == 1:   # only one key pressed
            if pressed.index(1) < 4:   # LEFT, RIGHT, UP, or DOWN key
                moveType = 'straight'
                direction = directions[pressed.index(1)]
            elif pressed.index(1) == 4:   # SPACE key
                moveType = 'to ball'
        elif sum(pressed) == 2:   # two keys pressed at the same time
            if pressed.index(1) < 2:   # LEFT or RIGHT key
                if pressed.index(1,2) < 4:   # UP or DOWN key
                    moveType = 'straight'
                    direction = directions[pressed.index(1,2)] + \
                                directions[pressed.index(1)]
                elif pressed[5]:   # RSFHIT key
                    moveType = 'circle'
                    direction = directions[pressed.index(1)]
        return moveType, direction
        
    def processMovements(self, ball, goal, players):
        '''This function processes the movements of the ball and
        of the goalkeeper while the ball is moving.
        players is an array listing the players in the game. The
        goalkeeper must be listed first.'''
        for player in players:
            if player.touchedBall:
                bodyAngle = player.getBodyAngle(ball)
                break
        ball.apprScrBound, ball.apprGoalPost, ball.inGoal = [False] * 3
        ball.apprPlayer = [False] * len(players)
        # move ball
        ball.setMovingAngle(random.uniform(bodyAngle-.5, bodyAngle+.5))
        speed = ball.initSpeed
        ball.moving = True
        while ball.moving and round(speed) > 0:
            players[0].moveAcross(goal)
            players[0].updateAll()
            ball.setStep1(speed)
            stepX, stepY = ball.getStep()   # step size before adjustment
            ball.move(speed, goal, players)
            player.touchedBall = False   # reset
            if not ball.moving:
                break
            ball.update()
            if ball.apprScrBound != False or ball.apprGoalPost != False or \
               sum(ball.apprPlayer) > 0:
                ball.setStep2(stepX, stepY)   # reset
            speed /= random.uniform(1.03, 1.05)   # decrement speed
        if ball.inGoal:
            ball.reset()   # return to its original position
        print('***********************************************')
        print('********** END OF processMovements() **********')
        print('***********************************************\n\n')
        
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
        
    def crop(self, image, newWidth, newHeight, shiftLeft=0):
        '''This function crops an image and returns the new surface on which
        the final image will be pasted.'''
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
        self.left = self.crop(self.left, self.sideWidth, self.height,
                              shiftLeft=11)
        self.middle = self.crop(self.middle, self.middleWidth, self.height,
                                shiftLeft=(scale[0]-self.middleWidth)/2)
        self.right = self.crop(self.right, self.sideWidth, self.height,
                               shiftLeft=scale[0]-self.sideWidth-11)
        
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
    sin = math.sin(angle * math.pi/180)
    cos = math.cos(angle * math.pi/180)
    tan = math.tan(angle * math.pi/180)
    return sin, cos, tan
    
class Ball(Game):
    '''This class is a child class of Game and has the following methods:
    __init__, load, blit, getStartPos, setCenterPos, getCenterPos,
    setMovingAngle, getMovingAngle, setStep1, setStep2, getStep,
    getNewStep1, getNewStep2, getExtremes, apprScrBounds, apprGoalPosts,
    apprPlayers, bounceOff, move, reset, and update.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Ball.<method name>.__doc__'''
    def __init__(self, screenSize):
        '''This function initializes the class and sets its core attributes.'''
        Game.__init__(self, screenSize)   # initialize the parent class
        self.ball, self.diameter = None, 30
##        self.startPos = (self.screenWidth-self.diameter)/2,self.screenHeight-200
        self.startPos = (self.screenWidth-self.diameter)/2,self.screenHeight-350
        self.gkCaught = False
        self.initSpeed = random.uniform(18, 22)

    def load(self, imageName):
        '''This function loads the ball image into PyGame.'''
        self.ball = self.loadImage(imageName, self.diameter, self.diameter)
        
    def blit(self):
        '''This function draws the ball onto the screen.'''
        self.screen.blit(self.ball, self.startPos)
        self.center = self.ball.get_rect().center   # center of the ball
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
        '''This function sets the angle (measured in degrees) at which the ball
        will move, with respect to the negative y-axis pointing up from the
        current ball center.'''
        self.movingAngle = angle

    def getMovingAngle(self):
        '''This function returns the angle (measured in degrees) at which the
        ball is currently moving, with respect to the negative y-axis pointing 
        up from the current ball center.'''
        return self.movingAngle

    def setStep1(self, speed):
        '''This function sets the step sizes based on the total
        distance the ball will travel.'''
        self.stepX = speed * getTrig(self.getMovingAngle())[0]
        self.stepY = speed * getTrig(self.getMovingAngle())[1]

    def setStep2(self, stepX, stepY):
        '''This function sets the step sizes based on given values for
        the lateral and the vertical steps (stepX and stepY).'''
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
##        ########## NEED MORE WORK HERE ##########
        approaching = False,
        if not self.apprGoalPost:
            goalPosts = goal.getPosts()
            # the leftmost, rightmost, and top points on the ball
            left, right, top = self.getExtremes()[:3]
            newStepX, newStepY = self.getStep()
            if right < goalPosts[0] and self.stepX < right - goalPosts[0]:
                # left of left goal post and moving right
                print('left of left goal post and moving right')
                newStepX = right - goalPosts[0]
            elif left > goalPosts[1] and self.stepX > left - goalPosts[1]:
                # right of right goal post and moving left
                print('right of right goal post and moving left')
                newStepX = left - goalPosts[1]
            elif left > goalPosts[0] and self.stepX > left - goalPosts[0]:
                # right of left goal post and moving left
                print('right of left goal post and moving left')
                newStepX = left - goalPosts[0]
            elif right < goalPosts[1] and self.stepX < right - goalPosts[1]:
                # left of right goal post and moving right
                print('left of right goal post and moving right')
                newStepX = right - goalPosts[1]
            elif top > goalPosts[2] and self.stepY > top - goalPosts[2]:
                # below goal line and moving up
                print('below goal line and moving up')
                newStepY = top - goalPosts[2]
            if newStepX != self.stepX:
                newStepX, newStepY = self.getNewStep1(newStepX)
                if top - newStepY < goalPosts[2]:
                    approaching = 'side', newStepX, newStepY
            elif newStepY != self.stepY:
                newStepX, newStepY = self.getNewStep2(newStepY)
                if (left - newStepX <= goalPosts[0] and \
                    right - newStepX >= goalPosts[0]) or \
                    (left - newStepX <= goalPosts[1] and \
                     right - newStepX >= goalPosts[1]):
                    approaching = 'bottom', newStepX, newStepY
        return approaching
       
    def apprPlayers(self, players):
        '''This function checks if the ball is about to hit a player.
        players is an array listing the players in the game.'''
##        ########## NEED MORE WORK HERE ##########
        approaching = False,
        if sum(self.apprPlayer) == 0:
            print('STARTING apprPlayers()')
            for player in players:
                if player.touchedBall:   # this player just kicked the ball
                    continue
                print('--- Checking',player,'---')
                # the leftmost, rightmost, top, and bottom points on the ball
                leftP = (self.getExtremes()[0],
                         self.getExtremes()[2]+self.center[1])
                rightP = self.getExtremes()[1], leftP[1]
                topP = (self.getExtremes()[0]+self.center[0],
                        self.getExtremes()[2])
                bottomP = topP[0], self.getExtremes()[3]
                currCenterPos = self.getCenterPos()
                approachingPlayer = [False] * 4   # front, back, left, right
                apprPts = {}
                pCorners = player.getCorners()   # player's body corners
##                print('player corners:')
##                for corner in pCorners:
##                    print('\t',corner)
                # player's front, back, left, and right sides
                pSides = ([pCorners[0],pCorners[1]], [pCorners[2],pCorners[3]],
                          [pCorners[0],pCorners[2]], [pCorners[1],pCorners[3]])
                for p in (leftP, rightP, topP, bottomP):
##                    print('ball pt:',p)
                    newp = p[0]-self.stepX, p[1]-self.stepY
                    # points at which the line connecting p and newp
                    # intersects the player's sides
                    ints = []
                    for side in pSides:
                        ints += [line.getIntersect(p, newp, side[0], side[1])]
                    # check which side of the player the ball is approaching
##                    print('ints:')
                    for i in range(len(ints)):
##                        print('\tpoint'+str(i+1)+':',ints[i])
                        if line.isBetween(ints[i], p, newp) and \
                           line.isBetween(ints[i], pSides[i][0], pSides[i][1]):
                            print('ball point',p,'approaching side',i+1)
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
                else:
                    print('ball not approaching')
        print('END OF apprPlayers()')
        return approaching

    def bounceOff(self, x, y, speed, adjust=0):
        '''This function modifies the step size and angle to make the ball
        bounce off the screen boundaries, the goal posts, or a player.
        x and y denote whether the sign of the lateral step size and/or
        that of the vertical step size will be flipped.
        adjust is the angle (between -90 and 90 degrees) of the surface/line
        off which the ball bounces, with respect to the x-axis. The default
        line is any line parallel to the x-axis.'''
        factor = random.uniform(1.03, 1.05)   # a random real number
        if x == 1 and y == 0:
            self.setMovingAngle(-self.getMovingAngle())
        elif y == 1:
            self.setMovingAngle(180 - self.getMovingAngle() + adjust)
        self.setStep1(speed)
            
    def move(self, speed, goal, players):
        '''This function handles ball movements when the ball is kicked.
        players is an array listing the players in the game. The goalkeeper
        must be listed first.'''
        print('**************************')
        print('********** MOVE **********')
        goalPosts = goal.getPosts()
        checkScrBounds = self.apprScrBounds()
        checkGoalPosts = self.apprGoalPosts(goal)
        checkPlayers = self.apprPlayers(players)
        print('step size before adjust:',self.getStep())
        if checkScrBounds[0] != False:   # ball approaching screen boundary
            print('*** SCENARIO 1: approaching screen boundary ***')
            self.setStep2(checkScrBounds[1], checkScrBounds[2])
            self.apprScrBound = checkScrBounds[0]
        elif checkGoalPosts[0] != False:   # ball approaching goal post
            print('*** SCENARIO 2: approaching goal post ***')
            print('checkGoalPosts:',checkGoalPosts)
            self.setStep2(checkGoalPosts[1], checkGoalPosts[2])
            self.apprGoalPost = checkGoalPosts[0]
        elif checkPlayers[0] != False:   # ball approaching player
            print('*** SCENARIO 3: approaching player ***')
            print('checkPlayers:',checkPlayers[:-1])
            self.setStep1(checkPlayers[1])
            for i in range(len(players)):
                if players[i] == checkPlayers[-1]:
                    self.apprPlayer[i] = checkPlayers[0]
            print('self.apprPlayer:',self.apprPlayer)
        elif self.apprScrBound == 'vertb' or self.apprGoalPost == 'side':
            print('*** SCENARIO 4: hit vertb or hit goal post from side ***')
            self.bounceOff(1, 0, speed)
            self.apprScrBound, self.apprGoalPost = False, False   # reset
        elif self.apprScrBound == 'horzb' or self.apprGoalPost == 'bottom':
            print('*** SCENARIO 5: hit horzb or hit goal post from bottom ***')
            self.bounceOff(0, 1, speed)
            self.apprScrBound, self.apprGoalPost = False, False   # reset
        elif sum(self.apprPlayer) > 0:
            print('*** SCENARIO 6: hit player ***')
            print('self.apprPlayer:',self.apprPlayer)
            for i in range(len(self.apprPlayer)):
                if self.apprPlayer[i] != 0:
                    if self.apprPlayer[i] == 1:   # ball hits player's front
                        self.setStep2(0, 0)
                        self.moving = False
                        if i == 0:   # ball hits goalkeeper's front
                            self.gkCaught = True
                    else:   # ball hits player's back or flank
                        self.bounceOff(0, 1, speed)
                    break
            self.apprPlayer = [False] * len(players)   # reset
        elif self.getExtremes()[3] <= goalPosts[2] and \
             self.getExtremes()[0] >= goalPosts[0] and \
             self.getExtremes()[1] <= goalPosts[1]:
            print('*** SCENARIO 7: in goal')
            self.inGoal = True
        # new coordinates of the ball center
        self.setCenterPos(self.getCenterPos()[0]-self.stepX,
                          self.getCenterPos()[1]-self.stepY)
        print('step size after adjust:',self.getStep())
        print('gkCaught:',self.gkCaught)
        
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
