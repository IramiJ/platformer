from world.collisions import move
from entities.entity import entity
from entities.animations import load_animation
from entities.player.tail import Tail
from core.settings import Settings
import pygame, math

def player_movements(player, tile_rects, display, cd, tail, scroll):
    player.movement = [0, 0]
    if player.dashing:
        player.y_momentum = 0
        player.movement[0] = player.dash_speed * (-1 if player.flip else 1)
        player.dash_timer -= 1
        if player.dash_timer <= 0:
            player.dashing = False
    else:   
        if player.moving_right:
            player.movement[0] += player.velocity
            for point in tail.points:
                point.show = True
            tail.loc[0] = player.rect.x - 1 + player.movement[0]
            tail.dir = 'r'
        if player.moving_left:
            player.movement[0] -= player.velocity
            tail.loc[0] = player.rect.x + 17 + player.movement[0]
            for point in tail.points:
                point.show = True
            tail.dir = 'l'
        player.movement[1] += player.y_momentum
        tail.loc[1] = player.rect.y + 8
    
    
    player.y_momentum += 0.4
    if player.y_momentum > 7:
        player.y_momentum = 7
    if player.dash_cooldown > 0:
        player.dash_cooldown -= 1
        dash_cd(player, display, cd, scroll)
        
    
    if player.movement[0] > 0:
        if player.mode == "meele":
            player.change_action('run_meele')
        else:
            player.change_action('run_ranged')
        player.flip = False
    if player.movement[0] < 0:
        if player.mode == "meele":
            player.change_action('run_meele')
        else:
            player.change_action('run_ranged')
        player.flip = True
    if player.movement[0] == 0:
        if player.mode == "meele":
            player.change_action('idle_meele')
        else:
            player.change_action('idle_ranged')
    player.rect, collisions = move(player.rect, player.movement, tile_rects)

    if collisions['bottom']:
        player.y_momentum = 0
        player.air_timer = 0
    else:
        player.air_timer += 1

    if collisions['top']:
        player.y_momentum = 0
    
    tail.update_points()
    for i in range(len(tail.points)):
        if tail.points[i].show:
            tail.points[i].draw(display, scroll.render_scroll)
            tail.points[i].dur -= i
    
    
    
    


def dash_cd(player, display, cd, scroll):
    cd.img_id = cd.animation_database[cd.action][cd.frame]
    cd.img = cd.animation_frames[cd.img_id]
    display.blit(pygame.transform.flip(cd.img,cd.flip,False), [player.rect.x-scroll.render_scroll[0], player.rect.y-30-scroll.render_scroll[1]])
    cd.frame += 1
    if cd.frame >= len(cd.animation_database[cd.action]):
        cd.frame = 0
