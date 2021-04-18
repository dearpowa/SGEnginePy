import pygame, sys

from pygame.locals import *

 

pygame.init()

 

FPS = 30 # frames per second setting

fpsClock = pygame.time.Clock()

 

# set up the window

DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)

pygame.display.set_caption('Animation')

 

WHITE = (255, 255, 255)

spriteImg = pygame.image.load('simpleguy_small.png')

spritex = 10

spritey = 10

direction = 'right'

 

while True: # the main game loop

    DISPLAYSURF.fill(WHITE)

 

    if direction == 'right':

        spritex += 5

        if spritex == 280:

            direction = 'down'

    elif direction == 'down':

        spritey += 5

        if spritey == 220:

            direction = 'left'

    elif direction == 'left':

        spritex -= 5

        if spritex == 10:

            direction = 'up'

    elif direction == 'up':

        spritey -= 5

        if spritey == 10:

            direction = 'right'

    DISPLAYSURF.blit(spriteImg, (spritex, spritey))

    for event in pygame.event.get():

        if event.type == QUIT:

            pygame.quit()

            sys.exit()

    pygame.display.update()

    fpsClock.tick(FPS)