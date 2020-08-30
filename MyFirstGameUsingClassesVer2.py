'''This is the main program for the second version of a mini-game of football/
soccer in PyGame. Compared to the first version, this version adds a goalkeeper.'''

import pygame, sys, random
import NonplayerClasses as nonplayer
import PlayerClasses as player

pygame.init()   # start pygame

pygame.display.set_caption('My First Game')   # game title
screenSize = 400, 500   # screen size

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

# x-coordinates and size of the goal posts
goalPosts = goal.getPosts()

# list of everything on the screen
allThings = [bg.grass, goal.left, goal.middle, goal.right, goalkeeper.lFoot,
             goalkeeper.rFoot, striker.lFoot, striker.rFoot, ball.ball,
             goalkeeper.body, striker.body]
# list of the positions of everything on the screen
allPos = [bg.pos] + goal.getPos() + goalkeeper.getStartPos()[:2] + \
         striker.getStartPos()[:2] + [ball.getStartPos()] + \
         [goalkeeper.getStartPos()[2]] + [striker.getStartPos()[2]]
# indexes of the striker's left foot and of his body
strikerLFootIndex = allThings.index(striker.lFoot)
strikerBodyIndex = allThings.index(striker.body)
    
bg.frame   # initialize clock

playing = True
while playing:
    # process events in the game one by one
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            pygame.quit()
            sys.exit()   # prevents getting an error message when quitting the game

    striker.moved = False
    pressedKeys = pygame.key.get_pressed()
    # process keys used for player movements
    pressed, direction, moveType = bg.processMoveKeys(pressedKeys)
    if pressed in bg.moveKeys:
        # one of the keys used for player movements has been pressed
        striker.move(moveType, direction, ball.center, ball.getCenterPos())
    if pressedKeys[pygame.K_s] == 1:
        # 's' key has been pressed --> striker will kick the ball
        # choose the foot that will kick the ball
        striker.kickBall(ball.getCenterPos(), ball.center,
                         allThings, allPos, strikerLFootIndex)
        if striker.touchedBall:
            # foot has touched the ball --> ball will move
            # nearest distance to the player that the ball can get
            minDist = ball.center[1] + striker.bodyCenterStart[1] + \
                      striker.feetOut - 3
            # move ball
            ball.moveBall(
                striker.getBodyAngle(ball.getCenterPos()), random.uniform(18,22),
                goalPosts, striker.getRotation(), striker.getMidpoint(), minDist,
                allThings, allPos, pressedKeys)
            
    if striker.moved:
        striker.updatePlayer(allThings, allPos,
                             strikerLFootIndex, strikerBodyIndex)
    bg.updateDisplay()
