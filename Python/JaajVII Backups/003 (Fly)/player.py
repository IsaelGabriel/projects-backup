import pygame
from info import *
from entity import Entity

class Player(Entity):
    def start(self,scene):
        self.scene = scene
        self.speed = 3
        self.velocity = Vector2(0,0)

    def update(self,scene):
        self.scene = scene

        if keys['up']: self.velocity.y -= self.speed
        elif keys['down']: self.velocity.y += self.speed
        else: self.velocity.y = 0

        if self.velocity.y > self.speed: self.velocity.y = self.speed
        elif self.velocity.y < -self.speed: self.velocity.y = -self.speed

        self.pos.y += self.velocity.y

    def render(self):
        self.render_base_rect(pygame.Color('#32db5d'))


class Old_player(Entity):
    def start(self,scene):
        self.add = 7
        self.gravity = 8
        self.grounded= False
        self.scene = scene
        self.velocity = Vector2(0,0)
        self.jump_force = 20
        self.jumping = False
        self.jump_step = 0
        self.holding_jump = False

    def update(self,scene):
        self.scene = scene

        if keys['left']:
            self.velocity.x = self.check_collision_left()
        elif keys['right']:
            self.velocity.x = self.check_collision_right()
        else:
            self.velocity.x = 0

        grav = self.can_fall()
        if keys['up'] and not self.holding_jump:
            self.holding_jump = True
            if self.grounded:
                self.jumping = True
        elif not keys['up']: self.holding_jump = False

        if self.velocity.y < grav:
            self.velocity.y += grav
        elif self.velocity.y > grav:
            self.velocity.y = grav

        if self.jumping:
            self.velocity.y = -self.jump_force
            self.jump_step += 1

        if self.jump_step >= 8:
            self.jump_step = 0
            self.jumping = False

        self.check_bounds()
        self.pos += self.velocity

    def render(self):
        self.render_base_rect(pygame.Color('#32db5d'))

    def can_fall(self):
        c_obj = None
        rect = pygame.Rect(self.pos.x,self.pos.y + self.size.y,self.size.x,self.gravity)
        for obj_id in self.scene.obj_dict.keys():
            obj = self.scene.get_object(obj_id)
            if obj != self:
                if obj.coll_enabled and self.coll_enabled:
                    obj_rect = obj.get_collision_rect("normal")
                    if rect.colliderect(obj_rect):
                        c_obj = obj
        if c_obj != None:
            for y in range(1, self.gravity+1):
                rect = pygame.Rect(self.pos.x,self.pos.y + self.size.y,self.size.x,y)
                obj_rect = c_obj.get_collision_rect("normal")
                if rect.colliderect(obj_rect):
                    if y - 1 == 0:
                        self.grounded = True
                        if self.pos.y + self.size.y > c_obj.pos.y and self.velocity.y >= 0:
                            self.pos.y = c_obj.pos.y - self.size.y
                    else: self.grounded = False
                    return y - 1
        self.grounded = False
        if self.pos.y == window_size.y - self.size.y: self.grounded = True
        return self.gravity

    def check_bounds(self):
        new_pos = self.pos + self.velocity
        if new_pos.x <= 0:
            self.velocity.x = -self.pos.x
        elif new_pos.x + self.size.x >= window_size.x:
            self.velocity.x = window_size.x - (self.pos.x + self.size.x)

        if new_pos.y <= 0:
            self.velocity.y = -self.pos.y
        elif new_pos.y + self.size.y >= window_size.y:
            self.velocity.y = window_size.y - (self.pos.y + self.size.y)

    def check_collision_right(self):
        c_obj = None
        rect = pygame.Rect(self.pos.x+self.size.x,self.pos.y,self.add,self.size.y)
        for obj_id in self.scene.obj_dict.keys():
            obj = self.scene.get_object(obj_id)
            if obj != self:
                if obj.coll_enabled and self.coll_enabled:
                    obj_rect = obj.get_collision_rect("normal")
                    if rect.colliderect(obj_rect):
                        c_obj = obj
        if c_obj != None:
            for x in range(1, self.add+1):
                rect = pygame.Rect(self.pos.x+self.size.x,self.pos.y,x,self.size.y)
                obj_rect = c_obj.get_collision_rect("normal")
                if rect.colliderect(obj_rect):
                    return x - 1
        return self.add

    def check_collision_left(self):
        c_obj = None
        rect = pygame.Rect(self.pos.x-self.add,self.pos.y,self.add,self.size.y)
        for obj_id in self.scene.obj_dict.keys():
            obj = self.scene.get_object(obj_id)
            if obj != self:
                if obj.coll_enabled and self.coll_enabled:
                    obj_rect = obj.get_collision_rect("normal")
                    if rect.colliderect(obj_rect):
                        c_obj = obj
        if c_obj != None:
            for x in range(1, self.add+1):
                rect = pygame.Rect(self.pos.x-x,self.pos.y,x,self.size.y)
                obj_rect = c_obj.get_collision_rect("normal")
                if rect.colliderect(obj_rect):
                    return -(x - 1)
        return -self.add
