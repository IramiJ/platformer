

import pygame, sys, os
pygame.init()
from ui.Font_renderer import Font
from ui.shopping import Shop
from world.collisions import move
from world.tilemap import *
from entities.entity import *
from entities.player import Player
from core.settings import Settings
from entities.animations import draw_constants

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
map = read_csv('map0.csv')
#COLLISIONS-----------------------------------------------------------------------------------------------------------------------------------------------------------

#ANIMATOINS-----------------------------------------------------------------------------------------------------------------------------------------------------------
global animation_frames
animation_frames = {}
def load_animation(path,dur):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in dur:
        animation_frame_id = animation_name + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((0,0,0))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n +=1 
    return animation_frame_data
player.animation_database['idle'] = load_animation('assets/char/idle', [15, 15])
player.animation_database['run'] = load_animation('assets/char/run', [5,5,5,5])

coins = []
coin_amount = 1000
for i in range(5):
    coins.append(simple_entity('assets/collectables/coin.png', [160*i, 308]))
#OTHERS-------------------------------------------------------------------------------------------------------------------------------------------------------------
small_font = Font('assets/fonts/small_font.png')
large_font = Font('assets/fonts/large_font.png')
shop = Shop()
#MAIN LOOP-------------------------------------------------------------------------------------------------------------------------------------------------------------
while True:              
    display.fill((0,0,0))
    for coin in coins:
        coin.render(display, player.scroll)
        if coin.collision_test(player.rect):
            coins.remove(coin)
            if player.double_coin_buff:
                coin_amount += 2
            else:
                coin_amount += 1
    if player.rect.x < 150:
        player.scroll[0] += player.rect.x - player.scroll[0] -150 + (150-player.rect.x) 
    elif player.rect.x + 16 > last_x(map) - 150:
        player.scroll[0] += player.rect.x - player.scroll[0] -300 + (last_x(map)-player.rect.x) 
    else:
        player.scroll[0] += player.rect.x - player.scroll[0] -150
    player.scroll[1] += player.rect.y - player.scroll[1] - 100
    tile_rects = []
    y = 0
    for row in map:
        x = 0
        for tile in row:
            if tile != '-1':
                display.blit(dict[tile], (x*16-player.scroll[0], y*16-player.scroll[1]))
                if tile != '9' and tile != '10' and tile != '11':
                    tile_rects.append(pygame.Rect(x*16,y*16,16,16))
            x += 1
        y += 1

    player.y_momentum += 0.2

    player.movement = [0, 0]
    if player.moving_right:
        player.movement[0] += player.velocity
    if player.moving_left:
        player.movement[0] -= player.velocity
    player.movement[1] += player.y_momentum
    player.y_momentum += 0.2
    if player.y_momentum > 7:
        player.y_momentum = 7
    
    if player.movement[0] > 0:
        player.change_action('run')
        player.flip = False
    if player.movement[0] < 0:
        player.change_action('run')
        player.flip = True
    if player.movement[0] == 0:
        player.change_action('idle')

    player.rect, collisions = move(player.rect, player.movement, tile_rects)

    if collisions['bottom']:
        player.y_momentum = 0
        player.air_timer = 0
    else:
        player.air_timer += 1

    if collisions['top']:
        player.y_momentum = 0

    player.frame += 1
    if player.frame >= len(player.animation_database[player.action]):
        player.frame = 0
    player.img_id = player.animation_database[player.action][player.frame]
    player.img = animation_frames[player.img_id]
    display.blit(pygame.transform.flip(player.img,player.flip,False), [player.rect.x-player.scroll[0], player.rect.y-player.scroll[1]])
    draw_constants(display)
    large_font.render(display,str(coin_amount), (16,0))
    player.dying()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.moving_right = True
            if event.key == pygame.K_LEFT:
                player.moving_left = True
            if event.key == pygame.K_SPACE:
                if player.air_timer < 6:
                    player.y_momentum = player.jump_momentum
            if event.key == pygame.K_b:
                shop.change_displaying()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.moving_right = False
            if event.key == pygame.K_LEFT:
                player.moving_left = False
    if shop.displaying:
        shop.render(display)
        player.moving_right = False
        player.moving_left = False
        coin_amount = shop.buy(coin_amount,player.buffs)
    player.apply_buffs()
    surf = pygame.transform.scale(display,Settings.window_size)
    screen.blit(surf, (0,0))
    pygame.display.update()
    clock.tick(60)