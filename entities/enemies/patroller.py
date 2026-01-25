from entities.enemies.enemy import Enemy
from entities.animations import load_animation
from entities.entity import simple_entity
import pygame

class Patroller(Enemy):
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height)
        self.spawn_point = (self.x, self.y)
        self.distance = 40
        self.action = 'run'
        self.animation_database['run'] = load_animation('assets/enemies/patroller/run', [15,15,15,15], self)
        self.hp_bar = simple_entity('assets/hp_bar/enemy_hp_bar.png', [self.x, self.y-20])
    def render(self, display, scroll):
        self.draw(display, scroll)
        display.blit(self.hp_bar.img, [self.rect.x-scroll[0], self.rect.y-scroll[1]-20])