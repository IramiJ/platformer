from entities.entity import entity
from entities.player.tail import Tail
from entities.player.sword import Sword
from entities.player.pistol import Pistol
from entities.animations import load_animation
import json
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
        self.buffs = {}
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
        self.max_dash_cd = 120
        self.dash_cooldown = 0
        self.hp = 5
        self.dmg = 1
        self.animation_database['idle'] = load_animation('assets/char/idle', [15,15,20,30,10,10], self)
        self.animation_database['run'] = load_animation('assets/char/run', [5 for x in range(12)], self)
        self.dmg_cd = 0
        self.cd_obj = entity(self.x, self.y + 15, 16, 16)
        self.cd_obj.animation_database['idle'] = load_animation('assets/cooldown/idle', [8 for x in range(15)], self.cd_obj)
        self.tail = Tail('assets/tail/grey.png',[self.rect.x-2, self.rect.y+8])
        self.sword = Sword(self.rect.x, self.rect.y)
        self.pistol = Pistol(self.rect.y, self.rect.y)
        self.action = "idle"
        self.mode = "meele"
    def dying(self, max_y):
        if self.rect.y > max_y:
            self.rect.x = self.spawn_point[0]
            self.rect.y = self.spawn_point[1]
    def apply_buffs(self, buff_list):
        c = self.buffs.copy()   
        for buff in buff_list:
            if buff not in self.buffs:
                if buff == "speed boost":
                    self.velocity = 3
                elif buff == "jump boost":
                    self.jump_momentum = -10
                elif buff == "double coins":
                    self.double_coin_buff = False
        for buff in c:
            if self.buffs[buff] > 0:
                if buff == 'speed boost':
                    self.velocity = 4
                    self.buffs[buff] -= 1
                elif buff == 'jump boost':
                    self.jump_momentum = -15
                    self.buffs[buff] -= 1
                elif buff == 'double coin':
                    self.double_coin_buff = True
                    self.buffs[buff] -= 1
            else:
                self.buffs.pop(buff)
            
    def update_frames(self):
        self.frame += 1
        if self.frame >= len(self.animation_database[self.action]):
            self.frame = 0
        self.img_id = self.animation_database[self.action][self.frame]
        self.img = self.animation_frames[self.img_id]
    def draw(self, display, scroll):
#        pygame.draw.rect(display, (255,0,0), pygame.Rect(self.rect.left - scroll.render_scroll[0], self.rect.top - scroll.render_scroll[1], 16, 16))
        if self.mode == "meele":
            self.sword.draw(self, display, scroll)
        elif self.mode == "ranged":
            self.pistol.draw(self, display, scroll)
        self.sword.particles = [p for p in self.sword.particles if p.duration > 0]
        display.blit(pygame.transform.flip(self.img,self.flip,False), [self.rect.x-scroll.render_scroll[0], self.rect.y-scroll.render_scroll[1]])

    
    

    def dash(self):
        if not self.dashing and self.dash_cooldown == 0:           
            self.dashing = True
            self.dash_timer = self.dash_duration
            self.dash_cooldown = self.max_dash_cd   

    def switch_mode(self):
        if self.mode == "meele":
            self.mode   = "ranged"
        elif self.mode == "ranged":
            self.mode = "meele"

    def update_mode_variables(self):
        if self.mode == "meele":
            self.velocity = 3
            self.dash_duration = 20
            self.dmg = 2
        elif self.mode == "ranged":
            self.velocity = 4
            self.dash_duration = 10
            self.dmg = 1


    def attack(self, enemy):
        if self.dmg_cd == 0:
            if self.dashing and self.mode == "meele":
                if self.rect.colliderect(enemy.rect):
                    enemy.take_dmg()
                    self.dmg_cd = self.dash_cooldown
                    self.hp += 1
        else:
            self.dmg_cd -= 1
    def take_dmg(self, scroll):
        self.hp -= 1
        scroll.shake_timer = 10
        scroll.shake_strength = 3
    