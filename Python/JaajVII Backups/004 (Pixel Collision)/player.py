import pygame
from info import *
from entity import Entity

class Player(Entity):
    def start(self,scene):
        self.base_speed = 1.5
        self.speed = self.base_speed
        self.velocity = Vector2(0,0)
        self.map = scene.map
        self.gravity = 3
        self.mass = 1

    def update(self,scene):
        #self.move()
        self.set_velocity()
        self.pos += Vector2(self.velocity.x * deltaTime,self.velocity.y)

    def move(self):
        if get_button("w_left"):
            self.velocity.x = -self.speed
        elif get_button("w_right"):
            self.velocity.x = self.speed
        else:
            self.velocity.x = 0

    def set_velocity(self):
        velocity = self.velocity.y
        #set y velocity for gravity
        if velocity < self.gravity:
            velocity += self.gravity
        elif velocity > self.gravity:
            velocity = self.gravity

        velocity = self.gravity
        #if self.velocity.y >= 0:
        y_set = False
        for y in range(1,int(velocity)+1):
            for x in range(0,int(self.size.x + 1)):
                pos = Vector2(int(self.pos.x + x),self.pos.y+self.size.y + y)
                if pos in self.map.coll_list and not y_set:
                        ind = self.map.coll_list.index(pos)
                        print(pos)
                        velocity = pos.y - (self.pos.y+self.size.y)
                        y_set = True
                elif self.pos.y + self.size.y + y == window_size.y/10:
                    velocity = y
                    y_set = True

        self.velocity.y = velocity



    def render(self):
        self.render_base_rect(pygame.Color('green'),self.map.multiplier)

class Old_Player(Entity):
    def start(self,scene):
        self.mass = 1
        self.base_speed = 7
        self.speed = 7
        self.dashing = False
        self.dash_speed = 15
        self.dash_step = 0
        self.dash_step_max = 10
        self.base_gravity = 15
        self.gravity = 0
        self.grounded= False
        self.scene = scene
        self.velocity = Vector2(0,0)
        self.jump_force = [10,15,20,15,15,15,40,15]
        self.jumping = False
        self.jump_step = 0
        self.holding_jump = False


    def update(self,scene):
        self.scene = scene

        if get_button("w_left"):
            self.velocity.x = self.check_collision_left() * deltaTime
        elif get_button("w_right"):
            self.velocity.x = self.check_collision_right() * deltaTime
        else:
            self.velocity.x = 0



        if self.gravity < self.base_gravity:
            self.gravity += 1 * deltaTime

        grav = self.can_fall()
        if get_button('jump') and not self.holding_jump:
            self.holding_jump = True
            # if self.grounded:
            if self.can_fall() == 0:
                self.jumping = True
                self.gravity = 0
        elif not get_button('jump'): self.holding_jump = False

        if self.velocity.y < grav:
            self.velocity.y += grav * deltaTime
        elif self.velocity.y > grav:
            self.velocity.y = grav * deltaTime

        if self.jumping:
            self.velocity.y = -self.jump_force[self.jump_step]
            self.jump_step += 1

        if self.holding_jump:
            if self.jump_step >= len(self.jump_force):
                self.jump_step = 0
                self.jumping = False
        else:
            if self.jump_step >= int(len(self.jump_force)/2):
                self.jump_step = 0
                self.jumping = False

        self.check_bounds()
        self.pos += self.velocity * deltaTime
        if self.velocity.y == 0: self.gravity = 0

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
        rect = pygame.Rect(self.pos.x+self.size.x,self.pos.y,self.speed,self.size.y)
        for obj_id in self.scene.obj_dict.keys():
            obj = self.scene.get_object(obj_id)
            if obj != self:
                if obj.coll_enabled and self.coll_enabled:
                    obj_rect = obj.get_collision_rect("normal")
                    if rect.colliderect(obj_rect):
                        c_obj = obj
        if c_obj != None:
            for x in range(1, self.speed+1):
                rect = pygame.Rect(self.pos.x+self.size.x,self.pos.y,x,self.size.y)
                obj_rect = c_obj.get_collision_rect("normal")
                if rect.colliderect(obj_rect):
                    return x - 1
        return self.speed

    def check_collision_left(self):
        c_obj = None
        rect = pygame.Rect(self.pos.x-self.speed,self.pos.y,self.speed,self.size.y)
        for obj_id in self.scene.obj_dict.keys():
            obj = self.scene.get_object(obj_id)
            if obj != self:
                if obj.coll_enabled and self.coll_enabled:
                    obj_rect = obj.get_collision_rect("normal")
                    if rect.colliderect(obj_rect):
                        c_obj = obj
        if c_obj != None:
            for x in range(1, self.speed+1):
                rect = pygame.Rect(self.pos.x-x,self.pos.y,x,self.size.y)
                obj_rect = c_obj.get_collision_rect("normal")
                if rect.colliderect(obj_rect):
                    return -(x - 1)
        return -self.speed

    def dash(self):
        pass
