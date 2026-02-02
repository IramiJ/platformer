from entities.entity import entity
from entities.player.tail import Tail
from entities.animations import load_animation
import pygame

class Player(entity):
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height)
        self.spawn_point = [self.rect.x, self.rect.y]
        self.moving_left = False
        self.moving_right = False
        self.y_momentum = 0
        self.velocity = 3
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
        self.cd_obj = entity(self.x, self.y + 15, 16, 16)
        self.cd_obj.animation_database['idle'] = load_animation('assets/cooldown/idle', [8 for x in range(15)], self.cd_obj)
        self.tail = Tail('assets/tail/grey.png',[self.rect.x-2, self.rect.y+8])
    def dying(self, max_y):
        if self.rect.y > max_y:
            self.rect.x = self.spawn_point[0]
            self.rect.y = self.spawn_point[1]
    def apply_buffs(self):
        for buff in self.buffs:
            if buff == 'speed boost':
                self.velocity = 4
            elif buff == 'jump boost':
                self.jump_momentum = -15
            elif buff == 'double coins':
                self.double_coin_buff = True
    def update_frames(self):
        self.frame += 1
        if self.frame >= len(self.animation_database[self.action]):
            self.frame = 0
        self.img_id = self.animation_database[self.action][self.frame]
        self.img = self.animation_frames[self.img_id]
    def draw(self, display, scroll):
        display.blit(pygame.transform.flip(self.img,self.flip,False), [self.rect.x-scroll.render_scroll[0], self.rect.y-scroll.render_scroll[1]])
    def attack(self, enemy):
        if self.dmg_cd == 0:
            if self.dashing:
                if self.rect.colliderect(enemy.rect):
                    enemy.take_dmg()
                    self.dmg_cd = self.dash_cooldown
        else:
            self.dmg_cd -= 1
    def take_dmg(self, scroll):
        self.hp -= 1
        scroll.shake_timer = 10
        scroll.shake_strength = 3
    