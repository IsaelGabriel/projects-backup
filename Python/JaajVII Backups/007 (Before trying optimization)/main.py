import pygame, sys
from info import *
from player import Player
from game_instance import *
from pygame.math import Vector2
from pygame.locals import FULLSCREEN, DOUBLEBUF


pygame.init()
pygame.display.set_caption(window_name)
clock = pygame.time.Clock()


flags = DOUBLEBUF
screen = pygame.display.set_mode((int(window_size.x),int(window_size.y)),flags,16)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

game = Game(screen)

while 1:
    pressed_keys = False
    for key in pygame.key.get_pressed():
        if key: pressed_keys = True
    if pressed_keys == False:
        for key in keys.keys(): keys[key] = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            for key in keys.keys():
                if key == pygame.key.name(event.key):
                    keys[key] = True
        if event.type == pygame.KEYUP:
            for key in keys.keys():
                if key == pygame.key.name(event.key):
                    keys[key] = False


    #update method is called here
    if game.ready: game.update()

    #screen.fill(pygame.Color(bg_color))
    #render method is called here
    if game.ready: game.render()

    pygame.display.update([game.camera.surface.get_rect()])
    clock.tick(40)
