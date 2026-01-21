from world.tilemap import last_x
def player_scrolling(player, map):
    if player.rect.x < 150:
        #player.scroll[0] += player.rect.x - player.scroll[0] -150 + (150-player.rect.x) 
        player.scroll[0] -= player.scroll[0]
    elif player.rect.x + 16 > last_x(map) - 150:
        #player.scroll[0] += player.rect.x - player.scroll[0] -300 + (last_x(map)-player.rect.x) 
        player.scroll[0]  += -player.scroll[0] -300 + last_x(map)
    else:
        player.scroll[0] += player.rect.x - player.scroll[0] -150
    player.scroll[1] += player.rect.y - player.scroll[1] - 100