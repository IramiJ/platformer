from entities.entity import entity
from entities.animations import load_animation
import pygame

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
        self.dashing = False
        self.dash_timer = 0
        self.dash_duration = 10
        self.dash_speed = 6
        self.dash_cooldown = 0
        self.hp = 5
        self.animation_database['idle'] = load_animation('assets/char/idle', [15, 15], self)
        self.animation_database['run'] = load_animation('assets/char/run', [5,5,5,5], self)
        self.dmg_cd = 0
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
    def update_frames(self):
        self.frame += 1
        if self.frame >= len(self.animation_database[self.action]):
            self.frame = 0
        self.img_id = self.animation_database[self.action][self.frame]
        self.img = self.animation_frames[self.img_id]
    def draw(self, display):
        display.blit(pygame.transform.flip(self.img,self.flip,False), [self.rect.x-self.scroll[0], self.rect.y-self.scroll[1]])
    def attack(self, enemy):
        if self.dmg_cd == 0:
            if self.dashing:
                if self.rect.colliderect(enemy.rect):
                    enemy.hp -= 1
                    self.dmg_cd = self.dash_cooldown
        else:
            self.dmg_cd -= 1
