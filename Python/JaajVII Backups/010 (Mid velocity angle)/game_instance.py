from player import *
from entity import *
from info import *
from camera import *
    # Object list: (0 = Type), (1 = Name/id), (2 = position), (3 = size)
scene_dict = {
    'Test Scene' : [
        ["Player","Player",(10,10),(50,50)],
        ["Solid","",(0,500),(window_size[0],100)],
        ["Solid","",(window_size.x/2-250,window_size.y*0.75),(500,50)],
        ["Solid","",(0,window_size.y*0.75-50),(200,50)],
        ["Solid","",(window_size.x-150,window_size.y*0.75-50),(150,50)],
        ["Solid","",(window_size.x-150,window_size.y*0.50-50),(150,50)],
        ["Trap","", (window_size.x/2-250+50,window_size.y*0.75-(50/4)),(50,50/4)]
    ]
}

class Game:
    def __init__(self,screen):
        self.ready = False
        self.screen = screen
        self.camera = Camera(screen,(window_size.x*2,window_size.y))
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
        if obj[1] == None: return
        rect = pygame.Rect(obj[2],obj[3])
        if obj[0] == "Player":
            obj_list.append(Player(obj[1],rect))
        elif obj[0] == "Solid":
            count = 0
            for entity in obj_list:
                if entity.__class__.__name__ == "Solid": count += 1
            obj_list.append(Solid('Solid_'+str(count),rect))
        elif obj[0] == "Trap":
            count = 0
            for entity in obj_list:
                if entity.__class__.__name__ == "Trap": count += 1
            obj_list.append(Solid('Trap_'+str(count),rect))

    def get_object(self,id):
        for i in obj_list:
            if obj_list[i].id == id:
                return obj_list[i]
        return False
