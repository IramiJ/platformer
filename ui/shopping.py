import pygame, os, time
from ui.Font_renderer import Font
pygame.init()
small_font = Font('assets/fonts/small_font.png')
large_font = Font('assets/fonts/large_font.png')
path = 'assets/shop_items'
imgs = {}
files = os.listdir(path)
global counter
counter = 1
item_boxes = {}
global buy_cooldown
buy_cooldown = 0
prices = {'speed_boost': '5', 'double_coins': '5', 'jump_boost': '5'}
class Shop():
    def __init__(self):
        global counter
        self.displaying = False
        for file in files:
            name = file.split('.')[0]
            imgs[name] = pygame.image.load(path + '/' + file).convert(), [0, 32 * counter]
            item_boxes[name] = pygame.Rect(imgs[name][1][0],imgs[name][1][1],imgs[name][0].get_width(),imgs[name][0].get_height())
            counter += 1
    def render(self,surf):
        surf.fill((0,0,0))
        large_font.render(surf,'SHOP',(150,0))  
        for item in imgs:
            small_font.render(surf,item,(0,imgs[item][1][1]-8))
            large_font.render(surf,prices[item],[36,imgs[item][1][1]+2])
            surf.blit(imgs[item][0], (item_boxes[item].x,item_boxes[item].y))
    def buy(self, currency, buff_list):
        global buy_cooldown
        for item in imgs:
            if pygame.mouse.get_pressed()[0]:
                mouse_rect = pygame.Rect(pygame.mouse.get_pos()[0]/2, pygame.mouse.get_pos()[1]/2,1,1)
                if mouse_rect.colliderect(item_boxes[item]):
                    if currency >= int(prices[item]) and buy_cooldown == 0:
                        currency -= int(prices[item])
                        buy_cooldown = 0
                        buff_list.append(item)
                    else:
                        pass
        return currency
    def change_displaying(self):
        self.displaying = not self.displaying
        return self.displaying
    def show(self, display, player, coin_amount):
        if self.displaying:
            self.render(display)
            player.moving_right = False
            player.moving_left = False
            coin_amount = self.buy(coin_amount,player.buffs)