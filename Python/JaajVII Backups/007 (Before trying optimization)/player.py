import pygame
from info import *
from entity import Entity

class Player(Entity):
    def start(self):
        # basic physics
        self.gravity = 8
        self.grounded = False
        # walking
        self.speed = 7
        self.acceletation = 2
        self.decceleration = 1
        self.direction = 'right'
        # jump
        self.holding_jump = False
        self.jumping = False
        self.jump_force = [5,5,5,10,10,15,20,20,15,10,5,0,0,0,0,0]
        #self.jump_force = [5,5,0,10,10,0,15,15,15,0,20,20,0,0,0,0,0]
        self.jump_step = 0
        # dash
        self.dash_charged = True
        self.holding_dash = False
        self.dashing = False
        self.dash_velocity = 20
        self.dash_step = 0
        self.dash_duration = 12 # in frames
        self.dash_render = []
        self.dash_render_count = 0
        self.dash_render_frames = 30

    def update(self):
        #if self.get_every_trigger("normal",1) == "Trap" or not 0 < self.pos.x < self.scene.camera.map_size.x or not 0 < self.pos.y < self.scene.camera.map_size.y:
            #self.scene.reload()
        self.grounded =  (self.get_every_collision('down',1) == "Solid")
        self.move()
        self.jump()
        if self.velocity.y < self.gravity and not self.jumping:
            self.velocity.y += self.gravity
            if self.velocity.y > self.gravity:
                self.velocity.y = self.gravity
        self.dash()
        self.set_velocity()

        if self.pos.x + (self.size.x/2) < window_size.x/2:
            self.scene.camera.pos.x = 0
        else:
            self.scene.camera.pos.x = (self.pos.x + (self.size.x/2)) - (window_size.x/2)

    def move(self):
        w_vel = self.velocity.x
        if get_button('w_left'):
            w_vel -= self.acceletation
            self.direction = 'left'
        elif get_button('w_right'):
            w_vel += self.acceletation
            self.direction = 'right'
        else:
            if w_vel < 0:
                w_vel += self.decceleration
                if w_vel > 0: w_vel = 0
            elif w_vel > 0:
                w_vel  -= self.decceleration
                if w_vel < 0: w_vel = 0
            else: w_vel = 0


        if w_vel > self.speed: w_vel = self.speed
        elif w_vel < -self.speed: w_vel = -self.speed

        self.velocity.x = w_vel

    def jump(self):
        if get_button('jump') and not self.holding_jump:
            self.holding_jump = True
            if not self.jumping and self.grounded:
                self.jumping = True
        elif not get_button('jump'): self.holding_jump = False

        if self.jumping:
            if self.jump_step < len(self.jump_force) :
                self.velocity.y = -self.jump_force[self.jump_step]
                self.jump_step += 1
            if (not self.holding_jump) and (0 < self.jump_step < len(self.jump_force)-6):
                self.jump_step = len(self.jump_force)-6
            if 0 < self.jump_step >= len(self.jump_force):
                self.jumping = False
                self.jump_step = 0

    def dash(self):
        if len(self.dash_render) > 0:
            self.dash_render_count += 1
        if self.dash_render_count >= self.dash_render_frames:
            self.dash_render = []
            self.dash_render_count = 0


        if self.grounded and (not self.dash_charged) and (not self.dashing): self.dash_charged = True
        if get_button('dash') and not self.holding_dash and not self.dashing:
            self.holding_dash = True
            if self.dash_charged:
                self.dashing = True
                self.dash_charged = False
                self.dash_render = []
                self.dash_render_count = 0

        elif not get_button('dash'):
            self.holding_dash = False

        if self.dashing:
            if self.dash_render_count % 2 == 0: self.dash_render.append((self.pos.x,self.pos.y))
            self.dash_charged = False
            mult = Vector2(0,0)
            if get_button('w_left'): mult.x = -1
            elif get_button('w_right'): mult.x = 1

            if get_button('l_up'): mult.y = -1
            elif get_button('l_down'): mult.y = 1
            elif not get_button('w_left') and get_button('w_right'):
                 if self.direction == 'left': mult.x = -1
                 else: mult.x = 1

            self.velocity = (mult *  self.dash_velocity)
            self.dash_step += 1

        if self.dash_step >= self.dash_duration:
            self.dash_step = 0
            self.dashing = False
            self.dash_charged = False



    def obj_collided(self,direction):
        pass

    def no_collision(self,direction):
        pass

    def render(self):
        #render basic dash trail
        dash_index = 0
        if len(self.dash_render) > 0:
            for pos in range(0,len(self.dash_render)):
                reduce_value = 10
                #dash_rect = pygame.Rect(dash_pos.x,dash_pos.y,self.size.x,self.size.y)
                rect = pygame.Rect(self.dash_render[pos],self.size)
                rect.center = (rect.center[0]+reduce_value/2,rect.center[1]+reduce_value/3)
                rect.size = (rect.size[0]-reduce_value,rect.size[1]-reduce_value)
                min = (67,38,97,100)
                max = (113, 7, 171,170)
                ratio =  (((100/len(self.dash_render))*(pos + 1))/100) # float # 100/len(dash_render)*pos+1
                vs = []
                for value in range(0,4):
                    vs.append(int(((max[value]-min[value]) * ratio)+min[value]))
                c = (vs[0],vs[1],vs[2],vs[3])
                self.scene.camera.draw_transparent_rect(pygame.Color(c),rect)

        #render square
        self.render_base_rect((75,150,75))
        #render eye
        d = int((self.direction == 'right'))
        eye_rect = pygame.Rect(0,0,int(self.size.x)/5,int((self.size.y/5)*2))
        eye_rect.center = Vector2(int(self.pos.x + 10 + ((self.size.x - 20)*d)),int(self.pos.y + 5 + eye_rect.size[1]/2))
        if not self.grounded: eye_rect.center = Vector2(eye_rect.center[0],eye_rect.center[1]+5)
        self.scene.camera.draw_rect((150,150,170),eye_rect)
