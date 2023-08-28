class Animator:
    def __init__(self,animations,first_anim):
        # animations = dict()
        # animations[x] = [duration,frames]
        self.anims = animations
        self.c_anim = first_anim
        # current sprite = id of current sprite
        self.c_spr = f'{self.c_anim}_0'
        self.anim_count = 0

    def set_anim_sprite(self):
        i = (self.anim_count*self.anims[self.c_anim][1])/self.anims[self.c_anim][0]
        key = f'{self.c_anim}_{int(i)}'
        self.c_spr = key

    def play_anim(self,anim_id):
        self.c_anim = anim_id
        self.c_spr = f'{anim_id}_0'

    def update(self,dt):
        self.anim_count += dt
        if self.anim_count >= self.anims[self.c_anim][0]: self.anim_count = 0
        self.set_anim_sprite()
