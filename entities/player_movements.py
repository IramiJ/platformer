from world.collisions import move
from entities.entity import entity
from entities.animations import load_animation
import pygame

def player_movements(player, tile_rects, display, cd):
    player.movement = [0, 0]
    if player.dashing:
        player.movement[0] = player.dash_speed * (-1 if player.flip else 1)
        player.dash_timer -= 1
        if player.dash_timer <= 0:
            player.dashing = False
    else:   
        if player.moving_right:
            player.movement[0] += player.velocity
        if player.moving_left:
            player.movement[0] -= player.velocity
        player.movement[1] += player.y_momentum
    player.y_momentum += 0.4
    if player.y_momentum > 7:
        player.y_momentum = 7
    if player.dash_cooldown > 0:
        player.dash_cooldown -= 1
        dash_cd(player, display, cd)
        
    
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
    
    

def dash(player):
    if not player.dashing and player.dash_cooldown == 0:           
        player.dashing = True
        player.dash_timer = player.dash_duration
        player.dash_cooldown = 120
def dash_cd(player, display, cd):
    cd.img_id = cd.animation_database[cd.action][cd.frame]
    cd.img = cd.animation_frames[cd.img_id]
    display.blit(pygame.transform.flip(cd.img,cd.flip,False), [player.rect.x-player.scroll[0], player.rect.y-30-player.scroll[1]])
    cd.frame += 1
    if cd.frame >= len(cd.animation_database[cd.action]):
        cd.frame = 0
