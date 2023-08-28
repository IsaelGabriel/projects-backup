import pygame
from pygame.math import Vector2
from info import import_image,window_size

class Map:
    def __init__(self,src,coll_src,surface,multiplier):
        self.src = import_image(coll_src,multiplier)
        self.coll_img = import_image(coll_src,1)
        self.surface = surface
        self.multiplier = multiplier
        self.coll_list = []
        self.custom_surface = pygame.Surface((self.src.get_width(),self.src.get_height()),0,surface)
        self.custom_surface.set_colorkey((0,0,0))

        coll_px = pygame.PixelArray(self.custom_surface)
        bl = False
        for x in range(0,self.coll_img.get_width()):
            for y in range(0,self.coll_img.get_height()):
                if self.coll_img.get_at((x,y)) == (255,255,255):
                            self.coll_list.append(Vector2(x,y))




    def render(self):
        #rect = pygame.Rect(0,0,window_size.x,window_size.y)
        # self.surface.blit(self.src,self.custom_surface)
        self.custom_surface.fill((0,0,0))

        rect = self.custom_surface.get_rect()
        self.custom_surface.blit(self.src,rect)
        self.surface.blit(self.custom_surface,rect)
