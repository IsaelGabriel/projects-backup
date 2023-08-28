import pygame
from pygame.math import Vector2
from abc import ABC,abstractmethod
from math import sqrt
from info import window_size

obj_list = []

class Entity(ABC):
    def __init__(self,id,rect):
        self.id = id
        self.rect = rect
        self.collision = 'on'


    @abstractmethod
    def render(self,camera):
        pass

class MovableEntity(Entity):
    def __init__(self,id,rect):
        super().__init__(id,rect)
        self.pos = self.rect.center
        self.velocity = (0,0)
        self.delta_velocity = (0,0)
        #self.resistance = 10
        # gravity
        self.gravity_on = False
        self.gravity = (0,0)
        self.mass = 1
        # max vel
        self.max_vel = 70

    @abstractmethod
    def custom_update(self): pass

    def update(self):
        self.custom_update()
        self.set_delta_velocity()
        self.apply_velocity()

    def set_delta_velocity(self):
        if self.velocity[0] > self.max_vel: self.velocity = (self.max_vel,self.velocity[1])
        if self.velocity[1] > self.max_vel: self.velocity = (self.velocity[0], self.max_vel)
        vel = (self.velocity[0]*self.deltaTime,self.velocity[1]*self.deltaTime)
        distance = sqrt(vel[0]**2 + vel[1]**2)
        mult = (10**2)
        for d in range(1,int(distance*mult)+1):
            # make an enlarged rect and check if it collides with another objects enlarged rect
            rect_pos = [self.pos[0],self.pos[1]]
            for i in range(0,2):
                if vel[i] != 0 and d != 0 and distance != 0:
                    rect_pos[i] += ((d*(vel[i]*mult))/(distance*mult))*vel[i]
            rect_size = (self.rect.w*mult,window_size[1]*mult)#self.rect.h*mult)
            rect = pygame.Rect((0,0),rect_size)
            rect.center = (rect_pos[0],rect_pos[1])
            # check for collision
            for obj in obj_list:
                if obj != self:
                    obj_pos = (obj.rect.centerx*mult,obj.rect.centery*mult)
                    if hasattr(obj, 'pos'): obj_pos = (obj.pos[0]*mult,obj.pos[0]*mult)
                    obj_size = (obj.rect.w*mult,obj.rect.h*mult)
                    obj_rect = pygame.Rect((0,0),obj_size)
                    obj_rect.center = obj_pos
                    if rect.colliderect(obj_rect):
                        print(d)
                        nd = d/mult
                        x = 0
                        y = 0
                        if vel[0] != 0 and d != 0: x = (((nd-1)*vel[0])/distance)/vel[0]
                        if vel[1] != 1 and d != 0: y = (((nd-1)*vel[1])/distance)/vel[1]
                        self.delta_velocity = (x,y)
        self.delta_velocity = vel
        return

    def apply_velocity(self):
        if self.velocity != (0,0):
            new_pos = [self.pos[0],self.pos[1]]
            for i in range(0,2): new_pos[i] += self.delta_velocity[i]
            self.pos = (new_pos[0],new_pos[1])
            self.rect.center = (self.pos[0],self.pos[1])

    def add_force(self,f):
        new_vel = [self.velocity[0],self.velocity[1]]
        for i in range(0,2):
            v = new_vel[i]
            v += f[i]*self.mass*self.deltaTime
            if v <= f[i]: new_vel[i] = v
        self.velocity = (new_vel[0],new_vel[1])

    def get_collision_list(self,mult):
        c_list = []
        rect_pos = {
            'up' : (self.pos[0],(self.pos[1]-(self.rect.size[1]/2))-1),
            'down' : (self.pos[0],self.pos[1]+(self.rect.size[1]/2)),
            'left': ((self.pos[1]-(self.rect.size[0]/2))-1,self.pos[1]),
            'right' : (self.pos[1]+(self.rect.size[0]/2),self.pos[1])
        }
        rect = dict()
        for key in rect_pos.keys():
            size = (self.rect.w*mult,mult)
            if key in 'updown': size = (mult,self.rect.h)
            rect[key] = pygame.Rect((rect_pos[key][0]*mult,rect_pos[key][1]*mult),size)
        # check for collision
        for i in range(0,len(obj_list)):
            obj = obj_list[i]
            if obj != self:
                obj_pos = (obj.rect.center[0]*mult,obj.rect.center[1]*mult)
                if hasattr(obj, 'pos'): obj_pos = (obj.pos[0]*mult,obj.pos[0]*mult)
                obj_size = (obj.rect.w*mult,obj.rect.h*mult)
                obj_rect = pygame.Rect(obj_pos,obj_size)
                for key in rect_pos.keys():
                    if rect[key].colliderect(obj_rect):
                        c_list.append(Collision(i,rect_pos[key],key))
        return c_list

    @abstractmethod
    def render(self,camera): pass

class OMovableEntity(Entity):
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

    def add_velocity(self,index,value):
        v = [0,0]
        v[index] = 1
        self.velocity = (self.velocity[0]+(value*v[0]),self.velocity[1]+(value*v[1]))

class Solid(Entity):
    def render(self,camera): camera.draw_rect((100,100,200),self.rect.topleft,self.rect.size)

class Trap(Entity):
    def __init__(self,id,rect):
        super().__init__(id,rect)
        self.collision = 'trigger'

    def render(self,camera): camera.draw_rect(pygame.Color('red'),self.rect.topleft,self.rect.size)

class Collision():
    def __init__(self,obj_index,pos,dir):
        self.obj_index = obj_index
        self.pos = pos
        self.dir = dir
