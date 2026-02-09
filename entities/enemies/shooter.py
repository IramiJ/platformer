from entities.enemies.enemy import Enemy
from entities.enemies.shooter_bullet import Shooter_Bullet
from entities.animations import load_animation
from entities.hp_bar import Hp_bar
from core.settings import Settings
import math, pygame

class Shooter(Enemy):
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height)
        self.spawn_point = [self.x, self.y]
        self.aggro_range = 120
        self.action = 'idle'
        self.animation_database['idle'] = load_animation('assets/enemies/shooter/idle', [20,20,20,20,20,20], self)
        self.animation_database['shoot'] = load_animation('assets/enemies/shooter/shoot', [20, 20], self)
        self.hp_bar = Hp_bar('assets/hp_bar/enemy_hp_bar_bg.png','assets/hp_bar/enemy_hp_bar_frame.png',self.x,self.y-20)
        self.attack_cd = 0
        self.collision_cd = 0
        

    def render(self, display, scroll):
        if not self.alive:
            return 
        self.draw(display, scroll)
        self.hp_bar.x = self.rect.x-scroll[0]
        self.hp_bar.y = self.rect.y-scroll[1]-20
        self.hp_bar.draw(display, 3, self.hp)
    def attack(self, player, bullet_list, scroll):
        if self.attack_cd > 0:           
            self.attack_cd -= 1
        elif math.sqrt((self.spawn_point[0] - player.rect.x)**2 + (self.spawn_point[1] - player.rect.y)**2) <= self.aggro_range:
            self.change_action('shoot')
            if self.attack_cd == 0:
                self.attack_cd = 3 * Settings.fps
                bullet_list.append(Shooter_Bullet(self.spawn_point.copy(), player))
        else:
            self.change_action('idle')
        
        if self.collision_cd > 0:
            self.collision_cd -= 1

        elif self.rect.colliderect(player.rect) and not player.dashing:
            player.take_dmg(scroll)
            self.collision_cd  = 30

        

    
        

             