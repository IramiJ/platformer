from entities.enemies.enemy import Enemy
from entities.animations import load_animation
from entities.hp_bar import Hp_bar


class Chaser(Enemy):
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height)
        self.spawn_point = (self.x, self.y)
        self.aggro_range = 100
        self.action = 'run'
        self.animation_database['idle'] = load_animation('assets/enemies/chaser/idle', [30,30], self)
        self.animation_database['run'] = load_animation('assets/enemies/chaser/run', [15,15,15,15], self)
        self.hp_bar = Hp_bar('assets/hp_bar/enemy_hp_bar_bg.png','assets/hp_bar/enemy_hp_bar_frame.png',self.x,self.y-20)
        self.direction = 'r'
        self.velocity = 1
        self.attack_cd = 0
        

    def render(self, display, scroll):
        if not self.alive:
            return 
        self.draw(display, scroll)
        self.hp_bar.x = self.rect.x-scroll[0]
        self.hp_bar.y = self.rect.y-scroll[1]-20
        self.hp_bar.draw(display, 3, self.hp)
    def move(self, player):
        self.movement = [0, 0]
        if abs(self.rect.x - player.rect.x) <= self.aggro_range:
            if player.rect.x < self.rect.x:
                self.change_action('run')
                self.direction = 'l'
                self.flip = False
                self.movement[0] -= self.velocity
            elif player.rect.x > self.rect.x:
                self.change_action('run')
                self.direction = 'r'
                self.flip = True
                self.movement[0] += self.velocity
            elif player.rect.x == self.rect.x:
                self.movement[0] = 0
        elif self.rect.x != self.spawn_point[0]:
                if self.rect.x < self.spawn_point[0]:
                    self.change_action('run')
                    self.direction = 'r'
                    self.flip = True
                    self.movement[0] += self.velocity
                else:
                    self.change_action('run')
                    self.direction = 'l'
                    self.flip = False
                    self.movement[0] -= self.velocity
        else:
            self.change_action('idle')
        self.rect.x += self.movement[0]

    def attack(self, player):
        if self.attack_cd > 0:
            
            self.attack_cd -= 1
        else:
            if self.rect.colliderect(player.rect) and not player.dashing:
                player.hp -= 1
                self.attack_cd = 30
