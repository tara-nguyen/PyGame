'''The following classes are defined: Game, Background, Goal, and Ball.
For neatness, the Player class, which is a child class of Game, is defined in a
different module named PlayerClasses.
To get a brief description of each class, use the following syntax:
    <module name as imported>.<class name>.__doc__'''

import pygame, random, math
import CroppingImages as crop
import LineParams as line
import MoveFunctions as move

class Game:
    '''This class is the parent class Background, Goal, Player, and Ball.
    This class has the following methods: __init__, updateDisplay, getFile,
    loadImage, addToLists, getLists and processMoveKeys.
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

    def addToLists(self, allThings, allPos, methodName, numPlayers):
        '''This function adds items to a list of everything on the screen
        (allThings), and to a list of those things' positions (allPos). NOTE!!! 
        For this function to work properly, the items must be added in the 
        following order: things in the Background class first, followed by those 
        in the Goal and the Ball classes, and finally things in the Player class.
        methodName is the name of the method used to get the drawing positions.
        numPlayers is the number of players in the game.'''
        # add items to the list of everything on the screen
        allThings += self.things
        # add items to the list of those things' positions
        if methodName == 'pos':   # Background class
            allPos += [self.pos]
        elif methodName == 'getPos':   # Goal class
            allPos += self.getPos()
        else:   # Ball class and Player class
            allPos += self.getStartPos()
        # rearrange lists so that the items representing the players' bodies are
        # at the end of each list
        if len(allThings) == 5 + numPlayers*3:   # end of list
            allThingsTemp, allPosTemp = allThings[:4], allPos[:4]
            for num in range(numPlayers):
                allThingsTemp += allThings[(5+num*3):(5+num*3+2)]
                allPosTemp += allPos[(5+num*3):(5+num*3+2)]
            allThingsTemp += [allThings[4]] 
            allPosTemp += [allPos[4]]
            for num in range(numPlayers):
                allThingsTemp += [allThings[5+num*3+2]]
                allPosTemp += [allPos[5+num*3+2]]
            allThings, allPos = allThingsTemp, allPosTemp
            return allThings, allPos

    def getLists(self, allThings, allPos):
        '''This function turns the list of everything on the screen (allThings)
        and the list of those things' positions (allPos) into class attributes.'''
        self.allThings = allThings
        self.allPos = allPos

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
    '''This class is a child class of Game and has three methods: __init__, 
    load, and blit.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Background.<method name>.__doc__'''
    def __init__(self, screenSize):
        '''This function initializes the class and sets its core attributes.'''
        Game.__init__(self, screenSize)   # initialize the parent class
        self.grass = None   # contains nothing
        
    def load(self, imageName):
        '''This function loads the background image into PyGame.'''
        self.grass = Game.loadImage(self, imageName,
                                    self.screenWidth, self.screenHeight)
        
    def blit(self):
        '''This function draws the background image onto the screen.'''
        self.pos = 0, 0   # where the image will be drawn
        self.screen.blit(self.grass, self.pos)
        self.things = [self.grass]

class Goal(Game):
    '''This class is a child class of Game and has the following methods:
    __init__, crop, load, setPos, blit, getPos, getCenter, and getCenterPos.
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
        self.height = 80   # final goal height

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
        self.lCenter, self.mCenter, self.rCenter = self.getCenter()
        self.mPos = self.screenCenter[0]-self.mCenter[0], 0
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

class Ball(Game):
    '''This class is a child class of Game and has the following methods:
    __init__, load, blit, getStartPos, setCenterPos, getCenterPos, 
    setMovingAngle, getMovingAngle, getSinCos, setFirstStep, setStep, getStep, 
    setVelocity, getVelocity, decrementStep, getExtremes, setFinalStep1, 
    setFinalStep2, hitGoalPosts, bounceBack, checkBouncing, hitPlayer, 
    checkGoal, move, resetBall, and updateBall.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Ball.<method name>.__doc__'''
    def __init__(self, screenSize):
        '''This function initializes the class and sets its core attributes.'''
        Game.__init__(self, screenSize)   # initialize the parent class
        self.ball = None   # contains nothing
        self.diameter = 36
        self.gkCaught = False

    def load(self, imageName):
        '''This function loads the ball image into PyGame.'''
        self.ball = Game.loadImage(self, imageName, self.diameter, self.diameter)
        
    def blit(self):
        '''This function draws the ball onto the screen.'''
        X = (self.screenWidth - self.diameter) / 2
        Y = self.screenHeight - 200
        self.startPos = X, Y   # where the ball will be drawn
        self.screen.blit(self.ball, self.startPos)
        self.center = self.ball.get_rect().center   # center of the ball
        # coordinates of the center at the start of the program
        self.centerPos = X+self.center[0], Y+self.center[1]
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
        # the leftmost, rightmost, top, and bottom points on the ball
        left, right, top, bottom = self.getExtremes()
        # set the size of the final step before the ball reaches the
        # screen boundaries
        if self.stepX > left:
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
        factor = random.uniform(1.03, 1.05)   # a random real number
        if switch == 'x':
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
        # leftmost, rightmost, top, and bottom points on the ball
        left, right, top, bottom = self.getExtremes()
        stepX, stepY = self.getStep()   # current step size
        # After reaching the screen boundaries, the ball will bounce back
        # and continue moving at a reduced speed.
        if left == 0 or right == self.screenWidth or \
           top == 0 or bottom == self.screenHeight:
            if left == 0 or right == self.screenWidth:
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
        # return True if the step size has been modified
        if self.stepX != stepX or self.stepY != stepY:
            return True
        else:
            return False
    
    def hitPlayer(self, numPlayers, playerRots, feetMidpoints, minDist):
        '''This function handles ball movements when it runs into the player.
        The ball will stop moving if it hits the player from the front, but will
        bounce back if it hits the player from the side or from the back.
        numPlayers is the number of players in the game.
        playerRots is a tuple of the players' current rotations (angles measured
        in degrees). The goalkeeper's comes first.
        feetMidpoints is a tuple of the midpoint of the line connecting each 
        player's feet at their centers. Again, the goalkeeper's comes first.
        minDist is the nearest distance to each player that the ball can get.'''
        self.gkCaught = False   # ball hasn't been caught by the goalkeeper
        for i in range(numPlayers):
            # distance from ball to the midpoint, and angle (measured in 
            # degrees) of the ball with respect to the y-axis pointing down
            # from the midpoint
            dist, angle = line.getParams(feetMidpoints[i],
                                         self.getCenterPos())[2:4]
            # difference between the current rotation of the player and the 
            # angle just computed
            angleDiff = abs(playerRots[i] - angle)
            if dist <= minDist:
                if angleDiff >= 120 and angleDiff <= 240:
                    # ball reaches the front of the player's body
                    self.setStep(0, 0)   # stop moving
                    if i == 0:   # goalkeeper has the ball
                        self.gkCaught = True
                    break
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

    def move(self, stepSize, goalPosts, numPlayers, playerRots, feetMidpoints,
             minDist):
        '''This function handles ball movements when the ball is kicked.
        goalPosts denotes the x-coordinates and size of the goal posts.
        numPlayers is the number of players in the game.
        playerRots is a tuple of the current rotations of the players (angles 
        measured in degrees).
        feetMidpoints is a tuple of the midpoint of the line connecting each 
        player's feet at their centers.
        minDist is the nearest distance to each player that the ball can get.'''
        self.setVelocity()   # ball's velocity
        # set the size of the final step before the ball reaches either the
        # screen boundaries or the goal posts
        self.setFinalStep2(goalPosts)
        # new coordinates of the ball center
        self.setCenterPos(self.getCenterPos()[0]-self.stepX,
                          self.getCenterPos()[1]-self.stepY)
        # update ball position and update display to show movement
        self.updateBall()
        stepX, stepY = self.getStep()   # current step size
        if self.checkBouncing(goalPosts):
            # ball bouncing back after hitting either the screen boundaries
            # or the goal posts
            # new coordinates of the ball center
            self.setCenterPos(self.getCenterPos()[0]-self.stepX,
                              self.getCenterPos()[1]-self.stepY)
            # update ball position and update display to show movement
            self.updateBall()
        # movement when ball hits player
        self.hitPlayer(numPlayers, playerRots, feetMidpoints, minDist)
        if self.stepX == 0 and self.stepY == 0:   # ball has stopped moving
            self.moving = False
        if self.stepX != stepX or self.stepY != stepY:
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

    def updateBall(self):
        '''This function updates the position of the ball and updates the
        display to show movements.'''
        move.update(self.screen, self.allThings, self.allPos, 
                    (self.ball,self.ball), (self.getCenterPos(),))
        self.updateDisplay()
