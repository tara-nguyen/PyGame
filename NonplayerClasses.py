'''The following classes are defined: Game, Background, Goal, and Ball.
For neatness, the Player class, which is a child class of Game, is defined in a
different module named PlayerClasses.
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
    '''This class is the parent class of Background, Goal, Player, and Ball.
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
        '''This function updates the display and update the clock.'''
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
            # change the width but not the height
            newHeight = image.get_rect().height
        if newWidth == None and newHeight != None:
            # change the height but not the width
            newWidth = image.get_rect().width
        if newWidth != None or newHeight != None:
            # change both the height and the width
            image = pygame.transform.scale(image, (newWidth, newHeight))
        return image

    def processMoveKeys(self, pressedKeys):
        '''This function processes pressed keys that will initiate
        player movements.'''
        moveType, direction = None, None
        if pressedKeys[pygame.K_LEFT]:
            if pressedKeys[pygame.K_RSHIFT]:
                # right shift key pressed at the same time
                moveType = 'circle'
            else:
                moveType = 'straight'
            direction = 'left'
        if pressedKeys[pygame.K_RIGHT]:
            if pressedKeys[pygame.K_RSHIFT]:
                # right shift key pressed at the same time
                moveType = 'circle'
            else:
                moveType = 'straight'
            direction = 'right'
        if pressedKeys[pygame.K_UP]:
            moveType = 'straight'
            if pressedKeys[pygame.K_LEFT]:
                # left arrow key pressed at the same time
                direction = 'up left'
            elif pressedKeys[pygame.K_RIGHT]:
                # right arrow key pressed at the same time
                direction = 'up right'
            else:
                direction = 'up'
        if pressedKeys[pygame.K_DOWN]:
            moveType = 'straight'
            if pressedKeys[pygame.K_LEFT]:
                # left arrow key pressed at the same time
                direction = 'down left'
            elif pressedKeys[pygame.K_RIGHT]:
                # right arrow key pressed at the same time
                direction = 'down right'
            else:
                direction = 'down'
        if pressedKeys[pygame.K_SPACE]:
            moveType = 'to ball'
        return moveType, direction
        
    def processMovements(self, ballStep, ball, goal, players):
        '''This function processes the movements of the ball and of the 
        goalkeeper while the ball is moving.
        players is an array listing the players in the game. The goalkeeper
        must be listed first.'''
        # angle (measured in degrees) of the body with respect to the
        # y-axis pointing downward from the ball
        for player in players:
            if player.touchedBall:
                bodyAngle = player.getBodyAngle(ball)
        ball.apprScrBound, ball.apprGoalPost, ball.inGoal = [False] * 3
        ball.apprPlayer = []
        # angle (measured in degrees) at which the ball will move, with
        # respect to the y-axis pointing up from the current ball center
        ball.setMovingAngle(random.uniform(bodyAngle-.5, bodyAngle+.5))
        ball.setFirstStep(ballStep)
        ball.moving = True
        while ball.moving and round(ballStep) > 0:
            players[0].move(goal)   # move goalkeeper between goal posts
            players[0].updatePlayer()
            stepX, stepY = ball.getStep()   # step size before adjustment
            ball.move(goal, players)
            ball.update()
            if ball.apprScrBound != False or ball.apprGoalPost != False or \
               (ball.apprPlayer != [] and (not ball.gkCaught)):
                ball.setStep(stepX, stepY)   # reset
            ball.decrementStep()
            ballStep = math.sqrt(ball.stepX**2 + ball.stepY**2)
        if ball.inGoal:
            ball.reset()   # return to its original position
    
class Background(Game):
    '''This class is a child class of Game and has three methods: __init__, 
    load, and blit.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Background.<method name>.__doc__'''
    def __init__(self, screenSize):
        '''This function initializes the class and sets its core attributes.'''
        Game.__init__(self, screenSize)   # initialize the parent class
        self.grass = None   # contain nothing
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
        self.postWidth = 11
        leftPost = self.lPos[0] + self.postWidth / 2
        rightPost = self.rPos[0] + self.sideWidth - self.postWidth / 2
        return leftPost, rightPost, self.height

def getTrig(angle):
    '''This function returns the sine, cosine, and tangent of an angle.'''
    sin = math.sin(angle * math.pi/180)
    cos = math.cos(angle * math.pi/180)
    if cos != 0:
        tan = sin/cos
    else:
        tan = None
    return sin, cos, tan
    
class Ball(Game):
    '''This class is a child class of Game and has the following methods:
    __init__, load, blit, getStartPos, setCenterPos, getCenterPos, 
    setMovingAngle, getMovingAngle, setFirstStep, setStep, getStep,
    decrementStep, getExtremes, approachScrBounds, approachGoalPosts,
    approachPlayer, bounceBack, move, reset, and update.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Ball.<method name>.__doc__'''
    def __init__(self, screenSize):
        '''This function initializes the class and sets its core attributes.'''
        Game.__init__(self, screenSize)   # initialize the parent class
        self.ball = None   # contain nothing
        self.diameter = 30
        # where the image will be drawn
        self.startPos = (self.screenWidth-self.diameter)/2,self.screenHeight-200
##        self.startPos = (self.screenWidth-self.diameter)/2,self.screenHeight-100
        self.gkCaught = False

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

    def setFirstStep(self, stepDiag):
        '''This function sets the size of the first step the ball will make.'''
        self.stepX = stepDiag * getTrig(self.getMovingAngle())[0]
        self.stepY = stepDiag * getTrig(self.getMovingAngle())[1]

    def setStep(self, stepX, stepY):
        '''This function sets the step size for the ball's movements.'''
        self.stepX = stepX
        self.stepY = stepY

    def getStep(self):
        '''This function returns the step size for the ball's movements.'''
        return self.stepX, self.stepY

    def decrementStep(self):
        '''This function decrements the step size to make the ball move slower.'''
        factor = random.uniform(1.03, 1.05)   # a random real number
        self.setStep(self.stepX/factor, self.stepY/factor)

    def getExtremes(self):
        '''This function returns the x-coordinates of the leftmost and
        rightmost points on the ball, and the y-coordinates of the top
        and bottom points on the ball.'''
        left = self.getCenterPos()[0] - self.center[0]
        right = left + self.diameter
        top = self.getCenterPos()[1] - self.center[1]
        bottom = top + self.diameter
        return left, right, top, bottom

    def approachScrBounds(self):
        '''This function checks if the ball is about to hit the 
        screen boundaries.'''
        if not self.apprScrBound:
            # the leftmost, rightmost, top, and bottom points on the ball
            left, right, top, bottom = self.getExtremes()
            if self.stepX > left:
                newStepX = left
                newStepY = newStepX / getTrig(self.getMovingAngle())[2]
                return 'vertb', newStepX, newStepY
            elif self.stepX < right - self.screenWidth:
                newStepX = right - self.screenWidth
                newStepY = newStepX / getTrig(self.getMovingAngle())[2]
                return 'vertb', newStepX, newStepY
            elif self.stepY > top:
                newStepY = top
                newStepX = newStepY * getTrig(self.getMovingAngle())[2]
                return 'horzb', newStepX, newStepY
            elif self.stepY < bottom - self.screenHeight:
                newStepY = bottom - self.screenHeight
                newStepX = newStepY * getTrig(self.getMovingAngle())[2]
                return 'horzb', newStepX, newStepY
            else:
                return False,
        else:
            return False,

    def approachGoalPosts(self, goal):
        '''This function checks if the ball is about to hit the goal posts.'''
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
                newStepY = newStepX / getTrig(self.getMovingAngle())[2]
                if top - newStepY < goalPosts[2]:
                    return 'side', newStepX, newStepY
                else:
                    return False,
            elif newStepY != self.stepY:
                newStepX = newStepY * getTrig(self.getMovingAngle())[2]
##                NEED MORE WORK HERE
                if (left - newStepX <= goalPosts[0] and \
                    right - newStepX >= goalPosts[0]) or \
                    (left - newStepX <= goalPosts[1] and \
                     right - newStepX >= goalPosts[1]):
                    return 'bottom', newStepX, newStepY
                else:
                    return False,
            else:
                return False,
        else:
            return False,
       
    def approachPlayer(self, players):
        '''This function checks if the ball is about to hit a player.
        players is an array listing the players in the game.'''
##        NEED MORE WORK HERE
        print('entering approachPlayer()')
        if self.apprPlayer == []:
            # the leftmost, rightmost, top, and bottom points on the ball
            leftP = self.getExtremes()[0], self.getExtremes()[2]+self.center[1]
            rightP = self.getExtremes()[1], leftP[1]
            topP = self.getExtremes()[0]+self.center[0], self.getExtremes()[2]
            bottomP = topP[0], self.getExtremes()[3]
            approachingPlayer = [False] * 4   # front, back, left, right
            apprPts = {}
            for player in players:
                pCorners = player.getCorners()   # player's body corners
                # check if, with the current step size, the ball would
                # hit the player 
                for p in (leftP, rightP, topP, bottomP):
                    newp = p[0]-self.stepX, p[1]-self.stepY
                    # points at which the line connecting p and newp
                    # intersects the player's sides
                    ints = [line.getIntersect(p, newp,
                                              pCorners[0], pCorners[1])[:2]]
                    ints += [line.getIntersect(p, newp,
                                               pCorners[2], pCorners[3])[:2]]
                    ints += [line.getIntersect(p, newp,
                                               pCorners[0], pCorners[2])[:2]]
                    ints += [line.getIntersect(p, newp,
                                               pCorners[1], pCorners[3])[:2]]
                    # check which side of the player the ball is approaching
                    if line.isBetween(ints[0], p, newp) and \
                       line.isBetween(ints[0], pCorners[0], pCorners[1]):
                        approachingPlayer[0] = True
                        intsPoint = ints[0]
                        intsAngle =line.getIntersect(
                            p, newp, pCorners[0], pCorners[1])[2]
                    elif line.isBetween(ints[1], p, newp) and \
                         line.isBetween(ints[1], pCorners[2], pCorners[3]):
                        approachingPlayer[1] = True
                        intsPoint = ints[1]
                        intsAngle = line.getIntersect(
                            p, newp, pCorners[2], pCorners[3])[2]
                    elif line.isBetween(ints[2], p, newp) and \
                         line.isBetween(ints[2], pCorners[0], pCorners[2]):
                        approachingPlayer[2] = True
                        intsPoint = ints[2]
                        intsAngle = line.getIntersect(
                            p, newp, pCorners[0], pCorners[2])[2]
                    elif line.isBetween(ints[3], p, newp) and \
                         line.isBetween(ints[3], pCorners[1], pCorners[3]):
                        approachingPlayer[3] = True
                        intsPoint = ints[3]
                        intsAngle = line.getIntersect(
                            p, newp, pCorners[1], pCorners[3])[2]
                    if 1 in approachingPlayer:
                        apprPts[p] = intsPoint, intsAngle
                if 1 in approachingPlayer:
                    # find the point on the ball that will
                    # reach the player first
                    count = 0
                    for p in apprPts.keys():
                        count += 1
                        if count == 1:
                            minDist = line.getParams(p, apprPts[p][0])[2]
                            closestp = p
                        else:
                            dist = line.getParams(p, apprPts[p][0])[2]
                            if dist < minDist:
                                minDist, closestp = dist, p
                    newStepX, newStepY = \
                              line.getParams(closestp, apprPts[closestp][0])[:2]
                    return (approachingPlayer.index(1)+1, newStepX, newStepY,
                            apprPts[p][1], player)
            if 1 not in approachingPlayer:
                return False,
        else:
            return False,        

    def bounceBack(self, switch):
        '''This function modifies the step size and angle to make the ball
        bounce back from either the screen boundaries or the goal posts.
        switch denotes whether the direction in which the ball is moving will 
        be flipped laterally ('x') or vertically ('y').'''
        factor = random.uniform(1.03, 1.05)   # a random real number
        if switch == 'x':
            self.setStep(self.getStep()[0]/-factor, self.getStep()[1]/factor)
            self.setMovingAngle(-self.getMovingAngle())
        elif switch == 'y':
            self.setStep(self.getStep()[0]/factor, self.getStep()[1]/-factor)
            if self.getMovingAngle() < 0:
                self.setMovingAngle(-180 - self.getMovingAngle())
            else:
                self.setMovingAngle(180 - self.getMovingAngle())

    def move(self, goal, players):
        '''This function handles ball movements when the ball is kicked.
        players is an array listing the players in the game. The goalkeeper
        must be listed first.'''
        print('MOVE')
        print('step size before adjust:',self.getStep())
        goalPosts = goal.getPosts()
        checkScrBounds = self.approachScrBounds()
        checkGoalPosts = self.approachGoalPosts(goal)
        checkPlayer = self.approachPlayer(players)
        if checkScrBounds[0] != False:   # ball approaching screen boundary
            print('*** SCENARIO 1: approaching screen boundary')
            self.setStep(checkScrBounds[1], checkScrBounds[2])
            self.apprScrBound = checkScrBounds[0]
        elif checkGoalPosts[0] != False:   # ball approaching goal post
            print('*** SCENARIO 2: approaching goal post')
            print('checkGoalPosts:',checkGoalPosts)
            self.setStep(checkGoalPosts[1], checkGoalPosts[2])
            self.apprGoalPost = checkGoalPosts[0]
        elif checkPlayer[0] != False:   # ball approaching player
            print('*** SCENARIO 3: approaching player')
            print('checkPlayer:',checkPlayer[:-1])
            self.setStep(checkPlayer[1], checkPlayer[2])
            for i in range(len(players)):
                if players[i] == checkPlayer[-1]:
                    self.apprPlayer.append(checkPlayer[0])
                else:
                    self.apprPlayer.append(0)
            print('self.apprPlayer:',self.apprPlayer)
        elif self.apprScrBound == 'vertb' or self.apprGoalPost == 'side':
            print('*** SCENARIO 4: hit vertb or hit goal post from side')
            self.bounceBack('x')
            self.apprScrBound, self.apprGoalPost = False, False   # reset
        elif self.apprScrBound == 'horzb' or self.apprGoalPost == 'bottom':
            print('*** SCENARIO 5: hit horzb or hit goal post from bottom')
            self.bounceBack('y')
            self.apprScrBound, self.apprGoalPost = False, False   # reset
        elif len(self.apprPlayer) > 0:
            print('*** SCENARIO 6: hit player')
            for i in range(len(self.apprPlayer)):
                if self.apprPlayer[i] == 1:   # ball hits player's front
                    self.setStep(0, 0)
                    self.moving = False
                    if i == 0:   # ball caught by goalkeeper
                        self.gkCaught = True
                    self.apprPlayer = []   # reset
                    break
##                else:
##                    ...
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
