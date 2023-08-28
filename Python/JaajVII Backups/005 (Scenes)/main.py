import pygame, sys
from info import *
from player import Player
from game_instance import *
from pygame.math import Vector2


pygame.init()
pygame.display.set_caption(window_name)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((int(window_size.x),int(window_size.y)))

game = Game(screen)

t = 1
# deltaTime in seconds.
deltaTime = 1
getTicksLastFrame = 1

while True:
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

    t = pygame.time.get_ticks()
    # deltaTime in seconds.
    game.current_scene.deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t


    #update method is called here
    game.current_scene.update()

    #screen.fill(pygame.Color(bg_color))
    #render method is called here
    game.current_scene.render()

    pygame.display.update()
    clock.tick(framerate)
