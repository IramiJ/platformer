import pygame, sys
from entities.player.player_movements import dash
def kb_events(player, shop):
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
                if event.key == pygame.K_e:
                    dash(player)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    player.moving_right = False
                if event.key == pygame.K_LEFT:
                    player.moving_left = False