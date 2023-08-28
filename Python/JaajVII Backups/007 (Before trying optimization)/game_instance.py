from player import *
from entity import *
from info import *
from camera import *

class Game:
    def __init__(self,render_surface):
        self.ready = False
        self.obj_dict = dict()
        self.render_surface = render_surface
        #self.coll_list = []
        self.camera = Camera(render_surface,Vector2(window_size.x*2,window_size.y),window_size,bg_color)
        self.scene_list = {
            'Scene 1': [
                ("Player","Player",(10,20),(50,50),"on"),
                (None,"Solid",(window_size.x/2-250,window_size.y*0.75),(500,50)),
                (None,"Solid",(0,window_size.y*0.75-50),(200,50)),
                (None,"Solid",(window_size.x-150,window_size.y*0.75-50),(150,50)),
                (None,"Solid",(window_size.x-150,window_size.y*0.50-50),(150,50)),
                (None,"Trap",(window_size.x/2-250+50,window_size.y*0.75-(50/4)),(50,50/4))
            ]
        }
        self.current_scene = 'Scene 1'
        self.load(self.current_scene)

    def load(self,scene):
        self.ready = False
        self.obj_dict = None
        self.obj_dict = dict()
        self.current_scene = scene
        for i in range(0,len(self.scene_list[scene])):
            obj = self.scene_list[scene][i]
            self.add_object(obj[0],obj[1],obj[2],obj[3])
        self.ready = True

    def reload(self):
        self.load(self.current_scene)

    def add_object(self,id,type,pos,size):
        if id == None or (id in self.obj_dict.keys()): id = self.set_id(type)

        if type == "Player":
            self.obj_dict[id] = Player(id,pos,size)
        elif type == "Solid":
            self.obj_dict[id] = Solid(id,pos,size)
        elif type == "Trap":
            self.obj_dict[id] = Trap(id,pos,size)

        if id in self.obj_dict.keys(): self.obj_dict[id].full_start(self)

    def set_id(self,type):
        num = 0
        for id in self.obj_dict.keys():
            if self.obj_dict[id].__class__.__name__ == type:
                num += 1
        return (type + "_" + str(num))

    def update(self):
        for obj in self.obj_dict.keys():
            if self.obj_dict[obj].updating: self.obj_dict[obj].full_update(self)
        self.camera.render()

    def render(self):
        for obj in self.obj_dict.keys():
            self.obj_dict[obj].full_render(self)

    def get_object(self,id):
        return self.obj_dict[id]
