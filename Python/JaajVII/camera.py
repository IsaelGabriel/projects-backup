import pygame
from pygame.math import Vector2
from info import window_scale,window_size,get_bounds

class Camera:
    def __init__(self,screen,map_size):
        self.screen = screen
        self.pos = (0,0)
        self.map_size = map_size

    def blit(self,src,pos,size):
        #self.fix_pos()
        if self.get_collision(pos,size):
            rect = pygame.Rect(0,0,size[0]*window_scale,size[1]*window_scale)
            final_pos = [pos[0]*window_scale,pos[1]*window_scale]
            rect.center = (final_pos[0],final_pos[1])
            rect.centerx -= (self.pos[0]-(window_size[0])/2)*window_scale
            rect.centery -= (self.pos[1]-(window_size[1])/2)*window_scale
            self.screen.blit(src,rect)

    def draw_rect(self,color,pos,size):
        #self.fix_pos()
        #if self.rect.colliderect(pygame.Rect(5,5)))
        if self.get_collision(pos,size):
            rect = pygame.Rect((0,0),(size[0]*window_scale,size[1]*window_scale))
            final_pos = [pos[0]*window_scale,pos[1]*window_scale]
            rect.center = (final_pos[0],final_pos[1])
            rect.centerx -= (self.pos[0]-(window_size[0])/2)*window_scale
            rect.centery -= (self.pos[1]-(window_size[1])/2)*window_scale
            pygame.draw.rect(self.screen,color,rect)
        #self.dr((0,0,0),(10,10))

    def get_position(self):
        return self.pos
    
    def set_position(self,position):
        new_pos = [position[0],position[1]]
        if new_pos[0] - window_size[0]/2 < -self.map_size[0]/2:
            new_pos[0] = -self.map_size[0]/2 + window_size[0]/2
        elif new_pos[0] + window_size[0]/2 > self.map_size[0]/2:
            new_pos[0] = self.map_size[0]/2 - window_size[0]/2

        if new_pos[1] - window_size[1]/2 < -self.map_size[1]/2:
            new_pos[1] = -self.map_size[1]/2 + window_size[1]/2
        elif new_pos[1] + window_size[1]/2 > self.map_size[1]/2:
            new_pos[1] = self.map_size[1]/2 - window_size[1]/2
        self.pos = (new_pos[0],new_pos[1])

    def get_collision(self,o_pos,o_size):
        s_bounds = get_bounds(self.pos,window_size)
        s_min = s_bounds['min']
        s_max = s_bounds['max']
       
        o_bounds = get_bounds(o_pos,o_size)
        o_min = o_bounds['min']
        o_max = o_bounds['max']

        if not (s_min[0] < s_max[0] <= o_min[0] < o_max[0]) and  not (o_min[0] < o_max[0] <= s_min[0] < s_max[0]):
            if not (s_min[1] < s_max[1] <= o_min[1] < o_max[1]) and not (o_min[1] < o_max[1] <= s_min[1] < s_max[1]):
                return True
        
        return False