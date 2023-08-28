import pygame
from pygame.math import Vector2

class Camera:
        def __init__(self,screen,map_size,win_size,bg_color):
            self.screen = screen
            self.map_size = map_size
            self.pos = Vector2(0,0)
            self.surface = pygame.Surface(self.map_size)
            self.win_size = win_size
            self.bg_color = bg_color

        def render(self):
            #self.surface.convert_alpha()
            rect = pygame.Rect(-self.pos,self.win_size)
            self.screen.blit(self.surface,rect)
            self.surface.fill(pygame.Color(self.bg_color))

        def blit(self,src):
            rect = src.get_rect()
            s_rect = pygame.Rect(self.pos,self.win_size)
            if s_rect.colliderect(rect): self.surface.blit(src,rect)

        def draw_rect(self,color,rect):
            s_rect = pygame.Rect(self.pos,self.win_size)
            if s_rect.colliderect(rect):
                pygame.draw.rect(self.surface,color,rect)
                self.surface.convert_alpha()

        def draw_transparent_rect(self,color,rect):
            s_rect = pygame.Rect(self.pos,self.win_size)
            if s_rect.colliderect(rect):
                s = pygame.Surface(rect.size)  # the size of your rect
                s.set_alpha(color.a)                # alpha level
                s.fill(color)           # this fills the entire surface
                self.surface.blit(s,rect)
