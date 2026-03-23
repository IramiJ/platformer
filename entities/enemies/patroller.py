from entities.enemies.enemy import Enemy
from entities.animations import load_animation
from entities.hp_bar import Hp_bar

class Patroller(Enemy):
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height)
        self.spawn_point = (self.x, self.y)
        self.distance = 50
        self.action = 'run'
        self.animation_database['run'] = load_animation('assets/enemies/patroller/run', [5,5,5,5,5,5], self)
        self.hp_bar = Hp_bar('assets/hp_bar/enemy_hp_bar_bg.png','assets/hp_bar/enemy_hp_bar_frame.png',self.x,self.y-20)
        self.direction = 'r'
        self.velocity = 1.2
        self.burst_velocity = 0.6
        self.true_velocity = self.velocity + self.burst_velocity
        self.attack_cd = 0
        self.stunned = False
        self.stun_cd = 0
        self.bursting = False
        self.burst_cd = 0
        

    def render(self, display, scroll):
        if not self.alive:
            return 
        self.draw(display, scroll)
        self.update_hp_bar_location(scroll)
        self.hp_bar.draw(display, self.max_hp, self.hp)
    def update_hp_bar_location(self, scroll):
        self.hp_bar.x = self.rect.x-scroll[0]
        self.hp_bar.y = self.rect.y-scroll[1]-20
    def move(self, dt):
        if self.stunned:
            self.stun_cd -= 1
            if self.stun_cd == 0:
                self.stunned = False
        else:
            self.movement = [0, 0]
            self.handle_burst()
            if self.direction == 'r':
                self.move_right()
            if self.direction == 'l':
                self.move_left()
            self.rect.x += self.movement[0] * dt
    def move_right(self):
        if self.rect.x >= self.spawn_point[0] + self.distance:
            self.direction = 'l'
            self.flip = True
            self.activate_burst()
        else:
            self.movement[0] += self.true_velocity
    def move_left(self):
        if self.rect.x <= self.spawn_point[0] - self.distance:
            self.direction = 'r'
            self.flip = False
            self.activate_burst()
        else:
            self.movement[0] -= self.true_velocity
    def attack(self, player, scroll):
        if self.attack_cd > 0:
            self.attack_cd -= 1
        else:
            if self.rect.colliderect(player.rect) and not player.dashing:
                player.take_dmg(scroll)
                self.attack_cd = 30
    def stun(self):
        self.stun_cd = 20
        self.stunned = True
    def activate_burst(self):
        self.bursting = True
        self.burst_cd = 30
    def handle_burst(self):
        if self.bursting:
            self.true_velocity = self.velocity + self.burst_velocity
            self.burst_cd -= 1
            if self.burst_cd == 0:
                self.bursting = False
        else:
            self.true_velocity = self.velocity
    
