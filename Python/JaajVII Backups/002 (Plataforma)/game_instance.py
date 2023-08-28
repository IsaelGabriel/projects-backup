from player import *
from entity import *
from info import *

class Game:
    def __init__(self,render_surface):
        self.obj_dict = dict()
        self.render_surface = render_surface
        #self.coll_list = []
        self.add_object(Player("Player",Vector2(10,20),Vector2(50,50),render_surface,True,None))
        self.add_object(Solid("Block",Vector2(window_size.x/2-250,window_size.y*0.75),Vector2(500,50),render_surface,True,None))
        self.add_object(Solid("Block_2",Vector2(0,window_size.y*0.75-50),Vector2(200,50),render_surface,True,None))
        self.add_object(Solid("Block_3",Vector2(window_size.x-150,window_size.y*0.75-50),Vector2(150,50),render_surface,True,None))

    def add_object(self,obj):
        already_added = False
        for existing_obj in self.obj_dict.keys():
            if existing_obj == obj.id:
                already_added = True
        if not already_added:
            self.obj_dict[obj.id] = obj
            self.obj_dict[obj.id].start(self)

    def update(self):
        for obj in self.obj_dict.keys():
            self.obj_dict[obj].update(self)

    def render(self):
        for obj in self.obj_dict.keys():
            self.obj_dict[obj].render()

    def get_object(self,id):
        return self.obj_dict[id]
