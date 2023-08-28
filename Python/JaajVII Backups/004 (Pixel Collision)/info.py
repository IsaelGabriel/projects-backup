import pygame
from pygame.math import Vector2


t = 1
deltaTime = 1
get_ticks_last_frame = 1

window_size = Vector2(800,600)
window_name = "BOB - Game Jaaj 7"
bg_color = "#1d2636"
framerate = 60
keys = {
    "left" : False,
    "right" : False,
    "up" : False,
    "space" : False,
    "z" : False
}
key_bindings = {
    "w_left" : "left",
    "w_right" : "right",
    "l_up" : "up",
    "l_down" : "down",
    "jump" : "space",
    "dash" : "z"
}

def get_button(id):
    if id in key_bindings.keys():
        if key_bindings[id] in keys.keys():
            return keys[key_bindings[id]]
    return False

def import_image(path,multiplier):
    image = pygame.image.load(path).convert_alpha()
    resize = pygame.transform.scale(image,(int(image.get_width() * multiplier),int(image.get_height() * multiplier)))
    return resize
