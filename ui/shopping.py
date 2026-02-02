import pygame, os, time
from ui.Font_renderer import Font
pygame.init()
small_font = Font('assets/fonts/small_font.png')
large_font = Font('assets/fonts/large_font.png')

class Shop():
    def __init__(self):
        self.path = 'assets/shop_items'
        self.files = os.listdir(self.path)
        self.buy_cooldown = 0
        counter = 1
        self.item_boxes = {}
        self.displaying = False
        self.imgs = {}
        self.prices = {'speed_boost': '5', 'double_coins': '5', 'jump_boost': '5'}
        for file in self.files:
            name = file.split('.')[0]
            self.imgs[name] = pygame.image.load(self.path + '/' + file).convert(), [0, 32 * counter]
            self.item_boxes[name] = pygame.Rect(self.imgs[name][1][0],self.imgs[name][1][1],self.imgs[name][0].get_width(),self.imgs[name][0].get_height())
            counter += 1
    def render(self,surf):
        surf.fill((0,0,0))
        large_font.render(surf,'SHOP',(150,0))  
        for item in self.imgs:
            small_font.render(surf,item,(0,self.imgs[item][1][1]-8))
            large_font.render(surf,self.prices[item],[36,self.imgs[item][1][1]+2])
            surf.blit(self.imgs[item][0], (self.item_boxes[item].x,self.item_boxes[item].y))
    def buy(self, currency, buff_list):
        for item in self.imgs:
            if pygame.mouse.get_pressed()[0]:
                mouse_rect = pygame.Rect(pygame.mouse.get_pos()[0]/2, pygame.mouse.get_pos()[1]/2,1,1)
                if mouse_rect.colliderect(self.item_boxes[item]):
                    if currency >= int(self.prices[item]) and self.buy_cooldown == 0 and item not in buff_list:
                        currency -= int(self.prices[item])
                        self.buy_cooldown = 0
                        buff_list.append(item)
                    else:
                        pass
        return currency
    def change_displaying(self):
        self.displaying = not self.displaying
        return self.displaying
    def show(self, display, player, coin_amount, logic_variables):
        if self.displaying:
            logic_variables.MOVEMENTS = False
            self.render(display)
            player.moving_right = False
            player.moving_left = False
            coin_amount = self.buy(coin_amount,player.buffs)
        else:
            logic_variables.MOVEMENTS = True