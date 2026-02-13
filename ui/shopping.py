import pygame, os, json
from ui.Font_renderer import Font
pygame.init()
small_font = Font('assets/fonts/small_font.png')
large_font = Font('assets/fonts/large_font.png')

class Shop():
    def __init__(self):
        with open("ui/shop.json", "r") as file:
            self.data = json.load(file)
        self.buy_cooldown = 0
        counter = 1
        self.item_boxes = {}
        self.displaying = False
        self.imgs = {}
        self.prices = {}
        for entry in self.data:
            self.prices[entry] = str(self.data[entry]["price"])
            self.imgs[entry] = pygame.image.load(self.data[entry]["asset_path"]).convert(), [0, 32 * counter]
            self.item_boxes[entry] = pygame.Rect(self.imgs[entry][1][0],self.imgs[entry][1][1],self.imgs[entry][0].get_width(),self.imgs[entry][0].get_height())
            counter += 1
    def render(self,surf):
        surf.fill((0,0,0))
        large_font.render(surf,'SHOP',(150,0))  
        for item in self.imgs:
            small_font.render(surf,item,(0,self.imgs[item][1][1]-8))
            large_font.render(surf,self.prices[item],[36,self.imgs[item][1][1]+2])
            small_font.render(surf, "duration: " + str(self.data[item]["duration"]), [60,self.imgs[item][1][1]+2]), 
            surf.blit(self.imgs[item][0], (self.item_boxes[item].x,self.item_boxes[item].y))
    def buy(self, player, buff_list):
        for item in self.imgs:
            if pygame.mouse.get_pressed()[0]:
                mouse_rect = pygame.Rect(pygame.mouse.get_pos()[0]/2, pygame.mouse.get_pos()[1]/2,1,1)
                if mouse_rect.colliderect(self.item_boxes[item]):
                    if player.coin_amount >= int(self.prices[item]) and self.buy_cooldown == 0 and item not in buff_list:
                        player.coin_amount -= int(self.prices[item])
                        self.buy_cooldown = 0
                        buff_list[item] = int(self.data[item]["duration"]) * 60
    def change_displaying(self):
        self.displaying = not self.displaying
        return self.displaying
    def show(self, display, player):
        if self.displaying:
            self.render(display)
            player.moving_right = False
            player.moving_left = False
            self.buy(player,player.buffs)