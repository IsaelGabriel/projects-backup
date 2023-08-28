from pygame.math import Vector2

window_size = Vector2(800,600)
window_name = "GAME"
camera_position = (0,0)
bg_color = "#1d2636"
keys = {
    "left" : False,
    "right" : False,
    "down" : False,
    'up' : False,
    'x' : False,
    'c' : False
}

buttons = {
    "w_left" : 'left',
    'w_right' : 'right',
    'l_up' : 'up',
    'l_down': 'down',
    'jump' : 'c',
    'dash' : 'x'
}

def get_button(id):
    if id in buttons.keys():
        if buttons[id] in keys.keys():
            return keys[buttons[id]]
    return False
