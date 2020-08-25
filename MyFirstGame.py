import pygame, sys, random, math
import CroppingImages as crop
import LineParams as line
import MoveFunctions as move

def update(moved, newCenterPos, rotate=False, update=True):
    '''This function redraws things on the screen to show movements.
    moved is a tuple/list of objects that will be moved after the redrawing, 
    along with the original surfaces containing the moved objects at the 
    beginning of the program.
    newCenterPos is a tuple/list of the new coordinates of the moved objects' 
    center points after being redrawn.
    rotate, if specified, is a tuple/list of the angles (measured in degrees) by 
    which the moved objects will rotate. The default is that there is no change
    from the original rotation.
    update denotes whether or not the display needs updating.'''
    move.update(screen, things, thingsPos, moved, newCenterPos, rotate)
    if update == True:
        pygame.display.flip()   # update/clear display
        frame.tick(30)   # maximum number of frames per second
    
def processMoveKeys():
    '''This function processes pressed keys that will initiate player movements.'''    
    pressed, direction, moveType = [False] * 3
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
        direction = False
        moveType = 'to ball'
    return pressed, direction, moveType

def getRotation():
    '''This function returns the current rotation of the player, i.e., the
    direction the player is currently facing, with respect to the y-axis pointing
    down from the midpoint of the line connecting the two feet at their centers.
    The function also returns that midpoint.'''
    # midpoint of the line connecting the two feet at their centers
    midPoint = ((lFootCenterPos[0]+rFootCenterPos[0])/2,
                (lFootCenterPos[1]+rFootCenterPos[1])/2)
    # direction the player is currently facing (angle measured in degrees)
    currentRot = line.getParams(midPoint, bodyCenterPos)[3]
    return currentRot, midPoint

def feetToFront(target):
    '''This function moves the player's feet to the front of the player's body.
    target is either the point around which the player rotates or the point
    toward which the player moves.'''
    global lFootCenterPos, rFootCenterPos
    # direction the player is currently facing (angle measured in degrees)
    currentRot = getRotation()[0]
    if target != bodyCenterPos:
        # angle (measured in degrees) of the body with respect to the y-axis
        # pointing down from the target point
        bodyAngle = line.getParams(target, bodyCenterPos)[3]
        if bodyAngle != currentRot:
            lFootCenterPos = (
                move.moveCircle(bodyCenterPos, lFootCenterPos, 'right',
                                step=bodyAngle-currentRot)[0])
            rFootCenterPos = (
                move.moveCircle(bodyCenterPos, rFootCenterPos, 'right',
                                step=bodyAngle-currentRot)[0])
    else:
        # player is already at the target point
        lFootCenterPos = (
            move.moveCircle(bodyCenterPos, lFootCenterPos, 'right',
                            step=rotate-currentRot)[0])
        rFootCenterPos = (
            move.moveCircle(bodyCenterPos, rFootCenterPos, 'right',
                            step=rotate-currentRot)[0])

def getEndPoint(centerPos, finalDist):
    '''This function determines the point to which an object (either the player
    or one of the feet) will move.
    centerPos is the current coordinates of the center of the object.
    finalDist is the distance from the body to the ball when the object is at
    the target end point.'''
    # angle (measured in degrees) of the moved object (player or foot) with 
    # respect to the y-axis pointing down from the ball
    angle = line.getParams(ballCenterPos, centerPos)[3]
    # angle measured in radians
    angle *= math.pi/180
    # point to which the foot will move
    endPointX = ballCenterPos[0] + finalDist * math.sin(angle)
    endPointY = ballCenterPos[1] + finalDist * math.cos(angle)
    endPoint = endPointX, endPointY
    # direction object will be facing when it has reached end point
    endAngle = line.getParams(ballCenterPos, endPoint)[3]   # measured in degrees
    return endPoint, endAngle

def movePlayer(moveType, direction=False, step=10):
    '''This function moves the player's body and feet at the same time.
    moveType is the type of movement (circle, straight, or to point).
    For circle movements, step is the change in the angle (measured in degrees) by which the object
    will move at each keypress.
    For straight movements, step is the number of pixels by which the object will
    move either horizontally or vertically at each keypress.'''
    global bodyCenterPos, lFootCenterPos, rFootCenterPos, rotate, playerMoved
    oldCenterPos = bodyCenterPos   # body position before moving
    if moveType == 'circle':
        # current angle (measured in degrees) of the body with respect to the 
        # y-axis pointing down from the ball
        bodyAngle = line.getParams(ballCenterPos, oldCenterPos)[3]
        # rotate body and feet around ball
        bodyCenterPos, rotate = move.moveCircle(
            ballCenterPos, oldCenterPos, direction, step,
            boundaryX=[0,screenWidth], boundaryY=[0,screenHeight],
            objCenter=bodyCenter)
        if rotate != bodyAngle:
            # body still moving, so feet still move too
            # set step size; make sure it's between 0 and 180 degrees
            if rotate - bodyAngle > 180:
                step = abs(rotate - bodyAngle - 360)
            elif rotate - bodyAngle < -180:
                step = abs(rotate - bodyAngle + 360)
            else:
                step = abs(rotate - bodyAngle)
            # move feet
            lFootCenterPos = move.moveCircle(ballCenterPos, lFootCenterPos,
                                             direction, step=step)[0]
            rFootCenterPos = move.moveCircle(ballCenterPos, rFootCenterPos,
                                             direction, step=step)[0]
        feetToFront(ballCenterPos)   # move feet to front of body
    elif moveType == 'straight':
        # move body
        bodyCenterPos, rotate = move.moveStraight(
            bodyCenter, oldCenterPos, direction, stepX=step, stepY=step,
            boundaryX=[feetOut,screenWidth-feetOut],
            boundaryY=[feetOut,screenHeight-feetOut])
        # distance moved
        moveX, moveY = line.getParams(bodyCenterPos, oldCenterPos)[:2]
        # move feet at the same distance as body
        lFootCenterPos = lFootCenterPos[0]+moveX, lFootCenterPos[1]+moveY
        rFootCenterPos = rFootCenterPos[0]+moveX, rFootCenterPos[1]+moveY
        # direction the player is currently facing (angle measured in degrees)
        currentRot = getRotation()[0]
        if currentRot != rotate:
            # player is facing the wrong direction --> move feet around body
            feetToFront(bodyCenterPos)
    elif 'to ' in moveType:
        # distance from body to ball when player is at target end point
        finalDist = bodyOrigCenter[1] + feetOut + ballCenter[1]
        # point to which body will move
        endPoint, endAngle = getEndPoint(bodyCenterPos, finalDist)
        feetToFront(endPoint)   # move feet to front of body
        # distance left to go
        dist = line.getParams(endPoint, oldCenterPos)[2]
        # move body to end point
        bodyCenterPos, rotate = move.moveToPoint(endPoint, bodyCenterPos,
                                                 endAngle=endAngle, speedBoost=2)
        # distance moved
        moveX, moveY, moveDist = line.getParams(bodyCenterPos, oldCenterPos)[:3]
        # move feet at the same distance as body
        lFootCenterPos = lFootCenterPos[0]+moveX, lFootCenterPos[1]+moveY
        rFootCenterPos = rFootCenterPos[0]+moveX, rFootCenterPos[1]+moveY
        if dist != 0 and moveDist == dist:
            # final step has been made --> move feet to front of body
            feetToFront(endPoint)
    if bodyCenterPos != oldCenterPos:
        playerMoved = True

def getBallExtremes():
    '''This function returns the leftmost, rightmost, top, and bottom points
    on the ball'''
    ballLeft = ballCenterPos[0] - ballCenter[0]
    ballRight = ballLeft + ballWidth
    ballTop = ballCenterPos[1] - ballCenter[1]
    ballBottom = ballTop + ballWidth
    return ballLeft, ballRight, ballTop, ballBottom

def setFinalStep(direction, distance, ballAngle):
    '''This function sets the size of the final step before the ball reaches
    screen boundaries or before it reaches the goal posts.
    direction denotes which way the ball is moving (x direction or y direction).
    distance is the distance from the ball to the boundary/goal post.
    ballAngle is the angle (measured in radians) at which the ball is moving,
    with respect to the negative y-axis pointing up from the ball at the
    current position.'''
    if direction == 'x':
        # ball reached either the left or the right side of the screen, or
        # reached one of the goal posts
        stepX = distance
        stepY = stepX / math.tan(ballAngle)
    else:
        # ball reached either the top or the bottom of the screen
        stepY = distance
        stepX = stepY * math.tan(ballAngle)
    return stepX, stepY

def bounceBack(currentSpeed, ballAngle, switch):
    '''This function modifies the step size and the ball angle to make the ball
    bounce back from a boundary (e.g., one of the screen boundaries or one of
    the goal posts).
    switch denotes whether it is the lateral step (stepX) or the vertical step
    (stepY) whose sign needs to be switched.'''
    global ballCenterPos
    factor = random.uniform(1.03, 1.05)
    if switch == 'x':
        # ball bouncing back in the x direction
        stepX = currentSpeed[0] / -factor
        stepY = currentSpeed[1] / factor
        ballAngle *= -1
    elif switch == 'y':
        # ball bouncing back in the y direction
        stepX = currentSpeed[0] / factor
        stepY = currentSpeed[1] / -factor
        if ballAngle < 0:
            ballAngle = -math.pi - ballAngle
        else:
            ballAngle = math.pi - ballAngle
    # move ball and update display to show movement
    ballCenterPos = ballCenterPos[0]-stepX, ballCenterPos[1]-stepY
    update((ball,ballOrig), (ballCenterPos,))
    return stepX, stepY, ballAngle

def moveBall(bodyAngle):
    '''This function handles ball movements when the ball is kicked.
    bodyAngle is the angle (measured in degrees) of the body with respect to the
    y-axis pointing down from the ball.'''
    global ballCenterPos
    scored = False
    # angle (measured in radians) at which ball will move, with respect to
    # the negative y-axis pointing up from the ball at the current position
    ballAngle = random.uniform(bodyAngle-1, bodyAngle+1) * math.pi/180
    # initial step size
    stepDiag = random.uniform(28, 32)
    stepX = stepDiag * math.sin(ballAngle)
    stepY = stepDiag * math.cos(ballAngle)
    while round(stepDiag) > 0:
        speed = stepX, stepY
        # the leftmost, rightmost, top, and bottom points on the ball
        ballLeft, ballRight, ballTop, ballBottom = getBallExtremes()
        # size of the final step before the ball reaches screen boundaries 
        # or before it reaches the goal posts
        if stepX > ballLeft:
            # ball reaching left side of the screen
            stepX, stepY = setFinalStep('x', ballLeft, ballAngle)
        if stepX < ballRight - screenWidth:
            # ball reaching right side of the screen
            stepX, stepY = setFinalStep('x', ballRight-screenWidth,
                                        ballAngle)
        if stepY > ballTop:
            # ball reaching top side of the screen
            stepX, stepY = setFinalStep('y', ballTop, ballAngle)
        if stepY < ballBottom - screenHeight:
            # ball reaching bottom side of the screen
            stepX, stepY = setFinalStep('y', ballBottom-screenHeight,
                                        ballAngle)
        goalPosts = goalLeftPos[0], goalRightPos[0]+goalLeftWidth
        if ballTop < goalHeight:
            if ballRight < goalPosts[0] and stepX < ballRight-goalPosts[0]:
                # ball reaching the outside of the left post
                stepX, stepY = setFinalStep('x', ballRight-goalPosts[0],
                                            ballAngle)
            if ballLeft > goalPosts[1] and stepX > ballLeft-goalPosts[1]:
                # ball reaching the outside of the right post
                stepX, stepY = setFinalStep('x', ballLeft-goalPosts[1],
                                            ballAngle)
            if ballLeft > goalPosts[0]+postWidth and \
               stepX > ballLeft-(goalPosts[0]+postWidth):
                # ball reaching the inside of the left post
                stepX, stepY = setFinalStep(
                    'x', ballLeft-(goalPosts[0]+postWidth), ballAngle)
            if ballRight < goalPosts[1]-postWidth and \
               stepX < ballRight-(goalPosts[1]-postWidth):
                stepX, stepY = setFinalStep(
                    'x', ballRight-(goalPosts[1]-postWidth), ballAngle)
        # move ball and update display to show movement
        ballCenterPos = ballCenterPos[0]-stepX, ballCenterPos[1]-stepY
        update((ball,ballOrig), (ballCenterPos,))
    ######################################################################            
        # new leftmost, rightmost, top, and bottom points on the ball
        ballLeft, ballRight, ballTop, ballBottom = getBallExtremes()
        # After reaching the screen boundaries, the ball will bounce back
        # and continue moving at a reduced speed.
        if ballLeft == 0 or ballRight == screenWidth or \
           ballTop == 0 or ballBottom == screenHeight:
            if ballLeft == 0 or ballRight == screenWidth:
                stepX, stepY, ballAngle = bounceBack(speed, ballAngle, 'x')
            else:
                stepX, stepY, ballAngle = bounceBack(speed, ballAngle, 'y')
        # Ball will stop moving if it comes back to the front of the player, but
        # will bounce back if it hits the back of the player.
        # direction the player is currently facing (angle measured in degrees),
        # and midpoint of the line connecting the two feet at their centers
        currentRot, midPoint = getRotation()
        # distance from ball to the midpoint, and angle (measured in degrees) of
        # the ball with respect to the y-axis pointing down from the midpoint
        ballToMP_dist, ballToMP_angle = \
                       line.getParams(midPoint, ballCenterPos)[2:4]
        angleDiff = abs(ballToMP_angle-currentRot)   # angle difference
        if ballToMP_dist <= ballCenter[1]+bodyOrigCenter[1]+feetOut-5:
            if angleDiff >= 100 and angleDiff <= 260:
                # ball stops moving
                stepX = 0
                stepY = 0
                break
            else :
                # ball bouncing back
                stepX, stepY, ballAngle = bounceBack(speed, ballAngle,
                                                     random.choice(['x','y']))
        # Ball will also bounce back if it hits the goal posts.
        # conditions for hitting the outside of the posts
        hitLPFromOut = ballTop < goalHeight and \
                       ballLeft < goalPosts[0] and \
                       ballRight >= goalPosts[0] and \
                       ballAngle < 0 and ballAngle > -math.pi
        hitRPFromOut = ballTop < goalHeight and \
                       ballRight > goalPosts[1] and \
                       ballLeft <= goalPosts[1] and \
                       ballAngle > 0 and ballAngle < math.pi
        # conditions for hitting the inside of the posts
        hitLPFromIn = ballTop < goalHeight and \
                      ballRight > goalPosts[0]+postWidth and \
                      ballLeft <= goalPosts[0]+postWidth and \
                      ballAngle > 0 and ballAngle < math.pi
        hitRPFromIn = ballTop < goalHeight and \
                      ballLeft < goalPosts[1]-postWidth and \
                      ballRight >= goalPosts[1]-postWidth and \
                      ballAngle < 0 and ballAngle > -math.pi
        if hitLPFromOut or hitRPFromOut:
            if ballCenterPos[1] > goalHeight and abs(ballAngle) < math.pi/2:
                # ball bouncing back in the y direction
                stepX, stepY, ballAngle = bounceBack(speed, ballAngle, 'y')
            else:
                # ball bouncing back in the x direction
                stepX, stepY, ballAngle = bounceBack(speed, ballAngle, 'x')
        if hitLPFromIn or hitRPFromIn:
            # ball bouncing back in the x direction
            stepX, stepY, ballAngle = bounceBack(speed, ballAngle, 'x')
        # Player scores if the ball is between the goal posts.
        if ballBottom <= goalHeight and ballLeft >= goalPosts[0] and \
           ballRight <= goalPosts[1]:
            scored = True
    ######################################################################            
        # decrement step size
        factor = random.uniform(1.03, 1.05)
        stepX /= factor
        stepY /= factor
        stepDiag = math.sqrt(stepX**2 + stepY**2)
    # If the player scores, the ball will be placed at a random position
    # after it has stopped moving.
    if scored == True:
        ballPosX = random.uniform(0, screenWidth-ballWidth)
        ballPosY = random.uniform(screenHeight/2, screenHeight-ballWidth)
        # move ball and update display to show movement
        ballCenterPos = ballPosX+ballCenter[0], ballPosY+ballCenter[1]
        update((ball,ballOrig), (ballCenterPos,), update=False)

def kickBall():
    '''This function makes the player kick the ball.'''
    global lFoot, rFoot
    # direction the body is currently facing (angle measured in degrees)
    currentRot = getRotation()[0]
    # distance from each foot to ball
    lFootToBall = line.getParams(ballCenterPos, lFootCenterPos)[2]
    rFootToBall = line.getParams(ballCenterPos, rFootCenterPos)[2]
    # the foot closer to the ball will be the one that kicks the ball
    if lFootToBall < rFootToBall:
        oldFootCenterPos = lFootCenterPos
    elif lFootToBall > rFootToBall:
        oldFootCenterPos = rFootCenterPos
    else:
        # ball is equidistant from both feet --> randomly pick the kicking foot
        oldFootCenterPos = random.choice([lFootCenterPos, rFootCenterPos])
    # distance from foot to ball when the foot touches the ball
    finalDist = footOrigCenter[1] + ballCenter[1] - 3
    # point to which the foot will move
    endPoint = getEndPoint(oldFootCenterPos, finalDist)[0]
    # move foot to ball
    newFootCenterPos, rotate = move.moveToPoint(endPoint, oldFootCenterPos,
                                                endAngle=currentRot)
    if oldFootCenterPos == lFootCenterPos:
        # left foot has changed both position and rotation
        newCenterPos = newFootCenterPos, rFootCenterPos
        rotate = rotate, currentRot
    else:
        # right foot has changed both position and rotation
        newCenterPos = lFootCenterPos, newFootCenterPos
        rotate = currentRot, rotate
    # update display to show movement
    update((lFoot,rFoot,foot,foot), newCenterPos, rotate=rotate)
    pygame.time.wait(100)   # pause program for 100 ms
    ######################################################################
    # bring foot back to the position and rotation before the kick
    moved = things[-4],things[-3], foot, foot
    if oldFootCenterPos == lFootCenterPos:
        # left foot has changed position
        newCenterPos = oldFootCenterPos, rFootCenterPos
    else:
        # right foot has changed position
        newCenterPos = lFootCenterPos, oldFootCenterPos
    # update display to show movement
    update(moved, newCenterPos, rotate=(currentRot,)*2)
    lFoot, rFoot = things[-4], things[-3]
    ######################################################################
    # check if the foot has touched the ball
    if newFootCenterPos == endPoint:
        # current angle (measured in degrees) of the body with respect to the 
        # y-axis pointing down from the ball
        bodyAngle = line.getParams(ballCenterPos, bodyCenterPos)[3]
        moveBall(bodyAngle)   # move ball
                       
'''BEGINNING OF PROGRAM'''

pygame.init()   # start pygame

# screen size
screenWidth = 550
screenHeight = 700
screenSize = screenWidth, screenHeight
screen = pygame.display.set_mode(screenSize)
screenCenter = screen.get_rect().center   # coordinates of center of the screen

pygame.display.set_caption('My First Game')   # game title

'''IMAGES IN PYGAME'''

# background image
grass = pygame.image.load('./ImagesInPyGame/grass.png').convert()
# rescale the image so that it covers the whole screen
grass = pygame.transform.scale(grass, screenSize)
# print image to the screen at specified coordinates
screen.blit(grass, (0,0))
thingsPos = [(0, 0)]   # position of everything on the screen at this point

# goal image, left part
goalLeft = pygame.image.load('./ImagesInPyGame/goalLeft.png').convert_alpha()
goalScale = 130, 250
goalLeft = pygame.transform.scale(goalLeft, goalScale)
'''There's white space in the original image, so we need to crop it
before printing it to the screen.'''
goalLeftWidth = 60
goalHeight = screenHeight / 7
postWidth = 11
shiftUp = 33
goalLeft = crop.cropImage(goalLeft, 'pixels', goalLeftWidth, goalHeight,
                          shiftLeft=11, shiftUp=shiftUp)

# goal image, middle part
goalMiddle = pygame.image.load('./ImagesInPyGame/goalMiddle.png').convert_alpha()
goalMiddle = pygame.transform.scale(goalMiddle, goalScale)
goalMiddleWidth = 120
goalMiddle = crop.cropImage(
    goalMiddle, 'pixels', goalMiddleWidth, goalHeight,
    shiftLeft=(goalScale[0]-goalMiddleWidth)/2, shiftUp=shiftUp)
# center of the image, relative to the top-left corner of the image
goalMiddleCenter = goalMiddle.get_rect().center

# goal image, right part
goalRight = pygame.image.load('./ImagesInPyGame/goalRight.png').convert_alpha()
goalRight = pygame.transform.scale(goalRight, goalScale)
goalRight = crop.cropImage(goalRight, 'pixels', goalLeftWidth, goalHeight,
                           shiftLeft=goalScale[0]-goalLeftWidth-11,
                           shiftUp=shiftUp)

# goal position
goalMiddlePosX = screenCenter[0] - goalMiddleCenter[0]
goalMiddlePos = goalMiddlePosX, 0
goalLeftPos = goalMiddlePosX-goalLeftWidth, 0
goalRightPos = goalMiddlePosX+goalMiddleWidth, 0
screen.blit(goalMiddle, goalMiddlePos)
screen.blit(goalLeft, goalLeftPos)
screen.blit(goalRight, goalRightPos)
# position of everything on the screen at this point
thingsPos += [goalLeftPos, goalMiddlePos, goalRightPos]

# ball image
ball = pygame.image.load('./ImagesInPyGame/ball.png').convert_alpha()
# convert_alpha() takes care of not only conversion but also transparency
# rescale image
ball = pygame.transform.scale(ball, (36,36))
# center of the image, relative to the top-left corner of the image
ballCenter = ball.get_rect().center
ballWidth = ballCenter[0] * 2   # width (or diameter) of the ball
# ball position
ballPosX = random.uniform(0, screenWidth-ballWidth)
ballPosY = random.uniform(screenHeight/2, screenHeight-ballWidth)
ballPosX = screenCenter[0]-ballCenter[0]
ballPosY = screenCenter[1]-ballCenter[1]
ballPos = ballPosX, ballPosY
# coordinates of center of the image, relative to the screen
ballCenterPos = ballPosX+ballCenter[0], ballPosY+ballCenter[1]
# duplicate
ballOrig = ball

# player's body image
body = pygame.image.load('./ImagesInPyGame/playerBody.png').convert_alpha()
oldBodyWidth = body.get_rect().width
oldBodyHeight = body.get_rect().height
body = pygame.transform.scale(body, (int(oldBodyWidth*2.5),
                                     int(oldBodyHeight*2.5)))
body = pygame.transform.rotate(body, 90)   # rotate 90 degrees counterclockwise
# center of the image, relative to the top-left corner of the image
bodyCenter = body.get_rect().center
# duplicate
bodyOrig = body   
bodyOrigCenter = bodyOrig.get_rect().center

# player's foot image
foot = pygame.image.load('./ImagesInPyGame/playerFoot.png').convert_alpha()
oldFootWidth = foot.get_rect().width
oldFootHeight = foot.get_rect().height
foot = pygame.transform.scale(foot, (int(oldFootWidth*2.35),
                                     int(oldFootHeight*2.35)))
foot = pygame.transform.rotate(foot, 90)   # rotate 90 degrees counterclockwise
footWidth = foot.get_rect().width
# center of the image, relative to the top-left corner of the image
footCenter = foot.get_rect().center
# duplicate
footOrigCenter = footCenter
# left foot and right foot
lFoot = foot
rFoot = foot

# body position
bodyPosX = random.uniform(0, screenWidth-bodyCenter[0]*2)
bodyPosY = random.uniform(goalHeight, screenHeight-bodyCenter[1]*2)
bodyPosX = screenCenter[0]-bodyCenter[0]-100
bodyPosY = screenCenter[1]+ballCenter[1]+20
bodyPos = bodyPosX, bodyPosY
# coordinates of center of the image, relative to the screen
bodyCenterPos = bodyPosX+bodyCenter[0], bodyPosY+bodyCenter[1]

# foot positions
footEndToBodyCenter = 1   # empty space between each foot and the vertical line
                            # that passes the body's center point
feetOut = 1   # how much of the feet will be sticking out in front of the body
# left foot
lFootPosX = bodyCenterPos[0] - footWidth - footEndToBodyCenter
lFootPosY = bodyPosY - feetOut
lFootPos = lFootPosX, lFootPosY
# right foot
rFootPosX = bodyCenterPos[0] + footEndToBodyCenter
rFootPosY = lFootPosY
rFootPos = rFootPosX, rFootPosY
# coordinates of center of the image, relative to the screen
lFootCenterPos = lFootPosX+footCenter[0], lFootPosY+footCenter[1]
rFootCenterPos = rFootPosX+footCenter[0], rFootPosY+footCenter[1]

# distance from body to each foot, and distance between two feet
bodyToFootX = footCenter[0] + footEndToBodyCenter
bodyToFootY = bodyCenter[1] - footCenter[1] + feetOut
footToFoot = bodyToFootX * 2

# draw the player and the ball
screen.blit(lFoot, lFootPos)
screen.blit(rFoot, rFootPos)
screen.blit(ball, ballPos)
screen.blit(body, bodyPos)
# position of everything on the screen at this point
thingsPos += [lFootPos, rFootPos, ballPos, bodyPos]

# everything on the screen
things = [grass, goalLeft, goalMiddle, goalRight, lFoot, rFoot, ball, body]

# keys used for player movements
moveKeys = 'left', 'left-rshift', 'right', 'right-rshift', 'up', 'down', 'space'

'''THE SKELETON OF THE GAME'''

frame = pygame.time.Clock()   # initialize clock

# display the game and its objects
playing = True
while playing == True:
    # process events in the game one by one
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            pygame.quit()
            sys.exit()   # prevents getting an error message when quitting the game

    '''PROCESSING PRESSED KEYS'''

    playerMoved = False
    pressedKeys = pygame.key.get_pressed()
    pressed, direction, moveType = processMoveKeys()
    if pressed in moveKeys:
        movePlayer(moveType, direction)
    if pressedKeys[pygame.K_s] == 1:
        # 's' key has been pressed --> kick the ball
        kickBall()
        
    if playerMoved == True:
        # both the feet and the body have moved
        moved = lFoot, rFoot, body, foot, foot, bodyOrig
        centerPos = lFootCenterPos, rFootCenterPos, bodyCenterPos
        # update display to show movement
        update(moved, centerPos, rotate=(rotate,)*len(centerPos), update=False)
        lFoot, rFoot, body = things[-4], things[-3], things[-1]
        # objects' center points after the movement
        footCenter = lFoot.get_rect().center
        bodyCenter = body.get_rect().center
        
    pygame.display.flip()   # update/clear display
    frame.tick(30)   # maximum number of frames per second
