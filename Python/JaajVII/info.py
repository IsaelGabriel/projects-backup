import pygame
from pygame.math import Vector2

window_size = Vector2(80,60)
window_name = "BOB"
window_scale = 10
unit_size = 5
camera_position = (0,0)
c_palette = {
    "#333333" : ["#2d1b00","#622e4c","#46425e","#161616","#010101","#0f0f1b","#11070a"],
    "#666666" : ["#1e606e","#7550e8","#5b768d","#ab4646","#6e1fb1","#565a75","#860020"],
    "#999999" : ["#5ab9a8","#608fcf","#d17c7c","#8f9bf6","#cc3385","#c6b7be","#ff0015"],
    "#CCCCCC" : ["#c4f0c2","#8be5ff","#f6c6a8","#f0f0f0","#f8fbf3","#fafbf6","#fffcfe"]
}
palette_bgs = [
    c_palette["#666666"][0],
    c_palette["#333333"][1],
    c_palette["#333333"][2],
    c_palette["#666666"][3],
    c_palette["#666666"][4],
    c_palette["#666666"][5],
    c_palette["#666666"][6]#,
    #c_palette["#666666"][7]
    ]
current_palette = 2
bg_color = palette_bgs[current_palette]#"#1d2636"
keys = {
    "left" : False,
    "right" : False,
    "down" : False,
    'up' : False,
    'x' : False,
    'c' : False,
    'r' : False,
    'p' : False
}

buttons = {
    "left" : 'left',
    'right' : 'right',
    'l_up' : 'up',
    'l_down': 'down',
    'jump' : 'c',
    'dash' : 'x',
    'respawn' : 'r',
    'debug_pos' : 'p'
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



def color_change(surface,old_color,new_color):
    surf_copy = pygame.Surface((surface.get_width(),surface.get_height()))
    surf_copy.fill(new_color)
    surface.set_colorkey(old_color)
    surf_copy.blit(surface,(0,0))
    
    return surf_copy

def apply_outline(src,out_add):
    surf = pygame.Surface((src.get_width()+2,src.get_height()+1+out_add))
    #surf.fill((0,0,0))
    surf.blit(src,(1,1))
    outline = pygame.Surface((surf.get_width(),surf.get_height()))
    outline.set_colorkey((0,0,0))
    o_color = c_palette["#CCCCCC"][current_palette]
    for x in range(0,surf.get_width()):
        for y in range(0,surf.get_height()):
            if surf.get_at((x,y)) != (0,0,0):
                if x-1 >= 0:
                    if surf.get_at((x-1,y)) == (0,0,0): outline.set_at((x-1,y),o_color)
                if y-1 >= 0:
                    if surf.get_at((x,y-1)) == (0,0,0): outline.set_at((x,y-1),o_color)
                if x < surf.get_width()-1:
                    if surf.get_at((x+1,y)) == (0,0,0): outline.set_at((x+1,y),o_color)
                if y < surf.get_width()-2+out_add:
                    if surf.get_at((x,y+1)) == (0,0,0): outline.set_at((x,y+1),o_color)
    surf.blit(outline,(0,0))
    return surf

def import_sprite(path,new_size,outline):
    img = pygame.image.load(path).convert_alpha()
    for c in c_palette.keys():
        img = color_change(img,c,c_palette[c][current_palette])
    out_add = 0
    if outline:
        if img.get_height() == 8: out_add = 1
        img = apply_outline(img,out_add)
    if outline: img = apply_outline(img,out_add)
    img.set_colorkey((0,0,0))
    img = pygame.transform.scale(img,(new_size[0],new_size[1]))
    
    return img

def import_vertical_sprite(path,y,outline):
    img = pygame.image.load(path).convert_alpha()
    for c in c_palette.keys():
        img = color_change(img,c,c_palette[c][current_palette])
    out_add = 0
    if outline:
        if img.get_height() == 8: out_add = 1
        img = apply_outline(img,out_add)
    img.set_colorkey((0,0,0))
    x = (img.get_width()*y)/img.get_height()
    img = pygame.transform.scale(img,((x+out_add)*window_scale,(y+out_add)*window_scale))
    
    return img

def get_silhuette(img):
    bg = pygame.Surface((img.get_width(),img.get_height()))
    bg.fill((0,0,0))
    bg.blit(img,(0,0))
    img = bg
    s_color = pygame.Color(c_palette["#CCCCCC"][current_palette])
    s_color.a = 150
    for x in range(0,img.get_width()):
        for y in range(0,img.get_height()):
            if img.get_at((x,y)) != (0,0,0): img.set_at((x,y),s_color)
    img.set_colorkey((0,0,0))
    #img.convert_alpha()
    return img
