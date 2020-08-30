'''This is the main program for the first version of a mini-game of football/
soccer in PyGame.'''

import pygame, sys, random
import ClassesForMyFirstGame as game

pygame.init()   # start pygame

pygame.display.set_caption('My First Game')   # game title
screenSize = 550, 700   # screen size

# create objects that will appear on the screen
bg = game.Background(screenSize)
goal = game.Goal(screenSize)
player = game.Player(screenSize)
ball = game.Ball(screenSize)

# draw the objects onto the screen
bg.blit('grass')
goal.blit('goalLeft', 'goalMiddle', 'goalRight')
player.blit('playerFoot', 'playerBody', 'feet')
ball.blit('ball')
player.blit('playerFoot', 'playerBody', 'body')

# x-coordinates and size of the goal posts
goalPosts = goal.getPosts()

# list of everything on the screen
allThings = [bg.grass, goal.left, goal.middle, goal.right, player.lFoot,
             player.rFoot, ball.ball, player.body]
# list of the positions of everything on the screen
allPos = [bg.pos] + goal.getPos() + player.getPos()
allPos.insert(-1, ball.getPos())
    
bg.frame   # initialize clock

playing = True
while playing:
    # process events in the game one by one
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            pygame.quit()
            sys.exit()   # prevents getting an error message when quitting the game

    player.moved = False
    pressedKeys = pygame.key.get_pressed()
    # process keys used for player movements
    pressed, direction, moveType = bg.processMoveKeys(pressedKeys)
    if pressed in bg.moveKeys:
        # one of the keys used for player movements has been pressed
        player.move(moveType, direction, ball.center, ball.getCenterPos())
    if pressedKeys[pygame.K_s] == 1:
        # 's' key has been pressed --> player will kick the ball
        # choose the foot that will kick the ball
        player.kickBall(ball.getCenterPos(), ball.center, allThings, allPos)
        if player.touchedBall:
            # foot has touched the ball --> ball will move
            # nearest distance to the player that the ball can get
            minDist = ball.center[1] + player.bodyCenterStart[1] + \
                      player.feetOut - 5
            # move ball
            ball.moveBall(
                player.getBodyAngle(ball.getCenterPos()), random.uniform(28,32),
                goalPosts, player.getRotation(), player.getMidpoint(), minDist,
                allThings, allPos, pressedKeys)
            
    if player.moved:
        player.updatePlayer(allThings, allPos)
    bg.updateDisplay()
