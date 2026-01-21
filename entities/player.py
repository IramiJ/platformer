from entities.entity import entity
#from entities.animations import load_animation

class Player(entity):
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height)
        self.moving_left = False
        self.moving_right = False
        self.y_momentum = 0
        self.velocity = 2
        self.jump_momentum = -10
        self.buffs = []
        self.air_timer = 0
        self.double_coin_buff = False
        self.animation_database = {}
        self.scroll = [0,0]
        self.movement = [0, 0]
        self.animation_frames = {}
    def dying(self):
        if self.rect.y > 500:
            self.rect.x = 0
            self.rect.y = 304
    def apply_buffs(self):
        for buff in self.buffs:
            if buff == 'speed_boost':
                self.velocity = 4
            elif buff == 'jump_boost':
                self.jump_momentum = -15
            elif buff == 'double_coins':
                self.double_coin_buff = True