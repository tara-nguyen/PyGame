'''This is the main program for the third version of a mini-game of football/
soccer in PyGame. Compared to the previous versions, this version enables the
outfielder to move in any direction using only the arrow keys.'''

import pygame, sys, random, math
import NonplayerClasses as np
import PlayerClasses as pl

def processMovements():
    '''This function processes the movements of the ball and of the goalkeeper
    while the ball is moving.'''
    # angle (measured in degrees) of the body with respect to the
    # y-axis pointing downward
    if goalkeeper.touchedBall:
        bodyAngle = goalkeeper.getBodyAngle(ball)
    elif striker.touchedBall:
        bodyAngle = striker.getBodyAngle(ball)
    # angle (measured in degrees) at which the ball will move, with
    # respect to the y-axis pointing up from the current ball center
    ball.setMovingAngle(random.uniform(bodyAngle-.5, bodyAngle+.5))
    # initial step size of the ball
    stepSize = random.uniform(18, 22)
    ball.setFirstStep(stepSize)
    ball.moving = True
    while ball.moving and round(stepSize) > 0:
        # move goalkeeper between goal posts
        goalkeeper.move(goal.getPosts())   
        goalkeeper.updatePlayer(gkLFootIndex, gkBodyIndex)
        if ball.checkGoal(goal.getPosts()):   # ball in goal
            ball.inGoal = True
        # move ball
        ball.move(stepSize, goal.getPosts(), (goalkeeper,striker), minDist)
        # new step size
        stepSize = math.sqrt(ball.stepX**2 + ball.stepY**2)   
    
pygame.init()   # start pygame

pygame.display.set_caption('My First Game')   # game title
screenSize = 500, 500   # screen size

# create objects that will appear on the screen
bg = np.Background(screenSize)
goal = np.Goal(screenSize)
goalkeeper = pl.Goalkeeper(screenSize)
striker = pl.Outfielder(screenSize)
ball = np.Ball(screenSize)

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

numPlayers = 2   # number of players
gkStartSpeed = goalkeeper.speed   # goalkeeper's initial speed

# list of everything on the screen
allThings = bg.things + goal.things
for player in (goalkeeper, striker):
    allThings += player.things[:2]   # player's feet
allThings += ball.things
for player in (goalkeeper, striker):
    allThings.append(player.things[2])   # player's body

# list of those things' positions
allPos = [bg.pos] + goal.getPos()
for player in (goalkeeper, striker):
    allPos += player.getStartPos()[:2]   # player's feet
allPos += ball.getStartPos()
for player in (goalkeeper, striker):
    allPos.append(player.getStartPos()[2])   # player's body

# turn the lists into class attributes
for thing in (ball, goalkeeper, striker):
    thing.allThings, thing.allPos = allThings, allPos

# indexes of the striker's left foot and of his body in the lists
strikerLFootIndex = allThings.index(striker.lFoot)
strikerBodyIndex = allThings.index(striker.body)
# indexes of the striker's left foot and of his body in the lists
gkLFootIndex = allThings.index(goalkeeper.lFoot)
gkBodyIndex = allThings.index(goalkeeper.body)

bg.frame   # initializes clock

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
    moveType, direction = bg.processMoveKeys(pressedKeys)
    if moveType != None:
        striker.move(moveType, direction, ball)
    if pressedKeys[pygame.K_s] == 1:
        goalkeeper.kickBall(ball, gkLFootIndex, gk=True)
        striker.kickBall(ball, strikerLFootIndex)
        # The ball will move if the foot touches it.
        if goalkeeper.touchedBall or striker.touchedBall:
            # nearest distance to the player that the ball can get
            minDist = ball.center[1] + striker.bodyStartCenter[1]
            if goalkeeper.touchedBall:
                goalkeeper.speed = gkStartSpeed   # resets goalkeeper's speed
                processMovements()   # ball movement and goalkeeper movement
            else:
                processMovements()   # ball movement and goalkeeper movement
                if ball.gkCaught:   # goalkeeper has the ball
                    goalkeeper.speed = 0
                    # goalkeeper kicks the ball back
                    goalkeeper.kickBall(ball, gkLFootIndex, gk=True)
                    if goalkeeper.touchedBall:
                        # reset goalkeeper's speed
                        goalkeeper.speed = gkStartSpeed 
                        processMovements() # ball movement & goalkeeper movement
                        
    # If in goal, the ball will be return to its original position after it has
    # stopped moving.
    if ball.inGoal:
        ball.resetBall()
        goalkeeper.speed = gkStartSpeed   # resets goalkeeper's speed

    goalkeeper.move(goal.getPosts())   # moves goalkeeper between goal posts
    goalkeeper.updatePlayer(gkLFootIndex, gkBodyIndex)   # updates player
                
    if striker.moved:
        # update player
        striker.updatePlayer(strikerLFootIndex, strikerBodyIndex)

    bg.updateDisplay()   # updates display to show changes
