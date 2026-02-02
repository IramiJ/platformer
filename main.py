

import pygame, random

from ui.death_screen import Death_screen
pygame.init()
from ui.Font_renderer import Font
from ui.shopping import Shop
from world.tilemap import *
from entities.entity import *
from entities.player.player import Player
from entities.hp_bar import Hp_bar
from core.settings import Settings
from entities.animations import draw_constants, load_animation
from entities.player.player_movements import player_movements
from world.scrolling import Scroll
from core.kb_event_handling import kb_events
from entities.player.tail import Tail
from entities.enemies.enemies import Enemies
from entities.coins import Coins
from world.level_loader import Level_loader, update_level, reach_checkpoint
from core.logic_variables import Logic_variables
from ui.pause_screen import Pause_screen

clock = pygame.time.Clock()
window_size = [640, 480]
screen = pygame.display.set_mode(Settings.window_size)
display = pygame.Surface((320,240))
pygame.display.set_caption(Settings.caption)

tiles = load_tiles('assets/tiles')
level = Level_loader()
level.load_level('world/levels/level1.json')
player = Player(level.data['spawn'][0],level.data['spawn'][1],16,16)
hp_bar = Hp_bar("assets/hp_bar/hp_bar_bg.png","assets/hp_bar/hp_bar_frame.png", 280, 0)
small_font = Font('assets/fonts/small_font.png')
large_font = Font('assets/fonts/large_font.png')
coins = Coins()
logic_variables = Logic_variables() 
shop = Shop()
pause_screen = Pause_screen()
death_screen = Death_screen()
enemies = Enemies()
enemies.load_enemies(level)
bullets = []

scroll = Scroll()

#MAIN LOOP-------------------------------------------------------------------------------------------------------------------------------------------------------------
while True:              
    
    # Draw logic  
    if logic_variables.RENDER:  
        display.fill((0,0,0))
        coins.draw_coins(display, scroll)
        draw_constants(display)
        tile_rects = []
        display_map(display, scroll, tile_rects, level.map, tiles)
        player.update_frames()
        player.draw(display, scroll)
        large_font.render(display,str(coins.amount), (16,0))
        hp_bar.draw(display, 5, player.hp)

    # Movement logic
    if logic_variables.MOVEMENTS:
        player_movements(player, tile_rects, display, player.cd_obj, player.tail, scroll)
        coins.coin_collisions(player)
        enemies.handle_enemies(player, display, bullets, scroll, tile_rects)
        scroll.player_scrolling(player, level)
        for bullet in bullets:
            bullet.move(player, display, bullets, scroll)
        player.dying(level.data["max_y"])
        player.apply_buffs()
    if shop.displaying:
        shop.show(display, player, coins.amount, logic_variables)
    elif pause_screen.displaying:
        pause_screen.render(display, logic_variables)
    elif player.hp <= 0:
        death_screen.render(display, logic_variables)
    else:
        logic_variables.MOVEMENTS = True
        logic_variables.RENDER = True
    kb_events(player, shop, pause_screen)
    
    
    surf = pygame.transform.scale(display,Settings.window_size)
    update_level(player, level, enemies)
    reach_checkpoint(player, level)
    screen.blit(surf, (0,0))
    pygame.display.update()
    clock.tick(Settings.fps)