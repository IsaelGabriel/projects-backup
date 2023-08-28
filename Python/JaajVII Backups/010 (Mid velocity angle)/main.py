import pygame, sys
from info import *
from game_instance import *
from pygame.math import Vector2
from pygame.locals import FULLSCREEN, DOUBLEBUF

pygame.init()
pygame.display.set_caption(window_name)
clock = pygame.time.Clock()


flags = DOUBLEBUF
screen = pygame.display.set_mode((int(window_size.x),int(window_size.y)),flags,16)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

t = 0
getTicksLastFrame = 0
deltaTime = 0

game = Game(screen)

while 1:
    t = pygame.time.get_ticks()
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t

    pressed_keys = False
    for key in pygame.key.get_pressed():
        if key: pressed_keys = True
    if pressed_keys == False:
        for key in keys.keys(): keys[key] = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            for key in keys.keys():
                if key == pygame.key.name(event.key):
                    keys[key] = (event.type == pygame.KEYDOWN)

    #update method is called here
    game.deltaTime = deltaTime
    if game.ready: game.update()

    screen.fill(pygame.Color(bg_color))
    #render method is called here
    if game.ready: game.render()

    pygame.display.update()
    clock.tick(60)
