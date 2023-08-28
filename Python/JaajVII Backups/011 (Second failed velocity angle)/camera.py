import pygame
from pygame.math import Vector2
from info import window_scale

class Camera:
    def __init__(self,screen,size):
        self.screen = screen
        self.rect = pygame.Rect((0,0),(size[0]*window_scale,size[1]*window_scale))

    def blit(self,src,pos,size):
        if self.rect.colliderect(rect):
            rect.x = rect.x -self.rect.x
            rect.y = rect.y -self.rect.y
            self.screen.blit(src,rect)

    def draw_rect(self,color,pos,size):
        rect = pygame.Rect((0,0),(size[0]*window_scale,size[1]*window_scale))
        if isinstance(pos[0], float) or isinstance(pos[0], float): rect.center = (pos[0]*window_scale,pos[1]*window_scale)
        else: rect.topleft = (pos[0]*window_scale,pos[1]*window_scale)
        if self.rect.colliderect(rect):
            rect.topleft = (int(rect.left - self.rect.left),int(rect.top - self.rect.top))
            pygame.draw.rect(self.screen,color,rect)
