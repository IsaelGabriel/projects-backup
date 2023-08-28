from player import *
from entity import *
from info import *
from map import Map

class Game:
    def __init__(self,render_surface):
        self.obj_dict = dict()
        self.render_surface = render_surface
        #self.coll_list = []

        self.map = Map("Graphics/Map collisions/test_map.png","Graphics/Map collisions/test_map.png",render_surface,10)
        self.add_object(Player("Player",Vector2(1,2),Vector2(5,5),render_surface,True,None))

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
        self.map.render()
        for obj in self.obj_dict.keys():
            self.obj_dict[obj].render()


    def get_object(self,id):
        return self.obj_dict[id]
