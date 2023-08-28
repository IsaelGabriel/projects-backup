class Collision:
    def __init__(self,id_1,id_2,pos):
        self.id_1 = id_1
        self.id_2 = id_2
        self.pos = pos

    def get_opposite(self,id):
        if self.id_1 == id:
            return id_2
        else: return id_1

    def includes(self,id):
        if self.id_1 == id or self.id_2 == id:
            return True
        else: return False
