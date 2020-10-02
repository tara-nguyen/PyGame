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
    addToLists, getLists and processMoveKeys.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Game.<method name>.__doc__'''
    def __init__(self, screenSize):
        '''This function initializes the class and sets its core attributes.'''
        # screen size
        self.screenWidth = screenSize[0]
        self.screenHeight = screenSize[1]
        self.screen = pygame.display.set_mode(screenSize)
        self.screenCenter = self.screenWidth/2, self.screenHeight/2
        self.frame = pygame.time.Clock()   # initializes clock
        
    def updateDisplay(self):
        '''This function updates the display and sets the maximum number of
        frames per second.'''
        pygame.display.flip()   # updates/clears display
        self.frame.tick(30)   # maximum number of frames per second
        
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
        moveType, direction = None, None
        if pressedKeys[pygame.K_LEFT] == 1:   # left arrow key has been pressed
            if pressedKeys[pygame.K_RSHIFT] == 1:
                # right shift key pressed at the same time
                moveType = 'circle'
            else:
                moveType = 'straight'
            direction = 'left'
        if pressedKeys[pygame.K_RIGHT] == 1:  # right arrow key has been pressed
            if pressedKeys[pygame.K_RSHIFT] == 1:
                # right shift key pressedat the same time
                moveType = 'circle'
            else:
                moveType = 'straight'
            direction = 'right'
        if pressedKeys[pygame.K_UP] == 1:   # up arrow key has been pressed
            moveType = 'straight'
            if pressedKeys[pygame.K_LEFT] == 1:
                # left arrow key pressed at the same time
                direction = 'up left'
            elif pressedKeys[pygame.K_RIGHT] == 1:
                # right arrow key pressed at the same time
                direction = 'up right'
            else:
                direction = 'up'
        if pressedKeys[pygame.K_DOWN] == 1:   # down arrow key has been pressed
            moveType = 'straight'
            if pressedKeys[pygame.K_LEFT] == 1:
                # left arrow key pressed at the same time
                direction = 'down left'
            elif pressedKeys[pygame.K_RIGHT] == 1:
                # right arrow key pressed at the same time
                direction = 'down right'
            else:
                direction = 'down'
        if pressedKeys[pygame.K_SPACE] == 1:   # spacebar has been pressed
            moveType = 'to ball'
        return moveType, direction
        
class Background(Game):
    '''This class is a child class of Game and has three methods: __init__, 
    load, and blit.
    To get a brief description of each method, use the following syntax:
        <module name as imported>.Background.<method name>.__doc__'''
    def __init__(self, screenSize):
        '''This function initializes the class and sets its core attributes.'''
        Game.__init__(self, screenSize)   # initializes the parent class
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
        Game.__init__(self, screenSize)   # initializes the parent class
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
        lCenter = self.left.get_rect().center
        mCenter = self.middle.get_rect().center
        rCenter = self.right.get_rect().center
        return lCenter, mCenter, rCenter

    def getCenterPos(self):
        '''This function returns the coordinates of the center of each
        goal part.'''
        # positions of the goal parts (i.e., where they were drawn)
        self.lPos, self.mPos, self.rPos = self.getPos()
        # centers of the goal parts
        lCenter, mCenter, rCenter = self.getCenter()
        # coordinates of the centers
        lCenterPos = self.lPos[0]+lCenter[0], self.lPos[1]+lCenter[1]
        mCenterPos = self.mPos[0]+mCenter[0], self.mPos[1]+mCenter[1]
        rCenterPos = self.rPos[0]+rCenter[0], self.rPos[1]+rCenter[1]
        return [lCenterPos, mCenterPos, rCenterPos]

    def getPosts(self):
        '''This function returns the x-coordinates & the size of the goal posts.'''
        leftPost, rightPost = self.lPos[0], self.rPos[0]+self.sideWidth
        postWidth, postHeight = 11, self.height
        return leftPost, rightPost, postWidth, postHeight

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
        Game.__init__(self, screenSize)   # initializes the parent class
        self.ball = None   # contains nothing
        self.diameter = 36
        self.moving = False
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
        distance is the distance from the ball to the boundary/goal post.'''
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
                if left > goalPosts[1] and self.stepX > left - goalPosts[1]:
                    # right of right goal post and moving left
                    self.setFinalStep1('x', left-goalPosts[1])
                if left > goalPosts[0] + goalPosts[2] and \
                   self.stepX > left - (goalPosts[0] + goalPosts[2]):
                    # right of left goal post and moving left
                    self.setFinalStep1('x', left-(goalPosts[0]+goalPosts[2]))
                if right < goalPosts[1] - goalPosts[2] and \
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
                    self.bounceBack('x')   # bounces back in the x direction
            elif left == goalPosts[1] or left == goalPosts[1] - goalPosts[2]:
                # ball hit the goal post right at the corner
                if self.stepX > 0:   # ball moving to the left
                    self.bounceBack('x')   # bounces back in the x direction
            else:
                self.bounceBack('y')   # ball bouncing back in the y direction
        # return True if the step size has been modified
        if self.stepX != stepX or self.stepY != stepY:
            return True
        else:
            return False
    
    def hitPlayer(self, numPlayers, playerRots, playerCenterPos, minDist):
        '''This function handles ball movements when the ball is about to hit or
        has hit a player, and sets the step size accordingly.
        numPlayers is the number of players in the game.
        playerRots is a tuple of the players' current rotations (angles measured
        in degrees). The goalkeeper's comes first.
        playerCenterPos is a tuple of the coordinates of the centers of the
        players' bodies. Again, the goalkeeper's comes first.
        minDist is the nearest distance to each player that the ball can get.'''
        self.gkCaught = False   # ball hasn't been caught by the goalkeeper
        for i in range(numPlayers):
            # distance from ball to the player's body center, and angle 
            # (measured in degrees) of the ball with respect to the y-axis 
            # pointing down from the body center
            dist, angle = line.getParams(playerCenterPos[i],
                                         self.getCenterPos())[2:4]
            # current step size and rate of moving
            stepX, stepY = self.getStep()
            rate = math.sqrt(stepX**2 + stepY**2)
            # new coordinates of the ball center if the ball moves with the
            # current step size
            newCenterPos = (self.getCenterPos()[0]-stepX,
                            self.getCenterPos()[1]-stepY)
            # new distance from ball to the player's body center 
            newDist = line.getParams(playerCenterPos[i], newCenterPos)[2]
            if i == 1:
            if newDist < dist and dist > minDist and rate > dist - minDist:
                # ball is about to hit the player --> set final step size
                stepX, stepY = move.setDiagStep(stepX, stepY,
                                                maxDist=dist-minDist+.2)
                self.setStep(stepX, stepY)
            # difference between the current rotation of the player and the 
            # angle just computed
            angleDiff = abs(playerRots[i] - angle)
            if dist <= minDist:
                print('\nhit')
                if angleDiff >= 120 and angleDiff <= 240:
                    # ball hits the front of the player's body
                    self.setStep(0, 0)   # stops moving
                    if i == 0:   # goalkeeper has the ball
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

    def move(self, stepSize, goalPosts, numPlayers, playerRots, playerCenterPos,
             minDist):
        '''This function handles ball movements when the ball is kicked.
        goalPosts denotes the x-coordinates and size of the goal posts.
        numPlayers is the number of players in the game.
        playerRots is a tuple of the current rotations of the players (angles 
        measured in degrees).
        playerCenterPos is a tuple of the coordinates of the centers of the
        players' bodies.
        minDist is the nearest distance to each player that the ball can get.'''
        stepX, stepY = self.getStep()   # current step size
        # movement when ball hits or is about to hit a player
        self.hitPlayer(numPlayers, playerRots, playerCenterPos, minDist)
        if self.stepX == 0 and self.stepY == 0:   # ball has stopped moving
            self.moving, hittingPlayer = False, True
        elif self.stepX != stepX or self.stepY != stepY:
            # step size has been adjusted --> move ball again
            # new coordinates of the ball center
            self.setCenterPos(self.getCenterPos()[0]-self.stepX,
                              self.getCenterPos()[1]-self.stepY)
            # update ball position and update display to show movement
            self.updateBall()
            if self.stepX * stepX > 0 and self.stepY * stepY > 0:
                hittingPlayer = True
                self.setStep(stepX, stepY)   # resets step size
        else:
            hittingPlayer = False
        if self.moving and not hittingPlayer:
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
            self.decrementStep()   # decrements step size
        
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
