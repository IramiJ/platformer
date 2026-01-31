

import pygame, random
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

clock = pygame.time.Clock()
window_size = [640, 480]
screen = pygame.display.set_mode(Settings.window_size)
display = pygame.Surface((320,240))
pygame.display.set_caption(Settings.caption)
player = Player(0,304,16,16)
dict = load_tiles('assets/tiles')
map = read_csv('maps/map0.csv')
hp_bar = Hp_bar("assets/hp_bar/hp_bar_bg.png","assets/hp_bar/hp_bar_frame.png", 280, 0)
small_font = Font('assets/fonts/small_font.png')
large_font = Font('assets/fonts/large_font.png')
coins = Coins()

shop = Shop()

enemies = Enemies()
bullets = []

scroll = Scroll()

#MAIN LOOP-------------------------------------------------------------------------------------------------------------------------------------------------------------
while True:              
    display.fill((0,0,0))
    
    scroll.player_scrolling(player, map)
#    scroll.shake_offset = [random.randint(-4, 4), random.randint(-4, 4)] Shake test
    coins.handle_coins(display, player, scroll)
    
    tile_rects = []
    display_map(display, scroll, tile_rects, map, dict)
    
    player.update_frames()
    player.draw(display, scroll)
    player_movements(player, tile_rects, display, player.cd_obj, player.tail, scroll)

    enemies.handle_enemies(player, display, bullets, scroll)

    for bullet in bullets:
        bullet.move(player, display, bullets, scroll)
    
    draw_constants(display)
    large_font.render(display,str(coins.amount), (16,0))
    hp_bar.draw(display, 5, player.hp)
    player.dying()
    kb_events(player, shop)
    shop.show(display, player, coins.amount)
    player.apply_buffs()
    surf = pygame.transform.scale(display,Settings.window_size)
    screen.blit(surf, (0,0))
    pygame.display.update()
    clock.tick(Settings.fps)