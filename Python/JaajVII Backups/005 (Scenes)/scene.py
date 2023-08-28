from player import *
from entity import *
from info import *
from camera import *


class Scene:
    def __init__(self,render_surface,obj_list):
        self.obj_dict = dict()
        self.render_surface = render_surface
        #self.coll_list = []
        self.camera = Camera(render_surface,Vector2(window_size.x*3,window_size.y),window_size,bg_color)

        for obj in obj_list:
            self.add_object(obj[0],obj[1],obj[2],obj[3],obj[4])

    def add_object(self,id,type,pos,size,collision):
        if id == None or (id in self.obj_dict.keys()): id = self.set_id(type)

        if type == "Player":
            self.obj_dict[id] = Player(id,pos,size,collision)
        elif type == "Solid":
            self.obj_dict[id] = Solid(id,pos,size,collision)

        if id in self.obj_dict.keys(): self.obj_dict[id].full_start(self)
        
    def set_id(self,type):
        num = 0
        for id in self.obj_dict.keys():
            if self.obj_dict[id].__class__.__name__ == type:
                num += 1
        return (type + "_" + str(num))


    def update(self):
        for obj in self.obj_dict.keys():
            self.obj_dict[obj].full_update(self)
        self.camera.render()

    def render(self):
        for obj in self.obj_dict.keys():
            self.obj_dict[obj].full_render(self)

    def get_object(self,id):
        return self.obj_dict[id]
