import pygame
from pygame.math import Vector2

class Camera:
    def __init__(self,screen,size):
        self.screen = screen
        self.rect = pygame.Rect((0,0),size)

    def blit(self,src,rect):
        if self.rect.colliderect(rect):
            rect.x = rect.x -self.rect.x
            rect.y = rect.y -self.rect.y
            self.screen.blit(src,rect)

    def draw_rect(self,color,rect):
        if self.rect.colliderect(rect):
            rect.topleft = (int(rect.left - self.rect.left),int(rect.top - self.rect.top))
            pygame.draw.rect(self.screen,color,rect)
