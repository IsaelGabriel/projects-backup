import pygame
from pygame.math import Vector2
from abc import ABC,abstractmethod
from math import sqrt
from info import import_vertical_sprite, window_scale,get_bounds,unit_size

obj_list = []

class Entity(ABC):
    def __init__(self,id,pos,size):
        self.id = id
        self.pos = pos
        self.size = size
        self.collision = 'on'
        self.deltaTime = 0
        self.destroy = False
        self.animator = None

    @abstractmethod
    def render(self,camera):
        pass

   

class PhysicsEntity(Entity):
    def __init__(self,id,pos,size):
        super().__init__(id,pos,size)
        self.velocity = (0,0)
        self.delta_vel = (0,0)

    def update(self):
        self.custom_update()
        #self.apply_velocity()
        #self.fix_position()
        #self.set_velocity()
        vel_x = self.set_vel_axis(0)
        #if vel_x != 0: print(vel_x)
        self.pos = (self.pos[0] + vel_x,self.pos[1])
        vel_y = self.set_vel_axis(1)
        self.pos = (self.pos[0],self.pos[1] + vel_y)

    def set_vel_axis(self,axis):
        dvel = self.velocity[axis] * self.deltaTime
        if dvel == 0 or self.deltaTime == 0: return 0
        new_vel = [self.velocity[0],self.velocity[1]]

        size = [0,0]
        size[int(axis == 0)] = self.size[int(axis == 0)]
        size[axis] = abs(dvel)

        dist = [0,0]
        dist[axis] = dvel+self.size[axis]/2+dvel/2
        if dvel < 0: dist[axis] = dvel -self.size[axis]/2 - dvel/2
        
        coll = self.get_collision((dist[0],dist[1]),(size[0],size[1]))
        if coll != None:
            if obj_list[coll].collision == 'on':
                o_pos = obj_list[coll].pos[axis]
                o_size = obj_list[coll].size[axis]
                new_vel[axis] = 0
                self.velocity = (new_vel[0],new_vel[1])
                n_pos = self.pos[axis]
                if False:
                    if dvel > 0:
                        n_pos =  o_pos - (o_size/2 + self.size[axis]/2)
                        if n_pos == self.pos[axis]:return 0.0
                        if self.pos[axis] > n_pos:
                            new_pos = [self.pos[0],self.pos[1]]
                            new_pos[axis] = n_pos
                            self.pos = (new_pos[0],new_pos[1])
                            return 0.0
                    if dvel < 0:
                        n_pos =  o_pos + (o_size/2 + self.size[axis]/2)
                        if n_pos == self.pos[axis]:return 0.0
                        if self.pos[axis] < n_pos:
                            new_pos = [self.pos[0],self.pos[1]]
                            new_pos[axis] = n_pos
                            self.pos = (new_pos[0],new_pos[1])
                            return 0.0
                if dvel > 0:
                    n_pos =  o_pos - (o_size/2 + self.size[axis]/2)
                    if n_pos == self.pos[axis]:return 0.0
                    if self.pos[axis] != n_pos:
                        new_pos = [self.pos[0],self.pos[1]]
                        new_pos[axis] = n_pos
                        self.pos = (new_pos[0],new_pos[1])
                        return 0.0
                if dvel < 0:
                    n_pos =  o_pos + (o_size/2 + self.size[axis]/2)
                    if n_pos == self.pos[axis]:return 0.0
                    if self.pos[axis] != n_pos:
                        new_pos = [self.pos[0],self.pos[1]]
                        new_pos[axis] = n_pos
                        self.pos = (new_pos[0],new_pos[1])
                        return 0.0
                    
                return n_pos - self.pos[axis]
        if abs(new_vel[axis]) > abs(self.velocity[axis]): new_vel[axis] = self.velocity[axis] 
        self.velocity = (new_vel[0],new_vel[1])
        #if self.velocity[0] != 0: print(self.velocity[0])
        return dvel


    def get_collision(self,distance,size):
        s_pos = (self.pos[0] + distance[0],self.pos[1]+distance[1])
        s_bounds = get_bounds(s_pos,(size[0]-0.01,size[1]-0.01))
        
        for i in range(0,len(obj_list)):
            if obj_list[i] != self:
                obj = obj_list[i]
                o_bounds = get_bounds(obj.pos,obj.size)
                bounds = [s_bounds,o_bounds]

                min_x = [0,0]
                min_x[0] = bounds[0]['min'][0]
                if o_bounds['min'][0] < min_x[0]: min_x[0] = bounds[1]['min'][0]
                min_x[1] = bounds[int(min_x[0] == bounds[0]['min'][0])]['min'][0]
                if False:
                    max_x = [0,0]
                    max_x[0] = bounds[0]['max'][0]
                    if o_bounds['max'][0] > max_x[0]: max_x[0] = bounds[1]['max'][0]
                    max_x[1] = bounds[int(max_x == bounds[0]['max'][0])]['max'][0]
                max_x = [
                    bounds[int(min_x[0] != bounds[0]['min'][0])]['max'][0],
                    bounds[int(min_x[0] == bounds[0]['min'][0])]['max'][0]
                ]

                min_y = [0,0]
                min_y[0] = bounds[0]['min'][1]
                if o_bounds['min'][1] < min_y[0]: min_y[0] = bounds[1]['min'][1]
                min_y[1] = bounds[int(min_y[0] == bounds[0]['min'][1])]['min'][1]
                if False:
                    max_y = [0,0]
                    max_y[0] = bounds[0]['max'][1]
                    if o_bounds['max'][1] > max_y[0]: max_y[0] = bounds[1]['max'][1]
                    max_y[1] = bounds[int(max_y == bounds[0]['max'][1])]['max'][1]
                max_y = [
                    bounds[int(min_y[0] != bounds[0]['min'][1])]['max'][1],
                    bounds[int(min_y[0] == bounds[0]['min'][1])]['max'][1]
                ]



                check_x = min_x[0] <= min_x[1] <= max_x[0]
                check_y = min_y[0] <= min_y[1] <= max_y[0]
                if check_x and check_y: return i




                if False:
                    if not (s_min[0] < s_max[0] < o_min[0] < o_max[0]) and  not (o_min[0] < o_max[0] < s_min[0] < s_max[0]):
                        if not (s_min[1] < s_max[1] < o_min[1] < o_max[1]) and  not (o_min[1] < o_max[1] < s_min[1] < s_max[1]):
                            #print(self.velocity[0])
                            #print('k')
                            return i
        return None

    @abstractmethod
    def custom_update(self): pass

    @abstractmethod
    def render(self,camera): pass


class Tilemap(Entity):
    def __init__(self,id,pos,size,sprite):
        super().__init__(id,pos,size)
        self.sprite = sprite
        self.color = (255,255,255)
        if sprite != None:
            self.sprite_pos = []
            r_x = self.size[0]/unit_size
            r_y = self.size[1]/unit_size
            x,y = 0,0
            bounds = get_bounds(self.pos,self.size)
            diff_x = bounds['max'][0] - bounds['min'][0]
            diff_y = bounds['max'][1] - bounds['min'][1]
            frac_x = diff_x/unit_size
            frac_y = diff_y/unit_size
            while x < frac_x:
                while y < frac_y:
                    pos = (bounds['min'][0]+unit_size/2+(unit_size*x),bounds['min'][1]+unit_size/2+(unit_size*y))
                    self.sprite_pos.append(pos)
                    y += 1
                x += 1
                y = 0

    def render(self,camera):
        if self.sprite != None:
            for pos in self.sprite_pos:
                camera.blit(self.sprite,pos,(unit_size,unit_size))
        else: camera.draw_rect(self.color,self.pos,self.size)

class Solid(Tilemap):
    def start(self):
        self.color = (100,100,200)

class Trap(Tilemap):
    def __init__(self,id,pos,size,sprite):
        super().__init__(id,pos,size,sprite)
        self.collision = 'trigger'
        self.color = pygame.Color('red')

class Orb(Entity):
    def __init__(self,id,pos,size):
        super().__init__(id,pos,size)
        self.collision = 'trigger'
        self.used = False
        self.reload_time = 5
        self.count = 0
        self.sprite = import_vertical_sprite('Graphics/Sprites/Orb/orb.png',size[1],True)
    
    def update(self):
        if self.used:
            self.collision = None
            self.count += self.deltaTime
            if self.count >= self.reload_time:
                self.count = 0
                self.used = False
                self.collision = 'trigger'


    def render(self,camera):
        if not self.used:
            camera.blit(self.sprite,self.pos,self.size) 
            #camera.draw_rect(pygame.Color('blue'),self.pos,self.size)
