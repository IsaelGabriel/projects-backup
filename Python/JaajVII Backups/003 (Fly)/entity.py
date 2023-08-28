import pygame
from pygame.math import Vector2
from abc import ABC,abstractmethod
from info import window_scale

class Entity(ABC):
    def __init__(self,id, pos, size,surface, coll_enabled, coll_ignore):
        self.id = id
        self.pos = pos
        self.size = size
        self.surface = surface
        self.coll_enabled = coll_enabled
        self.coll_ignore = coll_ignore

    @abstractmethod
    def start(self,scene):
        pass

    @abstractmethod
    def update(self,scene):
        pass

    @abstractmethod
    def render(self):
        pass

    def render_base_rect(self,color):
        rect = pygame.Rect(int(self.pos.x*window_scale),int(self.pos.y*window_scale),int(self.size.x*window_scale),int(self.size.y*window_scale))
        pygame.draw.rect(self.surface,color,rect)

    def get_collision_rect(self,id):
        rect_pos = Vector2(self.pos.x,self.pos.y)
        rect_size = Vector2(1,1)
        if rect_pos == "bottom":
            rect_pos.y += 1 + self.size.y
            rect_size.x = self.size.x
        elif id == "top":
            rect_pos.y -= 1
            rect_size.x = self.size.x
        elif id == "left":
            pos.x -= 1
            rect_size.y = self.size.y
        elif id == "right":
            rect_pos.x += self.size.x + 1
            rect_size.y = self.size.y
        elif id == "normal":
            rect_pos = Vector2(self.pos.x,self.pos.y)
            rect_size = Vector2(self.size.x,self.size.y)
        else:
            rect_pos.x -= 1
            rect_pos.y -= 1
            rect_size.x += 2
            rect_size.y += 2

        return pygame.Rect(rect_pos.x,rect_pos.y,rect_size.x,rect_size.y)


class Solid(Entity):
    def start(self,scene):
        pass

    def update(self,scene):
        pass


    def render(self):
        self.render_base_rect((100,100,200))
