class Game:
    def __init__(self,render_surface):
        self.obj_dict = {}
        self.render_surface = render_surface
        self.coll_list = []

    def add_object(self,obj):
        already_added = False
        for existing_obj in self.obj_dict.keys():
            if existing_obj == obj.id:
                already_added = True
        if not already_added:
            self.obj_dict[obj.id] = obj
            self.obj_dict[obj.id].start()

    def update(self):
        check_all_collisions()
        for obj in self.obj_dict:
            obj.update()

    def check_all_collisions(self):
        for obj_1 in self.obj_dict:
            for collision in self.coll_list:
                obj_2 = self.obj_dict[collision.get_opposite(obj_1.id)]
                if collision.includes(obj_1.id):
                    if not obj_1.coll_enabled:
                        obj_1.coll_exit(obj_2,collision.pos)
                        self.obj_dict[obj_2.id].collision_exit(obj_1,collision_pos)
                        self.coll_list.remove(collision)
                    else:
                        if check_collision(obj_1,obj_2):
                            # update collision points
                            obj_1.collision_stay(obj_2,collision.pos)
                            self.obj_dict[obj_2.id].collision_stay(obj_1,collision_pos)
            for obj_2 in self.obj_dict:
                if obj_1.coll_enabled and obj_2.coll_enabled:
                    if check_collision(obj_1,obj_2):
                        # create collision
                        # call get collision on both objects


    def check_collision(self,obj_1,obj_2):
        pass

    def render(self):
        pass
