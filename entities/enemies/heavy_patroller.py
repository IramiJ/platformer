from .enemies import Patroller

class Heavy_Patroller(Patroller):
    def __init__(self,x,y,width=16,height=16):
        super().__init__(x,y,width,height)
        self.max_hp = 6
        self.hp = 6
        self.true_velocity = 1
    def move(self):
        self.movement = [0, 0]
        if self.direction == 'r':
            if self.rect.x >= self.spawn_point[0] + self.distance:
                self.direction = 'l'
                self.flip = True
            else:
                self.movement[0] += self.true_velocity
        if self.direction == 'l':
            if self.rect.x <= self.spawn_point[0] - self.distance:
                self.direction = 'r'
                self.flip = False
            else:
                self.movement[0] -= self.true_velocity
        self.rect.x += self.movement[0]