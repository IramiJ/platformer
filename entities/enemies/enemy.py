from entities.entity import entity
import pygame

class Enemy(entity):
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height)
        self.hp = 3
        self.velocity = 1
        self.alive = True
    def update_frames(self):
        self.frame += 1
        if self.frame >= len(self.animation_database[self.action]):
            self.frame = 0
        self.img_id = self.animation_database[self.action][self.frame]
        self.img = self.animation_frames[self.img_id]
    def draw(self, display, scroll):
        display.blit(pygame.transform.flip(self.img,self.flip,False), [self.rect.x-scroll[0], self.rect.y-scroll[1]])
    def take_dmg(self):
        if not self.alive:
            return
        self.hp -= 1
        if self.hp <= 0:
            self.hp = 0
            self.alive = False