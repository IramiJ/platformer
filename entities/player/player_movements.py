from world.collisions import move
from entities.entity import entity
from entities.animations import load_animation
from entities.player.tail import Tail
from core.settings import Settings
import pygame, math

def player_movements(player, tile_rects, display, cd, tail, scroll, dt):
    player.movement = [0, 0]
    if player.dashing:
        handle_player_dash(player, dt)
    else:   
        move_left(player, tail)
        move_right(player, tail)
        player.movement[1] += player.y_momentum
        tail.loc[1] = player.rect.y + 8
    
    
    set_player_y_momentum(player, dt)

    set_player_dash(player, dt, display, cd, scroll)
    
    determin_player_action(player)

    player.rect, collisions = move(player.rect, player.movement, tile_rects, dt)

    handle_velocity_collisions(collisions, player)
    
    tail.update_points()
    handle_tail_points(tail, display, scroll)

def handle_tail_points(tail, display, scroll):
    for i in range(len(tail.points)):
        if tail.points[i].show:
            tail.points[i].draw(display, scroll.render_scroll)
            tail.points[i].dur -= i    

def set_player_dash(player, dt, display, cd, scroll):
    if player.dash_cooldown > 0:
        player.dash_cooldown -= dt
        dash_cd(player, display, cd, scroll, dt)

def set_player_y_momentum(player, dt):
    player.y_momentum += 0.4 * dt
    if player.y_momentum > 7:
        player.y_momentum = 7

def determin_player_action(player):
    if player.movement[0] > 0:
        player.change_action('run')
        player.flip = False
    if player.movement[0] < 0:
        player.change_action('run')
        player.flip = True
    if player.movement[0] == 0:
        player.change_action('idle')

def move_right(player, tail):
    if player.moving_right:
        player.movement[0] += player.velocity
        for point in tail.points:
            point.show = True
        tail.loc[0] = player.rect.x - 1 + player.movement[0]
        tail.dir = 'r'

def move_left(player, tail):
    if player.moving_left:
        player.movement[0] -= player.velocity
        tail.loc[0] = player.rect.x + 17 + player.movement[0]
        for point in tail.points:
            point.show = True
        tail.dir = 'l'

def handle_player_dash(player, dt):
    player.y_momentum = 0
    player.movement[0] = player.dash_speed * (-1 if player.flip else 1)
    player.dash_timer -= 1 * dt
    if player.dash_timer <= 0:
        player.dashing = False    
    
def handle_velocity_collisions(collisions, player):
    if collisions['bottom']:
        player.y_momentum = 0
        player.air_timer = 0
    else:
        player.air_timer += 1

    if collisions['top']:
        player.y_momentum = 0    

def dash_cd(player, display, cd, scroll, dt):
    cd.img_id = cd.animation_database[cd.action][math.floor(cd.frame)]
    cd.img = cd.animation_frames[cd.img_id]
    display.blit(pygame.transform.flip(cd.img,cd.flip,False), [player.rect.x-scroll.render_scroll[0], player.rect.y-30-scroll.render_scroll[1]])
    cd.frame += dt
    if cd.frame >= len(cd.animation_database[cd.action]):
        cd.frame = 0
