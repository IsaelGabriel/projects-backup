import pygame
from info import *
from entity import Entity

class Player(Entity):
    def start(self):
        self.add = 7
        self.gravity = 5
        self.colliding_with_ground = False

    def update(self):
        new_pos = self.pos.x

        if keys['left']:
            new_pos -= self.add
        elif keys['right']:
            new_pos += self.add
        if 0 < (new_pos + self.size.x/2) < window_size.x:
            self.pos.x = new_pos

        #if not self.colliding_with_ground:
        if self.pos.y < 500:
            self.pos.y += self.gravity

    def render(self):
        self.render_base_rect(pygame.Color('#32db5d'))

    def get_collision(self,c_obj,c_pos):
        pass

    def collision_stay(self,c_obj,c_pos):
        if c_obj.id == "ground" and c_pos.y == self.position.y + self.size.y:
            self.colliding_with_ground = True

    def collision_exit(self,c_obj,c_pos):
        if c_obj.id == "ground": self.colliding_with_ground = False
