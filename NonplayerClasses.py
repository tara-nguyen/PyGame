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
        # screen size
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
            # resize image
            image = pygame.transform.scale(image, (newWidth, newHeight))
        return image

    def processMoveKeys(self, pressedKeys):
        '''This function processes pressed keys that will initiate
        player movements.'''
        moveType, direction = None, None
        if pressedKeys[pygame.K_LEFT]:   # left arrow key has been pressed
            if pressedKeys[pygame.K_RSHIFT]:
                # right shift key pressed at the same time
                moveType = 'circle'
            else:
                moveType = 'straight'
            direction = 'left'
        if pressedKeys[pygame.K_RIGHT]:  # right arrow key has been pressed
            if pressedKeys[pygame.K_RSHIFT]:
                # right shift key pressed at the same time
                moveType = 'circle'
            else:
                moveType = 'straight'
            direction = 'right'
        if pressedKeys[pygame.K_UP]:   # up arrow key has been pressed
            moveType = 'straight'
            if pressedKeys[pygame.K_LEFT]:
                # left arrow key pressed at the same time
                direction = 'up left'
            elif pressedKeys[pygame.K_RIGHT]:
                # right arrow key pressed at the same time
                direction = 'up right'
            else:
                direction = 'up'
        if pressedKeys[pygame.K_DOWN]:   # down arrow key has been pressed
            moveType = 'straight'
            if pressedKeys[pygame.K_LEFT]:
                # left arrow key pressed at the same time
                direction = 'down left'
            elif pressedKeys[pygame.K_RIGHT]:
                # right arrow key pressed at the same time
                direction = 'down right'
            else:
                direction = 'down'
        if pressedKeys[pygame.K_SPACE]:   # spacebar has been pressed
            moveType = 'to ball'
        return moveType, direction
        
    def processMovements(self, stepSize, minDist, ball, goal, goalkeeper,
                         striker):
        '''This function processes the movements of the ball and of the 
        goalkeeper while the ball is moving.
        minDist is the nearest distance to the player that the ball can get.'''
        # angle (measured in degrees) of the body with respect to the
        # y-axis pointing downward
        if goalkeeper.touchedBall:
            bodyAngle = goalkeeper.getBodyAngle(ball)
        elif striker.touchedBall:
            bodyAngle = striker.getBodyAngle(ball)
        # angle (measured in degrees) at which the ball will move, with
        # respect to the y-axis pointing up from the current ball center
        ball.setMovingAngle(random.uniform(bodyAngle-.5, bodyAngle+.5))
        ball.setFirstStep(stepSize)   # initial step size
        ball.moving = True
        while ball.moving and round(stepSize) > 0:
            goalkeeper.move(goal)   # move goalkeeper between goal posts
            goalkeeper.updatePlayer()
            if ball.checkGoal(goal.getPosts()):   # ball in goal
                ball.inGoal = True
            # move ball
            ball.move(stepSize, goal.getPosts(), (goalkeeper,striker), minDist)
            # new step size
            stepSize = math.sqrt(ball.stepX**2 + ball.stepY**2)   
    
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
        self.grass = Game.loadImage(self, imageName,
                                    self.screenWidth, self.screenHeight)
        
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
        self.left = None
        self.middle = None
        self.right = None
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
        self.mPos = self.screenCenter[0]-self.middle.get_rect().center, 0
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
        postWidthHalf = 11/2
        leftPost = self.lPos[0] + postWidthHalf
        rightPost = self.rPos[0] + self.sideWidth - postWidthHalf
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
    decrementStep, getExtremes, setFinalStep1, setFinalStepSB, setFinalStepGP,
    setFinalStep2, hitGoalPosts, bounceBack, checkBouncing, hitPlayer,
    checkGoal, move, resetBall, and updateBall.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Ball.<method name>.__doc__'''
    def __init__(self, screenSize):
        '''This function initializes the class and sets its core attributes.'''
        Game.__init__(self, screenSize)   # initialize the parent class
        self.ball = None   # contain nothing
        self.diameter = 36
        # where the image will be drawn
        self.startPos = ((self.screenWidth-self.diameter)/2,
                         self.screenHeight-200)
        self.moving, self.hittingPlayer, self.gkCaught, self.inGoal = [False]*4

    def load(self, imageName):
        '''This function loads the ball image into PyGame.'''
        self.ball = Game.loadImage(self, imageName, self.diameter, self.diameter)
        
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

    def setFirstStep(self, stepSize):
        '''This function sets the size of the first step that ball will make.'''
        self.stepX = stepSize * getTrig(self.getMovingAngle())[0]
        self.stepY = stepSize * getTrig(self.getMovingAngle())[1]

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
        '''This function returns the coordinates of the leftmost, rightmost, top, 
        and bottom points of the ball'''
        left = self.getCenterPos()[0] - self.center[0]
        right = left + self.diameter
        top = self.getCenterPos()[1] - self.center[1]
        bottom = top + self.diameter
        return left, right, top, bottom

    def setFinalStep1(self, direction, distance):
        '''This function sets the size of the final step before the ball hits
        either the screen boundaries or the goal posts.
        distance is the distance from the ball to the boundary/goal post.
        direction denotes whether the x- or the y-step size will be
        set to distance.'''
        if direction == 'x':
            self.setStep(distance, distance/getTrig(self.getMovingAngle())[2])
        elif direction == 'y':
            self.setStep(distance*getTrig(self.getMovingAngle())[2], distance)

    def setFinalStepSB(self):
        '''This function checks if the ball is about to hit the screen
        boundaries, and sets the step size accordingly.'''
        # the leftmost, rightmost, top, and bottom points on the ball
        left, right, top, bottom = self.getExtremes()
        # set final step
        if self.stepX > left:
            self.setFinalStep1('x', left)
        if self.stepX < right - self.screenWidth:
            self.setFinalStep1('x', right-self.screenWidth)
        if self.stepY > top:
            self.setFinalStep1('y', top)
        if self.stepY < bottom - self.screenHeight:
            self.setFinalStep1('y', bottom-self.screenHeight)

    def setFinalStepGP(self, goalPosts):
        '''This function checks if the ball is about to hit the goal posts,
        and sets the step size accordingly.
        goalPosts denotes the x-coordinates and size of the goal posts.'''
        # the leftmost, rightmost, and top points on the ball
        left, right, top = self.getExtremes()[:3]
        oldStepX, oldStepY = self.getStep()   # step size before adjusting
        if self.stepX != 0:   # there is movement in the x-direction
            if top < goalPosts[-1] or (top >= goalPosts[-1] and self.stepY > 0):
                if right < goalPosts[0] and self.stepX < right - goalPosts[0]:
                    # left of left goal post and moving right
                    self.setFinalStep1('x', right-goalPosts[0])
                elif left > goalPosts[1] and self.stepX > left - goalPosts[1]:
                    # right of right goal post and moving left
                    self.setFinalStep1('x', left-goalPosts[1])
                elif left > goalPosts[0] + goalPosts[2] and \
                   self.stepX > left - (goalPosts[0] + goalPosts[2]):
                    # right of left goal post and moving left
                    self.setFinalStep1('x', left-(goalPosts[0]+goalPosts[2]))
                elif right < goalPosts[1] - goalPosts[2] and \
                   self.stepX < right - (goalPosts[1] - goalPosts[2]):
                    # left of right goal post and moving right
                    self.setFinalStep1('x', right-(goalPosts[1]-goalPosts[2]))
                # check if, with the new step size, the ball would hit the
                # goal posts; if not, reset the step size
                if top > goalPosts[-1] and self.stepY < top - goalPosts[-1]:
                    self.setStep(oldStepX, oldStepY)
        
    def setFinalStep2(self, goalPosts):
        '''This function checks if the ball is about to hit either the screen
        boundaries or the goal posts, and sets the step size accordingly.
        goalPosts denotes the x-coordinates and size of the goal posts.'''
        self.setFinalStepSB()
        self.setFinalStepGP(goalPosts)

    def hitGoalPosts(self, goalPosts):
        '''This function checks if the ball has hit the goal posts.
        goalPosts denotes the x-coordinates and size of the goal posts.'''
        # the leftmost, rightmost, and top points on the ball
        left, right, top = self.getExtremes()[:3]
        # conditions for hitting the sides of the posts
        hitLP = ((top < goalPosts[-1] and right == goalPosts[0]) or \
                 (top < goalPosts[-1] and left == goalPosts[0] + goalPosts[2]))
        hitRP = ((top < goalPosts[-1] and left == goalPosts[1]) or \
                 (top < goalPosts[-1] and right == goalPosts[1] - goalPosts[2]))
        hitLPFromBelow = top == goalPosts[-1] and \
                         (left >= goalPosts[0] - self.diameter and \
                          left <= goalPosts[0] + goalPosts[2])
        hitRPFromBelow = top == goalPosts[-1] and \
                         (right <= goalPosts[0] + self.diameter and \
                          right >= goalPosts[0] - goalPosts[2])
        if hitLP or hitRP:
            return 'side'
        elif hitLPFromBelow or hitRPFromBelow:
            return 'from below'
        
    def bounceBack(self, switch):
        '''This function modifies the step size and angle to make the ball
        bounce back from either the screen boundaries or the goal posts.
        switch denotes whether the direction in which the ball is moving will 
        be flipped laterally or vertically.'''
        factor = random.uniform(1.03, 1.05)   # a random real number
        if switch == 'x':
            # ball bouncing back in the x-direction
            self.setStep(self.getStep()[0]/-factor, self.getStep()[1]/factor)
            self.setMovingAngle(-self.getMovingAngle())
        elif switch == 'y':
            # ball bouncing back in the y-direction
            self.setStep(self.getStep()[0]/factor, self.getStep()[1]/-factor)
            if self.getMovingAngle() < 0:
                self.setMovingAngle(-180 - self.getMovingAngle())
            else:
                self.setMovingAngle(180 - self.getMovingAngle())

    def checkBouncing(self, goalPosts):
        '''This function checks if the ball has hit either the screen boundaries
        or the goal posts, in which case the ball will bounce back and the
        function will return True. Otherwise the function will return False.
        goalPosts denotes the x-coordinates and size of the goal posts.'''
        # leftmost, rightmost, top, and bottom points on the ball
        left, right, top, bottom = self.getExtremes()
        stepX, stepY = self.getStep()   # current step size
        # After reaching the screen boundaries, the ball will bounce back
        # and continue moving at a reduced speed.
        if left == 0 or right == self.screenWidth:
            self.bounceBack('x')   # ball bouncing back in the x direction
        elif top == 0 or bottom == self.screenHeight:
            self.bounceBack('y')   # ball bouncing back in the y direction
        # Ball will also bounce back if it hits the goal posts.
        if self.hitGoalPosts(goalPosts) == 'side':   # hit the side of the post
            self.bounceBack('x')   # ball bouncing back in the x direction
        elif self.hitGoalPosts(goalPosts) == 'from below':
            # hit the post from below the goal line
            if right == goalPosts[0] or right == goalPosts[1] - goalPosts[2]:
                # ball hit the goal post right at the corner
                if self.stepX < 0:   # ball moving to the right
                    self.bounceBack('x')   # bounce back in the x direction
            elif left == goalPosts[1] or left == goalPosts[1] - goalPosts[2]:
                # ball hit the goal post right at the corner
                if self.stepX > 0:   # ball moving to the left
                    self.bounceBack('x')   # bounce back in the x direction
            else:
                self.bounceBack('y')   # ball bouncing back in the y direction
        # return True if the step size has been modified
        if self.stepX != stepX or self.stepY != stepY:
            return True
        else:
            return False

    def hitPlayer(self, players, minDist):
        '''This function handles ball movements when the ball is about to hit or
        has hit a player, and sets the step size accordingly.
        players is an array listing the players in the game. The goalkeeper
        must be listed first.
        minDist is the nearest distance to the player that the ball can get.'''
        self.gkCaught = False   # ball hasn't been caught by the goalkeeper
        for player in players:
            # player's parameters: coordinates of body center & current rotation
            pCenterPos = player.getCenterPos()[2]
            pRot = player.getRotation()
            # distance from ball to the player's body center, and angle 
            # (measured in degrees) of the ball with respect to the y-axis 
            # pointing downward
            dist, angle = line.getParams(pCenterPos,
                                         self.getCenterPos())[2:4]
            # current step size
            stepX, stepY = self.getStep()
            stepDiag = math.sqrt(stepX**2 + stepY**2)   # travel distance
            # new coordinates of the ball center if the ball moves with the
            # current step size
            newCenterPos = (self.getCenterPos()[0]-stepX,
                            self.getCenterPos()[1]-stepY)
            # new distance from ball to the player's body center 
            newDist = line.getParams(pCenterPos, newCenterPos)[2]
            if newDist < dist and dist > minDist and stepDiag > dist - minDist:
                # ball about to hit player --> set final step size
                stepX, stepY = move.setDiagStep(stepX, stepY,
                                                maxDist=dist-minDist+.2)
                self.setStep(stepX, stepY)
            # difference between the current rotation of the player and the 
            # angle just computed
            angleDiff = abs(pRot - angle)
            if self.hittingPlayer:   # ball has hit player
                self.hittingPlayer = False
                print('\nhit')
                if angleDiff >= 120 and angleDiff <= 240:
                    # ball hits the front of the player's body
                    self.setStep(0, 0)   # stop moving
                    if player == players[0]:   # goalkeeper has the ball
                        self.gkCaught = True
                    break
                else:
                    # ball hits the back of the player's body --> bounce back
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

    def move(self, stepSize, goalPosts, players, minDist):
        '''This function handles ball movements when the ball is kicked.
        goalPosts denotes the x-coordinates and size of the goal posts.
        players is an array listing the players in the game. The goalkeeper
        must be listed first.'''
        stepX, stepY = self.getStep()   # current step size
        # movement when ball hits or is about to hit a player
        self.hitPlayer(players, minDist)
        if self.stepX == 0 and self.stepY == 0:   # ball has stopped moving
            self.moving = False
        elif self.stepX != stepX or self.stepY != stepY:
            # step size has been adjusted --> move ball again
            # new coordinates of the ball center
            self.setCenterPos(self.getCenterPos()[0]-self.stepX,
                              self.getCenterPos()[1]-self.stepY)
            # update ball position and update display to show movement
            self.updateBall()
            if self.stepX * stepX > 0 and self.stepY * stepY > 0:
                self.hittingPlayer = True   # ball about to hit player
                self.setStep(stepX, stepY)   # reset step size
        if self.moving and not self.hittingPlayer:
            print('moving')
            stepX, stepY = self.getStep()   # current step size
            # set the size of the final step before the ball hits either the
            # screen boundaries or the goal posts
            self.setFinalStep2(goalPosts)
            # new coordinates of the ball center
            self.setCenterPos(self.getCenterPos()[0]-self.stepX,
                              self.getCenterPos()[1]-self.stepY)
            # update ball position and update display to show movement
            self.updateBall()
            if self.stepX != stepX or self.stepY != stepY:
                # step size has been adjusted --> reset it
                self.setStep(stepX, stepY)
            stepX, stepY = self.getStep()   # current step size
            # movement when ball hits the screen boundaries or the goal posts
            if self.checkBouncing(goalPosts):
                # new coordinates of the ball center
                self.setCenterPos(self.getCenterPos()[0]-self.stepX,
                                  self.getCenterPos()[1]-self.stepY)
                # update ball position and update display to show movement
                self.updateBall()
            self.decrementStep()   # decrement step size
        
    def resetBall(self):
        '''This function puts the ball at its original position after the 
        player scores.'''
        self.setCenterPos(self.getStartPos()[0][0]+self.center[0],
                          self.getStartPos()[0][1]+self.center[1])
        # update ball position and the display to show change
        self.updateBall()
        self.inGoal = False

    def updateBall(self):
        '''This function updates the position of the ball and updates the
        display to show movements.'''
        move.update(self.screen, self.allThings, self.allPos,
                    (self.ball,self.ball), (self.getCenterPos(),))
        self.updateDisplay()
