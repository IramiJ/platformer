from entities.entity import entity
from world.collisions import collision_test
import pygame

class Enemy(entity):
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height)
        self.hp = 3
        self.velocity = 1
        self.alive = True
        self.dmg_timer = 0
    def update_frames(self):
        self.frame += 1
        if self.frame >= len(self.animation_database[self.action]):
            self.frame = 0
        self.img_id = self.animation_database[self.action][self.frame]
        self.img = self.animation_frames[self.img_id]
    def draw(self, display, scroll):
        to_blit = self.img.copy()
        if self.dmg_timer > 0:
            if self.dmg_timer == 5:
                to_blit.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_ADD)
            else:
                to_blit.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_ADD)
            self.dmg_timer -= 1
        else:
            self.dmg_timer = 0
        display.blit(pygame.transform.flip(to_blit,self.flip,False), [self.rect.x-scroll[0], self.rect.y-scroll[1]])
    def take_dmg(self):
        if not self.alive:
            return
        self.dmg_timer = 5
        self.hp -= 1
        self.taking_dmg = True
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
    def collision(self, tiles):
        hit_list = collision_test(self.rect, tiles)
        for tile in hit_list:
            if self.movement[0] > 0:
                self.rect.right = tile.left
            elif self.movement[0] < 0:
                self.rect.left = tile.right