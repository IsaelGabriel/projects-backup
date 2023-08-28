import pygame, sys
from info import *
from player import *
from entity import *
from camera import *
#from game_instance import *
from pygame.math import Vector2
from pygame.locals import FULLSCREEN, DOUBLEBUF

    # Object list: (0 = Type), (1 = Name/id), (2 = position), (3 = size)
scene_dict = {
    'Test Scene' : [
        ["Player","Player",(-37,-27),(5,5)],
        ["Solid","",(0,55/2),(window_size[0],10)],
        ["Solid","",(0,(window_size.y*3/8)-2.5),(50,5)],
        ["Solid","",(-30,(window_size.y*3/8)-7.5),(20,5)],
        ["Solid","",(32.5,(window_size.y*3/8)-7.5),(15,5)],
        ["Solid","",(32.5,2.5),(15,5)],
        ["Trap","", (-17.5,(window_size.y*3/8)-5-(5/4/2)+0.1),(5,5/4)]
    ]
}

# game class start
class Game:
    def __init__(self,screen):
        self.ready = False
        self.screen = screen
        self.camera = Camera(screen)
        self.current_scene = 'Test Scene'
        obj_list = []
        self.load_scene(self.current_scene)

# core game loop

    def update(self):
        for i in range(0,len(obj_list)):
            obj_list[i].deltaTime = self.deltaTime
            if callable(getattr(obj_list[i], "update", False)): obj_list[i].update()
        self.camera.topleft = camera_position
        #print(int(1/self.deltaTime))#show FPS

    def render(self):
        for i in range(0,len(obj_list)):
            if callable(getattr(obj_list[i], "render", False)): obj_list[i].render(self.camera)

# scene system

    def load_scene(self,scene_id):
        if scene_id in scene_dict.keys():
            for index in range(0, len(scene_dict[scene_id])):
                self.add_object(scene_dict[scene_id][index])
                if callable(getattr(obj_list[-1], "start", False)): obj_list[-1].start()
        self.ready = True

# obj handling

    def add_object(self,obj):
        if obj[1] == None: return #no_class
        if obj[0] == "Player":
            obj_list.append(Player(obj[1],obj[2],obj[3]))
        elif obj[0] == "Solid":
            obj_list.append(Solid(obj[1],obj[2],obj[3]))
        elif obj[0] == "Trap":
            obj_list.append(Trap(obj[1],obj[2],obj[3]))

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

    pygame.display.update()
    clock.tick(60)
