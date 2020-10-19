'''This is the main program for the third version of a mini-game of football/
soccer in PyGame. Compared to the previous versions, this version enables the
outfielder to move in any direction using only the arrow keys.'''

import pygame, sys, random, math
import NonplayerClasses as np
import PlayerClasses as pl

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
goalkeeper.blitFeet()
striker.blitFeet()
ball.blit()
goalkeeper.blitBody()
striker.blitBody()

players = goalkeeper, striker

# list of everything on the screen
allThings = bg.things + goal.things
for player in players:
    allThings += player.things[:2]   # player's feet
allThings += ball.things
for player in players:
    allThings.append(player.things[2])   # player's body

# list of those things' positions at the start of the program
allPos = [bg.pos] + goal.getPos()
for player in players:
    allPos += player.getStartPos()[:2]   # player's feet
allPos += ball.getStartPos()
for player in players:
    allPos.append(player.getStartPos()[2])   # player's body

# turn the lists into class attributes
for thing in (ball,) + players:
    thing.allThings, thing.allPos = allThings, allPos

gkStartSpeed = goalkeeper.speed   # goalkeeper's initial speed

while True:
    # process events in the game
    for event in pygame.event.get():
        pressedKeys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or pressedKeys[pygame.K_ESCAPE] or \
           (pressedKeys[pygame.K_LCTRL] and pressedKeys[pygame.K_w]):
            pygame.quit()
            sys.exit()   # prevent getting an error message when quitting
                
    pressedKeys = pygame.key.get_pressed()
    moveType, direction = bg.processMoveKeys(pressedKeys)    
    if moveType != None:
        striker.move(moveType, direction, ball)
    if pressedKeys[pygame.K_s]:
        goalkeeper.kickBall(ball, gk=True)
        striker.kickBall(ball)
        if goalkeeper.touchedBall:
            goalkeeper.speed = gkStartSpeed   # reset
            ball.gkCaught = False
            bg.processMovements(ball, goal, players)
        elif striker.touchedBall:
            bg.processMovements(ball, goal, players)
            if ball.gkCaught:   # ball caught by goalkeeper
                goalkeeper.speed = 0
                goalkeeper.kickBall(ball, gk=True)
                if goalkeeper.touchedBall:
                    print('gk kicks ball back')
                    goalkeeper.speed = gkStartSpeed   # reset
                    ball.gkCaught = False   # reset
                    bg.processMovements(ball, goal, players)
                        
    goalkeeper.moveAcross(goal)
    goalkeeper.updateAll()
    if striker.moved:
        striker.updateAll()
    players = goalkeeper, striker
    
    bg.updateDisplay()
