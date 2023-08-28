import pygame, sys
from info import *
from player import Player
from pygame.math import Vector2

pygame.init()
pygame.display.set_caption(window_name)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((int(window_size.x),int(window_size.y)))

player = Player("Player",Vector2(10,20),Vector2(50,50),screen,True,None)
player.start()

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
            print (pygame.key.name(event.key))
            for key in keys.keys():
                if key == pygame.key.name(event.key):
                    keys[key] = True
        if event.type == pygame.KEYUP:
            for key in keys.keys():
                if key == pygame.key.name(event.key):
                    keys[key] = False


    #update method is called here
    player.update()

    screen.fill(pygame.Color(bg_color))
    #render method is called here
    player.render()

    pygame.display.update()
    clock.tick(framerate)
