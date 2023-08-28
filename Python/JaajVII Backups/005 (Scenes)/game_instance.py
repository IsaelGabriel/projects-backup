from player import Player
from info import *
from camera import Camera
from scene import Scene

class Game:
    def __init__(self,render_surface):
        self.render_surface = render_surface
        self.scene_dict = {
            "Scene 1" : Scene(render_surface,[
                ("Player","Player",Vector2(10,20),Vector2(50,50),"on"),
                (None,"Solid",Vector2(window_size.x/2-250,window_size.y*0.75),Vector2(500,50),"on"),
                (None,"Solid",Vector2(0,window_size.y*0.75-50),Vector2(200,50),"on"),
                (None,"Solid",Vector2(window_size.x-150,window_size.y*0.75-50),Vector2(150,50),"on"),
                (None,"Solid",Vector2(window_size.x-150,window_size.y*0.50-50),Vector2(150,50),"on")
            ])
        }
        self.current_scene = self.scene_dict["Scene 1"]
