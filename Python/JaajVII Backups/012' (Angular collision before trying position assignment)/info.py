from pygame.math import Vector2

window_size = Vector2(80,60)
window_name = "GAME"
window_scale = 10
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

def get_pos_add(nums):
    min = nums[0]
    for i in range(0,len(nums)):
        if nums[i] < min: min = nums[i]
    return abs(min)

def get_bounds(pos,size):
    n_min = [0,0]
    n_max = [0,0]
    for z in range(0,2):
        n_min[z] = pos[z]-size[z]/2
        n_max[z] = pos[z]+size[z]/2
    return {
        'min' : n_min,
        'max' : n_max
    }