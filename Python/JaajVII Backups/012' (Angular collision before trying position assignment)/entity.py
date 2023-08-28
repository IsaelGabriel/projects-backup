import pygame
from pygame.math import Vector2
from abc import ABC,abstractmethod
from math import sqrt
from info import window_scale,get_bounds

obj_list = []

class Entity(ABC):
    def __init__(self,id,pos,size):
        self.id = id
        self.pos = pos
        self.size = size
        self.collision = 'on'
        self.deltaTime = 0

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
        self.set_velocity()

    def apply_velocity(self):
        self.set_velocity_angle()
        np = [0,0]
        for i in range(0,2): np[i] = self.pos[i]+self.delta_vel[i]
        self.pos = (np[0],np[1])

    def set_velocity(self):
        vel = (self.velocity[0]*self.deltaTime,self.velocity[1]*self.deltaTime)
        if self.deltaTime == 0: return
        c_x,c_y = False,False
        

    def set_velocity_angle(self): # se n funcionar, trocar range para velocidade + 1 e dividir vel baseado na fraçao
        vel = (self.velocity[0]*self.deltaTime,self.velocity[1]*self.deltaTime)
        if self.deltaTime == 0: return
        coll = [self.get_collision((vel[0],0),self.size),self.get_collision((vel[1],0),self.size)]
        c_x = False
        c_y = False
        if coll[0] != None or coll[1] != None:
            last_x = 0
            last_y = 0
            max_x = 0
            max_y = 0
            c_x = False
            c_y = True
            x_ind = 1
            y_ind = 1
            for d in range(1,21):
                x = vel[0] * (x_ind/20)
                y = vel[1] * (y_ind/20)
                coll = [self.get_collision((x,last_y),self.size),self.get_collision((last_x,y),self.size)]
                if coll[0] != None and not c_x:
                    if obj_list[coll[0]].collision == 'on':
                        max_x = x
                        c_x = True
                        max_y = last_y
                        c_y = True
                        self.delta_vel = (max_x,max_y)
                        return
                elif not c_x: x_ind = d
                last_x = x
                if coll[1] != None and not c_y:
                    if obj_list[coll[1]].collision == 'on':
                        max_y = y
                        c_y = True
                        max_x = last_x
                        c_x = True
                        self.delta_vel = (max_x,max_y)
                        return
                elif not c_y: y_ind = d
                last_y = y
        self.delta_vel = vel
        return

    def set_velocity_angle_detailed(self):
        vel = (self.velocity[0] * self.deltaTime,self.velocity[1]*self.deltaTime)
        if self.deltaTime == 0: return
        distance = sqrt((vel[0]*(10**3))**2+(vel[1]*(10**3))**2)
        for d in range(1,int(distance)+1):
            #r_size = ((self.size[0]+2)*window_scale,(self.size[1]+2)*window_scale)
            x = ((d*(vel[0]))/distance)
            y = ((d*(vel[1]))/distance)
            #coll = self.get_collision((x*window_scale,y*window_scale),r_size)
            coll = self.get_collision((x,y),self.size)
            if coll != None:
                if obj_list[coll].collision == 'on':
                    if d == 1:
                        self.delta_vel = (0,0)
                    else:
                        x = (d-1*(vel[0]))/distance
                        y = (d-1*(vel[1]))/distance
                        self.delta_vel = (x,y)
                    return
            #print(d)
        self.delta_vel = vel
        return

    def get_collision(self,distance,size):
        s_pos = (self.pos[0] + distance[0],self.pos[1]+distance[1])
        s_bounds = get_bounds(s_pos,size)
        s_min = s_bounds['min']
        s_max = s_bounds['max']
        
        for i in range(0,len(obj_list)):
            if obj_list[i] != self:
                obj = obj_list[i]
                o_bounds = get_bounds(obj.pos,obj.size)
                o_min = o_bounds['min']
                o_max = o_bounds['max']

                if not ((s_min[0] < s_max[0] < o_min[0] < o_max[0]) or (o_min[0] < o_max[0] < s_min[0] < s_max[0])):
                    if not ((s_min[1] < s_max[1] < o_min[1] < o_max[1]) or (o_min[1] < o_max[1] < s_min[1] < s_max[1])):
                        #print('k')
                        return i
        return None

    def get_collision_list(self,distance,size):#[collided obj index, collision distance from center,collision size]
        s_pos = (self.pos[0] + distance[0],self.pos[1]+distance[1])
        s_bounds = get_bounds(s_pos,size)
        s_min = s_bounds['min']
        s_max = s_bounds['max']
        c_list = []
        for i in range(0,len(obj_list)):
            if obj_list[i] != self:
                obj = obj_list[i]
                o_bounds = get_bounds(obj.pos,obj.size)
                o_min = o_bounds['min']
                o_max = o_bounds['max']
                if not ((s_min[0] < s_max[0] < o_min[0] < o_max[0]) or (o_min[0] < o_max[0] < s_min[0] < s_max[0])):
                    if not ((s_min[1] < s_max[1] < o_min[1] < o_max[1]) or (o_min[1] < o_max[1] < s_min[1] < s_max[1])):
                        c_pos = [0,0]
                        c_size = [0,0]
                        #x_c = False
                        #y_c = False
                        #t = "overlap"
                        for z in range(0,2):
                            if s_min[z] <= o_min[z] <= o_max[z] <= s_max[z]:
                                d_min = o_min[z]-s_min[z]
                                d_max = s_max[z]-o_max[z]
                                c_size[z] = (size[z]-obj.size[z])
                                #diff min - size - diff max
                                c_pos[z] = ((s_min[z]+d_min+c_size[z]/2)-s_pos[z])
                            elif o_min[z] <= s_min[z] <= s_max[z] <= o_max[z]:
                                c_size = (size[z])
                                c_pos = (0)
                            elif s_min[z] <= o_min[z] and s_max[z] <= o_max[z]:
                                diff = s_max[z]-o_min[z]
                                c_pos = ((o_min[z]+(diff)/2)-s_pos[z])
                                c_size = ((diff))
                            elif s_max[z] >= o_max[z] and s_min[z] >= o_min[z]:
                                diff = o_max[z]-s_min[z]
                                c_pos = ((s_min[z]+(diff)/2)-s_pos[z])
                                c_size = ((diff))
                        f_pos = (c_pos[0],c_pos[1])
                        f_size = (c_size[0],c_size[1])
                        c_list.append([i,f_pos,f_size])
        return c_list

    def get_collision_definition(self,coll,size):
        d = list(range(0,len(coll)))
        for i in range(0,len(coll)):
            c_dist = coll[i][1]
            c_size = coll[i][2]
            d[i] = [obj_list[coll[i][0]].collision]
            if c_dist == (0,0) and c_size == size: d[i].append('inside')
            print(d[i])


        return d

    def fix_position(self):
        coll = {
            'up' : self.get_collision((0,(-self.size[1]/2)),(self.size[0],1)),
            'down' : self.get_collision((0,(self.size[1]/2)-1),(self.size[0],1)),
            'left' : self.get_collision(((-self.size[0]/2),0),(1,self.size[1])),
            'right' : self.get_collision(((self.size[0]/2)-1,0),(1,self.size[1]))
        }

        for d in coll.keys():
            if coll[d] != None:
                obj = obj_list[coll[d]]
                if obj.collision == 'on':
                    if d == 'down':
                        self.pos = (self.pos[0],obj.pos[1]-obj.size[1]/2-self.size[1]/2)
                    
    
                        

        
    @abstractmethod
    def custom_update(self): pass

    @abstractmethod
    def render(self,camera): pass

class Solid(Entity):
    def render(self,camera): camera.draw_rect((100,100,200),self.pos,self.size)

class Trap(Entity):
    def __init__(self,id,pos,size):
        super().__init__(id,pos,size)
        self.collision = 'trigger'

    def render(self,camera): camera.draw_rect(pygame.Color('red'),self.pos,self.size)
