from entities.enemies.enemy import Enemy
from entities.animations import load_animation
from entities.entity import simple_entity
from entities.hp_bar import Hp_bar

class Patroller(Enemy):
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height)
        self.spawn_point = (self.x, self.y)
        self.distance = 20
        self.action = 'run'
        self.animation_database['run'] = load_animation('assets/enemies/patroller/run', [15,15,15,15], self)
        self.hp_bar = Hp_bar('assets/hp_bar/enemy_hp_bar_bg.png','assets/hp_bar/enemy_hp_bar_frame.png',self.x,self.y-20)
        self.direction = 'r'
        self.velocity = 0.5
        self.attack_cd = 0
        

    def render(self, display, scroll):
        if not self.alive:
            return 
        self.draw(display, scroll)
        self.hp_bar.x = self.rect.x-scroll[0]
        self.hp_bar.y = self.rect.y-scroll[1]-20
        self.hp_bar.draw(display, 3, self.hp)
    def move(self):
        self.movement = [0, 0]
        if self.direction == 'r':
            if self.rect.x >= self.spawn_point[0] + self.distance:
                self.direction = 'l'
                self.flip = True
            else:
                self.movement[0] += self.velocity
        if self.direction == 'l':
            if self.rect.x <= self.spawn_point[0] - self.distance:
                self.direction = 'r'
                self.flip = False
            else:
                self.movement[0] -= self.velocity
        self.rect.x += self.movement[0]
    def attack(self, player, scroll):
        if self.attack_cd > 0:
            
            self.attack_cd -= 1
        else:
            if self.rect.colliderect(player.rect) and not player.dashing:
                player.take_dmg(scroll)
                self.attack_cd = 30
    
