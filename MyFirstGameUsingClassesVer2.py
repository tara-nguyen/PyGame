'''This is the main program for the second version of a mini-game of football/
soccer in PyGame. Compared to the first version, this version adds a goalkeeper.'''

import pygame, sys, random, math
import NonplayerClasses as nonplayer
import PlayerClasses as player

def processMovements():
    '''This function processes the movements of the ball and of the goalkeeper
    while the ball is moving.'''
    global goalkeeper, ball
    # angle (measured in degrees) at which the ball will move, with
    # respect to the y-axis pointing up from the current ball center
    ball.setMovingAngle(random.uniform(bodyAngle-1, bodyAngle+1))
    # initial step size of the ball
    stepSize = random.uniform(18, 22)
    ball.setFirstStep(stepSize)
    ball.moving = True
    while ball.moving and round(stepSize) > 0:
        # move goalkeeper between goal posts
        goalkeeper.move(goalPosts)   
        goalkeeper.updatePlayer(gkLFootIndex, gkBodyIndex)
        # all players' current rotations
        playerRots = goalkeeper.getRotation(), striker.getRotation()
        # point right between each player's feet
        feetMidpoints = (goalkeeper.getMidpoint(),
                         striker.getMidpoint())
        if ball.checkGoal(goalPosts):   # ball in goal
            ball.inGoal = True
        # move ball
        ball.move(stepSize, goalPosts, numPlayers, playerRots,
                  feetMidpoints, minDist)
        # new step size
        stepSize = math.sqrt(ball.stepX**2+ball.stepY**2)   
    
pygame.init()   # start pygame

pygame.display.set_caption('My First Game')   # game title
screenSize = 500, 500   # screen size

# create objects that will appear on the screen
bg = nonplayer.Background(screenSize)
goal = nonplayer.Goal(screenSize)
goalkeeper = player.Goalkeeper(screenSize)
striker = player.Outfielder(screenSize)
ball = nonplayer.Ball(screenSize)

# load objects into pygame
bg.load('grass')
goal.load('goalLeft', 'goalMiddle', 'goalRight')
goalkeeper.load('playerFoot', 'playerBody')
striker.load('playerFoot', 'playerBody')
ball.load('ball')

# draw the objects onto the screen
bg.blit()
goal.blit()
goalkeeper.blitFeet(rotate=-180)
striker.blitFeet()
ball.blit()
goalkeeper.blitBody(rotate=-180)
striker.blitBody()

goalPosts = goal.getPosts()   # x-coordinates and size of the goal posts

numPlayers = 2   # number of players
gkStartSpeed = goalkeeper.speed   # goalkeeper's initial speed
    
allThings = []   # list of everything on the screen
allPos = []   # list of those things' positions
# add to the lists
bg.addToLists(allThings, allPos, 'pos', numPlayers)
goal.addToLists(allThings, allPos, 'getPos', numPlayers)
ball.addToLists(allThings, allPos, 'getStartPos', numPlayers)
goalkeeper.addToLists(allThings, allPos, 'getStartPos', numPlayers)
allThings, allPos = striker.addToLists(allThings, allPos, 'getStartPos',
                                       numPlayers)
# turn the lists into class attributes
ball.getLists(allThings, allPos)
goalkeeper.getLists(allThings, allPos)
striker.getLists(allThings, allPos)

# indexes of the striker's left foot and of his body in the lists
strikerLFootIndex = allThings.index(striker.lFoot)
strikerBodyIndex = allThings.index(striker.body)
# indexes of the striker's left foot and of his body in the lists
gkLFootIndex = allThings.index(goalkeeper.lFoot)
gkBodyIndex = allThings.index(goalkeeper.body)

bg.frame   # initialize clock

playing = True
while playing:
    # process events in the game one by one
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            pygame.quit()
            sys.exit()   # prevents getting an error message when quitting

    striker.moved = False
    ball.inGoal = False

    pressedKeys = pygame.key.get_pressed()
    # process keys used for the striker's movements
    pressed, direction, moveType = bg.processMoveKeys(pressedKeys)
    if pressed in bg.moveKeys:
        # one of the movement keys has been pressed
        striker.move(moveType, direction, ball.center, ball.getCenterPos())
    if pressedKeys[pygame.K_s] == 1:
        # 's' key has been pressed --> player will kick the ball
        goalkeeper.kickBall(ball.getCenterPos(), ball.center, gkLFootIndex)
        striker.kickBall(ball.getCenterPos(), ball.center, ball.gkCaught,
                         strikerLFootIndex)
        # The ball will move if the foot touches it.
        if goalkeeper.touchedBall or striker.touchedBall:
            # nearest distance to the player that the ball can get
            minDist = ball.center[1] + striker.bodyCenterStart[1] - 3
            if goalkeeper.touchedBall:   # goalkeeper kicks the ball
                goalkeeper.speed = gkStartSpeed   # resets goalkeeper's speed
                # angle (measured in degrees) of the body with respect to the
                # y-axis pointing down from the ball
                bodyAngle = goalkeeper.getBodyAngle(ball.getCenterPos())
                # process movements of the ball and of the goalkeeper
                processMovements()
            else:   # striker kicks the ball
                # angle (measured in degrees) of the body with respect to the
                # y-axis pointing down from the ball
                bodyAngle = striker.getBodyAngle(ball.getCenterPos())
                # process movements of the ball and of the goalkeeper
                processMovements()
                if ball.gkCaught:   # goalkeeper has the ball
                    goalkeeper.speed = 0
                    # goalkeeper kicks the ball back
                    goalkeeper.kickBall(ball.getCenterPos(), ball.center,
                                        gkLFootIndex)
                    if goalkeeper.touchedBall:
                        # reset goalkeeper's speed
                        goalkeeper.speed = gkStartSpeed   
                        # angle (measured in degrees) of the body with respect
                        # to the y-axis pointing down from the ball
                        bodyAngle = goalkeeper.getBodyAngle(ball.getCenterPos())
                        # process movements of the ball and of the goalkeeper
                        processMovements()
                        
    # If in goal, the ball will be return to its original position after it has
    # stopped moving.
    if ball.inGoal:
        ball.resetBall()
        goalkeeper.speed = gkStartSpeed   # resets goalkeeper's speed

    goalkeeper.move(goalPosts)   # moves goalkeeper between goal posts
    goalkeeper.updatePlayer(gkLFootIndex, gkBodyIndex)   # updates player
                
    if striker.moved:
        # update player
        striker.updatePlayer(strikerLFootIndex, strikerBodyIndex)

    bg.updateDisplay()   # updates display to show changes
