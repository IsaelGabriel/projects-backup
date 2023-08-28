import pygame, sys
from info import *
from player import *
from entity import *
from camera import *
#from game_instance import *
from pygame.math import Vector2
from pygame.locals import FULLSCREEN, DOUBLEBUF

u = unit_size
    # Scene = [Map, Obj_list]
    # Object list: (0 = Type), (1 = Name/id), (2 = position), (3 = size)
scene_dict = {
    'Test Scene 0' : [
            [
                (window_size[0]*3,window_size[1]*3),
                'Test Map 0'
            ],
        [
            ["Player","Player",(-37,-27),(u,u)],
            ["Solid","",(0,(u*10+u)/2),(window_size[0],u*2)],
            ["Solid","",(0,(window_size.y*3/8)-u/2),(10*u,u)],
            ["Solid","",(-u*6,(window_size.y*3/8)-(u+u/2)),(u*4,u)],
            ["Solid","",(32.5,(window_size.y*3/8)-7.5),(u*3,u)],
            ["Solid","",(32.5,u/2),(u*3,u)],
            ["Solid","",(37.5,0),(u,u*12)],
            ["Trap","",(-17.5,(window_size.y*3/8)-u-(u/4/2)+0.1),(u,u/4)],
            ["Trap","",(0,(window_size.y*3/8)-u-(u/4/2)+0.1),(u,u/4)]
    ]],
    'Test Scene 1' : [
            [
                (window_size[0],window_size[1]*3),
                'Test Map 1'
            ],
        [
            ["Player","Player",(0,0+60),(u,u)],
            ["Solid","",(0,(u*10+u)/2+60),(window_size[0],u*2)],
            ["Solid","",(0,(window_size.y*3/8)-u/2+60),(10*u,u)],
            ["Solid","",(-u*6,(window_size.y*3/8)-(u+u/2)+60),(u*4,u)],
            ["Solid","",(32.5,(window_size.y*3/8)-7.5+60),(u*3,u)],
            ["Solid","",(32.5,u/2+60),(u*3,u)],
            ["Solid","",(-32.5,(u/2)*-3+60),(u*3,u)],
            ["Solid","",(32.5,(u/2)*-9+60),(u*3,u)],
            ["Solid","",(37.5,0),(u,window_size[1]*3)],
            ["Solid","",(-37.5,0),(u,window_size[1]*3)],
            ["Trap","",(-17.5,(window_size.y*3/8)-u-(u/4/2)+0.1+60),(u,u/4)],
            ["Trap","",(22.5,(window_size.y*3/8)-u-(u/4/2)+0.1+60),(u,u/4)],
            ["Orb","",(0,30),(u/2,u/2)],
            ["Bob","",(0,75),(u,u)]
    ]]
}

# game class start
class Game:
    def __init__(self,screen):
        self.ready = False
        self.screen = screen
        self.current_scene = 'Test Scene 1'
        obj_list = []
        self.camera = None
        self.load_scene(self.current_scene)
        

# core game loop

    def update(self):
        for i in range(0,len(obj_list)):
            if obj_list[i].destroy: obj_list.pop(i)
        for i in range(0,len(obj_list)):
            obj_list[i].deltaTime = self.deltaTime
            if callable(getattr(obj_list[i], "update", False)): obj_list[i].update()
        #self.camera.topleft = camera_position
        #print(int(1/self.deltaTime))#show FPS

    def render(self):
        for i in range(0,len(obj_list)):
            #if obj_list[i].animator != None:
                #for anim in obj_list[i].animator:
                    #anim.deltaTime = self.deltaTime
            if callable(getattr(obj_list[i], "render", False)): obj_list[i].render(self.camera)

# scene system

    def load_scene(self,scene_id):
        self.ready = False
        self.camera = Camera(screen,scene_dict[scene_id][0][0])
        #obj_list = []
        if scene_id in scene_dict.keys():
            for index in range(0, len(scene_dict[scene_id][1])):
                self.add_object(scene_dict[scene_id][1][index])
                if callable(getattr(obj_list[-1], "start", False)): obj_list[-1].start()
        self.ready = True

# obj handling

    def add_object(self,obj):
        if obj[1] == None: return #no_class
        if obj[0] == "Player":
            obj_list.append(Player(obj[1],obj[2],obj[3]))
        elif obj[0] == "Solid":
            obj_list.append(Solid(obj[1],obj[2],obj[3],import_vertical_sprite('Graphics/Sprites/block0.png',unit_size,False)))
        elif obj[0] == "Trap":
            obj_list.append(Trap(obj[1],obj[2],obj[3],None))
        elif obj[0] == "Orb":
            obj_list.append(Orb(obj[1],obj[2],obj[3]))
        elif obj[0] == "Bob":
            obj_list.append(Tilemap(obj[1],obj[2],obj[3],import_vertical_sprite('Graphics/Sprites/Player/bob0.png',unit_size,True)))

    def get_object(self,id):
        for i in obj_list:
            if obj_list[i].id == id:
                return obj_list[i]
        return False
# game class end





pygame.init()
pygame.display.set_caption(window_name)
clock = pygame.time.Clock()


flags = DOUBLEBUF
screen = pygame.display.set_mode((int(window_size.x*window_scale),int(window_size.y*window_scale)),flags,16)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

t = 0
getTicksLastFrame = 0
deltaTime = 0

game = Game(screen)

while 1:
    t = pygame.time.get_ticks()
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t

    pressed_keys = False
    for key in pygame.key.get_pressed():
        if key: pressed_keys = True
    if pressed_keys == False:
        for key in keys.keys(): keys[key] = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            for key in keys.keys():
                if key == pygame.key.name(event.key):
                    keys[key] = (event.type == pygame.KEYDOWN)

    #update method is called here
    game.deltaTime = deltaTime
    if game.ready: game.update()

    screen.fill(pygame.Color(bg_color))
    #render method is called here
    if game.ready: game.render()

    #print(clock.get_fps())

    pygame.display.update()
    clock.tick(60)
