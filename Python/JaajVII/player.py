import pygame
from info import *
from anim import Animator
from entity import PhysicsEntity,Entity,obj_list
from math import sqrt

m = sqrt(2/4)#sqrt(2)/2


class Player(PhysicsEntity):
    def start(self):
        # spawning
        self.spawnpoint = self.pos

        self.set_spawn_variables()

        # animation
        self.sprite_list = {
            'rp' : import_vertical_sprite('Graphics/Sprites/rp_1.png',self.size[1],True),
            'birdie0' : import_vertical_sprite('Graphics/Sprites/Player/Birdie0.png',self.size[1],True)
        }

        anims = { # [duration,frames]
            'idle' : [1,4],
            'birdie' : [1,1],
            'run' : [0.35,4],
            'dash' : [1,1]
        }
        for a in anims.keys():
            for i in range(0,anims[a][1]):
                self.sprite_list[f'{a}_{i}'] = import_vertical_sprite(f'Graphics/Sprites/Player/{a}{i}.png',self.size[1],True)

        self.silhuette_list = dict()
        for k in self.sprite_list.keys():
            self.silhuette_list[k] = get_silhuette(self.sprite_list[k])
        
        self.current_sprite = 'idle_0'
        self.animator = Animator(anims,'birdie')

    def set_spawn_variables(self):
        # basic physics
        self.gravity_add = 10
        self.gravity_max = 30
        self.grounded = False
        self.velocity = (0,0)
    
        # movement
        self.move_speed = 25
        self.move_acc_rate = 3
        self.move_decc_rate = 5
        self.direction = 'right'

        # jumping
        self.jump_force = 40#0
        self.holding_jump = False
        self.jump_hold = 0
        self.jump_duration = 0.2 # in seconds
        self.jump_step = 0
        self.jumping = False

        # dash
        self.dash_charged = True
        self.holding_dash = False
        self.dashing = False
        self.dash_type = (0,0)
        self.dash_velocity = 90#80#60
        self.dash_step = 0
        self.dash_duration = 0.25 # in seconds
        self.dash_sprites = []

    def respawn(self):
        self.pos = self.spawnpoint
        self.set_spawn_variables()

    def custom_update(self):
        if get_button('debug_pos'): print(self.pos)
        if self.velocity[1] < self.gravity_max and not self.grounded and not self.jumping:
            self.velocity = (self.velocity[0],self.velocity[1]+self.gravity_add)
            if self.velocity[1] > self.gravity_max: self.velocity = (self.velocity[0],self.gravity_max)
        if not self.dashing: self.move()
        self.jump()
        self.dash()
        if self.grounded and not self.dash_charged: self.dash_charged = True
        
        c_trigger = self.get_collision((0,0),(self.size[0]-0.01,self.size[1]-0.01))

        if c_trigger != None: 
            if obj_list[c_trigger].collision == 'trigger':
                if obj_list[c_trigger].__class__.__name__ == 'Trap': self.respawn()
                elif obj_list[c_trigger].__class__.__name__ == 'Orb': 
                    self.dash_charged = True
                    obj_list[c_trigger].used = True
        if get_button('respawn'): self.respawn()

    def move(self):

        vel_value = 0
        left = get_button('left')
        right = get_button('right')
        if left or right:
            a = (self.move_speed/self.move_acc_rate)
            if left:
                self.direction = 'left'
                vel_value = -1
            elif right:
                self.direction = 'right'
                vel_value = 1
            if abs(self.velocity[0]+a*vel_value) <= self.move_speed:
                self.velocity = (self.velocity[0]+(a*vel_value),self.velocity[1])
            elif abs(self.velocity[0]) < self.move_speed:
                self.velocity = (self.move_speed*vel_value,self.velocity[1])
        d = 0
        if (not left and self.direction == 'left' and self.velocity[0] < 0) or (right and self.velocity[0] < 0):
            d = (self.move_speed/self.move_decc_rate)
        elif (not right and self.direction == 'right' and self.velocity[0] > 0) or (left and self.velocity[0] > 0):
            d = -(self.move_speed/self.move_decc_rate)
        elif abs(self.velocity[0]) > self.move_speed and (left or right):
            d = -(self.move_speed/self.move_decc_rate) * vel_value
        if d != 0:
            if abs(self.velocity[0])-abs(d) < 0: self.velocity = (0,self.velocity[1])
            else: self.velocity = (self.velocity[0]+d,self.velocity[1])
        #print(self.velocity)

        
    def jump(self):
        d_coll = self.get_collision((0,self.size[1]/2),(self.size[0]-0.01,0.1))
        if d_coll != None: self.grounded = obj_list[d_coll].collision == 'on'
        else: self.grounded = False

        if get_button('jump') and not self.holding_jump:
            self.holding_jump = True
            if self.grounded and self.jump_step == 0:
                self.jumping = True
                self.jump_hold = self.deltaTime
        elif not get_button('jump'): self.holding_jump = False

        if self.jumping:
            if self.jump_step < self.jump_duration/10 or self.jump_hold:
                self.velocity = (self.velocity[0],-self.jump_force)
                self.jump_step += self.deltaTime
                if self.jump_step >= self.jump_duration:
                    if self.jump_step >= self.jump_duration + self.jump_duration/10:
                        self.jump_step = 0
                        self.jumping = False
                    else:
                        t = (self.jump_duration/10)-(self.jump_step - self.jump_duration)
                        f = -self.jump_force
                        ft  = (f * t)/(self.jump_duration/10)
                        self.velocity = (self.velocity[0],ft)
                if self.holding_jump: self.jump_hold += self.deltaTime
                else: self.jump_hold = 0
            else:
                self.jump_step = 0
                self.jumping = False
                self.jump_hold = 0
        else: self.jump_hold = 0

    def dash(self):

        if get_button('dash') and not self.holding_dash:
            self.holding_dash = True
            if not self.dashing and self.dash_charged:
                self.dashing = True
                dir_x = int(get_button('right')) - int(get_button('left'))
                dir_y = int(get_button('l_down')) - int(get_button('l_up'))
                d = (dir_x,dir_y)
                if abs(d[0]) == 1 and abs(d[1]) == 1: d = (m*d[0],m*d[1])
                if d == (0,0):
                    dir_x = int(self.direction == 'right') - int(self.direction == 'left')
                    d = (dir_x,dir_y)
                #d = (d[0]*sqrt(2),d[1]*sqrt(2))
                self.dash_type = d
                self.dash_charged = False
                self.dash_sprites = []
        elif not get_button('dash'): self.holding_dash = False

        if self.dashing:
            vel_x = (self.dash_velocity*self.dash_type[0])
            vel_y = (self.dash_velocity*self.dash_type[1])
            self.velocity = (vel_x,vel_y)
            self.dash_step += self.deltaTime
            self.dash_sprites.append([self.pos,(self.direction == 'left'),self.current_sprite])
            if self.dash_step >= self.dash_duration:
                self.dashing = False
                self.dash_step = 0
                self.dash_type = (0,0)
        elif len(self.dash_sprites) != 0:
            self.dash_sprites.pop(0)
            if len(self.dash_sprites) == 1: self.dash_sprites = []


    def fix_coords(self):
        new_size = (self.sprite_list[self.current_sprite].get_width()/window_scale,self.sprite_list[self.current_sprite].get_height()/window_scale)
        base = self.pos[1]+self.size[1]/2
        self.size = new_size
        self.pos = (self.pos[0],base-self.size[1]/2)

    def render(self,camera):
        if self.dashing and self.animator.c_anim != 'birdie': self.animator.play_anim('dash')
        elif not self.dashing and (get_button('left') or get_button('right')): self.animator.play_anim('run')
        elif not self.dashing and self.animator.c_anim != 'idle': self.animator.play_anim('idle')
        self.animator.update(self.deltaTime)
        self.current_sprite = self.animator.c_spr
        if self.size != (self.sprite_list[self.current_sprite].get_width()/window_scale,self.sprite_list[self.current_sprite].get_height()/window_scale): 
            self.fix_coords()
        camera.set_position((self.pos[0],self.pos[1]-self.size[1]))
        #camera.draw_rect(pygame.Color('green'),self.pos,self.size)
        #self.current_sprite = f'idle_{int()}'
        flip = (self.velocity[0] < 0 or (self.velocity[0] == 0 and self.direction == 'left'))
        for spr in self.dash_sprites:
            camera.blit(pygame.transform.flip(self.silhuette_list[spr[2]], spr[1], False),(spr[0]),self.size)
        camera.blit(pygame.transform.flip(self.sprite_list[self.current_sprite], flip, False),(self.pos[0],self.pos[1]),self.size)
        #camera.blit(pygame.transform.flip(self.sprite_list['birdie'], flip, False),(self.pos[0],self.pos[1]),self.size)
        #if get_button('left'): camera.draw_rect(pygame.Color('red'), self.pos,self.size)
