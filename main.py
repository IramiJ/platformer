

import pygame, sys
pygame.init()
from ui.Font_renderer import Font
from ui.shopping import Shop
from world.collisions import move
from world.tilemap import *
from entities.entity import *
from entities.player.player import Player
from core.settings import Settings
from entities.animations import draw_constants, load_animation
from entities.player.player_movements import player_movements
from world.scrolling import player_scrolling
from core.kb_event_handling import kb_events
from entities.player.tail import Tail
from entities.enemies.patroller import Patroller

clock = pygame.time.Clock()
#WINDOW-------------------------------------------------------------------------------------------------------------------------------------------------------------
window_size = [640, 480]
screen = pygame.display.set_mode(Settings.window_size)
display = pygame.Surface((320,240))
pygame.display.set_caption(Settings.caption)
#PLAYER----------------------------------------------------------------------------------------------------------------------------------------------------------------
player = Player(0,304,16,16)
#GAME MAP-------------------------------------------------------------------------------------------------------------------------------------------------------------
dict = load_tiles('assets/tiles')
map = read_csv('maps/map0.csv')
#ANIMATIONS-----------------------------------------------------------------------------------------------------------------------------------------------------------
cd = entity(player.x, player.y + 15, 16, 16)
cd.animation_database['idle'] = load_animation('assets/cooldown/idle', [8 for x in range(15)], cd)
tail = Tail('assets/tail/grey.png',[player.rect.x-2, player.rect.y+8])
#OTHERS-------------------------------------------------------------------------------------------------------------------------------------------------------------
small_font = Font('assets/fonts/small_font.png')
large_font = Font('assets/fonts/large_font.png')
coins = []
coin_amount = 1000
'''
for i in range(5):
    coins.append(simple_entity('assets/collectables/coin.png', [160*i, 308]))
'''
coins.append(simple_entity('assets/collectables/coin.png', [160, 308]))
shop = Shop()

enem = Patroller(48, 304, 16, 16)
#MAIN LOOP-------------------------------------------------------------------------------------------------------------------------------------------------------------
while True:              
    display.fill((0,0,0))
    
    player_scrolling(player, map)
    for coin in coins:
        coin.render(display, player.scroll)
        if coin.collision_test(player.rect):
            coins.remove(coin)
            if player.double_coin_buff:
                coin_amount += 2
            else:
                coin_amount += 1
    
    tile_rects = []
    display_map(display, player, tile_rects, map, dict)
    
    player.update_frames()
    player.draw(display)
    player_movements(player, tile_rects, display, cd, tail)

    enem.move()
    enem.update_frames()
    enem.render(display, player.scroll)

    draw_constants(display)
    large_font.render(display,str(coin_amount), (16,0))
    display.blit(pygame.image.load("assets/hp_bar/hp_bar.png"), (280, 0))
    player.dying()
    kb_events(player, shop)
    if shop.displaying:
        shop.render(display)
        player.moving_right = False
        player.moving_left = False
        coin_amount = shop.buy(coin_amount,player.buffs)
    player.apply_buffs()
    surf = pygame.transform.scale(display,Settings.window_size)
    screen.blit(surf, (0,0))
    pygame.display.update()
    clock.tick(Settings.fps)