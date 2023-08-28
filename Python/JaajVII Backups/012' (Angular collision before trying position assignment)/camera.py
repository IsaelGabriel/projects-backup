import pygame
from pygame.math import Vector2
from info import window_scale,window_size

class Camera:
    def __init__(self,screen):
        self.screen = screen
        self.rect = pygame.Rect((0,0),(window_size[0]*window_scale,window_size[1]*window_scale))
        self.rect.center = (0,0)

    def blit(self,src,pos,size):
        rect = pygame.Rect((0,0),(size[0]*window_scale,size[1]*window_scale))
        rect.center = ((pos[0]+window_size[0]/2)*window_scale,(pos[1]+window_size[1]/2)*window_scale)
        if self.rect.colliderect(rect):
            rect.x = rect.x -self.rect.x
            rect.y = rect.y -self.rect.y
            self.screen.blit(src,rect)

    def draw_rect(self,color,pos,size):
        rect = pygame.Rect((0,0),(size[0]*window_scale,size[1]*window_scale))
        final_pos = [pos[0]*window_scale,pos[1]*window_scale]
        rect.center = (final_pos[0],final_pos[1])
        #if self.rect.colliderect(pygame.Rect(5,5)))
        if self.rect.colliderect(rect):
            rect.centerx -= (self.rect.centerx-(window_size[0]*window_scale))/2
            rect.centery -= (self.rect.centery-(window_size[1]*window_scale))/2
            pygame.draw.rect(self.screen,color,rect)
        #self.dr((0,0,0),(10,10))
        
    def dr(self,color,size):
        rc = pygame.Rect((0,0),(size[0]*window_scale,size[1]*window_scale))
        rc.center = (0,0)
        pygame.draw.rect(self.screen,color,rc)

    def get_position(self):
        return (self.rect.centerx/window_scale,self.rect.centery/window_scale)
    
    def set_position(self,position):
        self.rect.center = (position[0]*window_scale,position[1]*window_scale)