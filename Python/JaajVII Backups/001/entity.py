import pygame
from abc import ABC,abstractmethod

class Entity(ABC):
    def __init__(self,id, pos, size,surface, coll_enabled, coll_ignore):
        self.id = id
        self.pos = pos
        self.size = size
        self.surface = surface
        self.coll_enabled = coll_enabled
        self.coll_ignore = coll_ignore
        
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def get_collision(self,c_obj,c_pos):
        pass

    @abstractmethod
    def collision_stay(self,c_obj,c_pos):
        pass

    @abstractmethod
    def collision_exit(self,c_obj,c_pos):
        pass

    def render_base_rect(self,color):
        rect = pygame.Rect(int(self.pos.x),int(self.pos.y),int(self.size.x),int(self.size.y))
        pygame.draw.rect(self.surface,color,rect)
