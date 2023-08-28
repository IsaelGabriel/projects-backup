import pygame
from pygame.math import Vector2
from abc import ABC,abstractmethod

class Entity(ABC):
    def __init__(self,id, pos, size, collision):
        self.id = id
        self.pos = pos
        self.size = size
        self.collision = collision
        self.velocity = Vector2(0,0)

    def full_start(self,scene):
        self.scene = scene
        self.start()

    @abstractmethod
    def start(self):
        pass

    def full_update(self,scene):
        self.scene = scene
        self.update()

    @abstractmethod
    def update(self):
        pass

    def full_render(self,scene):
        self.scene = scene
        self.render()

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def obj_collided(self,direction):
        pass

    @abstractmethod
    def no_collision(self,direction):
        pass

    def set_velocity(self):
        self.set_velocity_axis('x')
        self.set_velocity_axis('y')

    def set_velocity_axis(self,axis):
        scene = self.scene
        vel = 0
        pos = 0
        size = 0
        modes = ['left','right']
        if axis == 'x':
            vel = self.velocity.x
            pos = self.pos.x
            size = self.size.x
            modes = ['left','right']
        elif axis == 'y':
            vel= self.velocity.y
            pos = self.pos.y
            size = self.size.y
            modes = ['up','down']
        if vel == 0 or (not axis in ['x','y']) or scene == None:
            return 0
        mode =  modes[0]
        mult = -1
        if vel > 0:
            mode = modes[1]
            mult = 1
        c_obj = None

        for obj_id in scene.obj_dict.keys():
            obj = scene.get_object(obj_id)
            if obj != self:
                if self.get_collision(self.get_collision_rect(mode,vel * mult),obj):
                    c_obj = obj
        if c_obj != None:
            if not self.get_collision(self.get_collision_rect(mode,1),c_obj):
                self.no_collision(mode)
            for z in range(1,int((vel * mult) + 1)):
                if self.get_collision(self.get_collision_rect(mode,z),c_obj):
                    if z - 1 == 0:
                        c_pos = c_obj.pos.x
                        c_size = c_obj.size.x
                        if axis == 'y':
                            c_pos = c_obj.pos.y
                            c_size = c_obj.pos.y
                        self.obj_collided(mode)
                        if mode == 'left' or mode == 'up':
                            if pos < c_pos + c_size:
                                pos = c_pos + c_size
                        if mode == 'right' or mode == 'down':
                            if pos + size > c_pos:
                                pos = c_pos - size
                    vel = (z - 1) * mult
                    if axis == 'x': self.pos.x += vel
                    else: self.pos.y += vel
                    return 0
        if axis == 'x': self.pos.x += self.velocity.x * (self.scene.deltaTime * 45)
        else: self.pos.y += self.velocity.y * (self.scene.deltaTime * 45)
        self.no_collision(mode)
        return 0

    def get_collision(self,rect,obj):
        if obj != self and obj.collision == 'on' and self.collision == 'on':
            obj_rect = obj.get_collision_rect("normal",1)
            if rect.colliderect(obj_rect):
                return True
        return False

    def render_base_rect(self,color):
        rect = pygame.Rect(int(self.pos.x),int(self.pos.y),int(self.size.x),int(self.size.y))
        #pygame.draw.rect(self.surface,color,rect)
        self.scene.camera.draw_rect(color,rect)

    def get_collision_rect(self,id,size):
        rect_pos = Vector2(self.pos.x,self.pos.y)
        rect_size = Vector2(1,1)
        if id == "down":
            rect_pos.y += self.size.y
            rect_size = Vector2(self.size.x,size)
        elif id == 'up':
            rect_pos.y -= size
            rect_size = Vector2(self.size.x,size)
        elif id == "left":
            rect_pos.x -= size
            rect_size = Vector2(size,self.size.y)
        elif id == "right":
            rect_pos.x += self.size.x
            rect_size = Vector2(size,self.size.y)
        elif id == "normal":
            rect_pos = Vector2(self.pos.x,self.pos.y)
            rect_size = Vector2(self.size.x,self.size.y)
        else:
            rect_pos -= Vector2(int(size/2),int(size/2))
            rect_size += Vector2(int(size),int(size))

        return pygame.Rect(rect_pos,rect_size)

    def get_every_collision(self,id,size):
        scene = self.scene
        for obj_id in scene.obj_dict.keys():
            obj = scene.get_object(obj_id)
            if obj != self:
                if self.get_collision(self.get_collision_rect(id,size),obj):
                    return True
        return False

class Solid(Entity):
    def start(self): pass

    def update(self): pass

    def obj_collided(self,direction): pass

    def no_collision(self,direction): pass

    def render(self): self.render_base_rect((100,100,200))
