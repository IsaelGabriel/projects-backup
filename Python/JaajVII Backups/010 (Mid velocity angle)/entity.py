import pygame
from pygame.math import Vector2
from abc import ABC,abstractmethod
from math import sqrt

obj_list = []

class Entity(ABC):
    def __init__(self,id,rect):
        self.id = id
        self.rect = rect
        self.collision = 'on'
        self.velocity = (0,0)

    @abstractmethod
    def render(self,camera):
        pass

    def get_collision(self,mode,size):
        c_rect = None
        pos = (0,0)
        if mode == 'up':
            pos = (self.rect.left,self.rect.top-size)
        elif mode == 'down':
            pos = (self.rect.left,self.rect.bottom)
        elif mode == 'left':
            pos = (self.rect.left-self.rect.w,self.rect.top)
        elif mode == 'right':
            pos = (self.rect.right,self.rect.top)
        else:
            pos = self.rect.topleft
            pos -= size
            size *= 2
        c_rect = pygame.Rect(pos,(size,size))

        for i in range(0,len(obj_list)):
            if self != obj_list[i]:
                s = str(self.collision) + str(obj_list[i].collision)
                if mode == 'normal':
                    if 'trigger' in s and 'on' in s and 'None' not in s:
                        if self.rect.colliderect(obj_list[i].rect): return i
                elif s == 'onon':
                    if c_rect.colliderect(obj_list[i].rect): return i
        return None

    def get_velocity_axis(self,axis): # x = 0, y = 1
        direction = ['left','right']
        mult = 1
        if axis == 1: direction = ['up','down']
        vel = self.velocity[axis]*self.deltaTime
        if self.velocity[axis] >= 0: direction = direction[1]
        else:
            direction = direction[0]
            mult = -1

        for i in range(0,int(abs(vel)+1)):
            if i == 0:
                if self.get_collision(direction,1) != None:
                    obj = obj_list[self.get_collision(direction,1)]
                    pos = (0,0)
                    new_pos = self.rect.y
                    if direction == 'down':
                        pos = (self.rect.left,self.rect.bottom-1)
                        size = (self.rect.w,1)
                        new_pos  = obj.rect.top
                    elif direction == 'up':
                        pos = (self.rect.left,self.rect.top+1)
                        size = (self.rect.w,1)
                        new_pos = obj.rect.bottom + self.rect.h
                    elif direction == 'right':
                        pos = (self.rect.right-1,self.rect.top)
                        size = (1,self.rect.h)
                        new_pos = obj.rect.left
                    elif direction == 'left':
                        pos = (self.rect.left+1,self.rect.top)
                        size = (1,self.rect.h)
                        new_pos = obj.rect.right + self.rect.w
                    if pygame.Rect(pos,size).colliderect(obj.rect):
                        if direction in 'leftright': self.rect.right = new_pos
                        else: self.rect.bottom = new_pos
                        return 0
            elif self.get_collision(direction,i) != None:
                return (i-1) * mult
        return vel

    def get_velocity(self):
        #direction = [['left','right'],['up','down']]
        vel = self.velocity
        total_distance = sqrt(velocity[0]**2 + velocity[1]**2)
        initial_position = self.rect.topleft
        end_position = (self.rect.center[0]+velocity[0],self.rect.center[1]+velocity[1])

    def add_velocity(self,index,value):
        v = [0,0]
        v[index] = 1
        self.velocity = (self.velocity[0]+(value*v[0]),self.velocity[1]+(value*v[1]))

class Solid(Entity):
    def render(self,camera): camera.draw_rect((100,100,200),self.rect)

class Trap(Entity):
    def __init__(self,id,rect):
        super().__init__(id,rect)
        self.collision = 'trigger'

    def render(self,camera): camera.draw_rect((255,0,0),self.rect)
