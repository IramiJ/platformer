import os, csv, pygame, math
from .torch import Torch
from .chandelier import Chandelier

def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    map = []
    for row in data:
        map.append(list(row))
    return map
def read_csv(filename):
    map = []
    with open(os.path.join(filename)) as data:
        data = csv.reader(data, delimiter=',')
        for row in data:
            map.append(list(row))
    return map
def last_x(map):
    counter = -1
    for i in map[0]:
        counter += 1
    return counter * 16
def load_tiles(path):
    dict = {}
    files = os.listdir(path)
    for file in files:
        name = str(int(file.split('.')[0]) - 1)
        dict[name] = pygame.image.load(path + '/' + file).convert()
        dict[name].set_colorkey((0,0,0))
    return dict

def load_torches(map, torch_list):
    torch_types = {"10": Torch, "12": Chandelier}
    y = 0
    torch_list.clear()
    for row in map:
        x = 0
        for tile in row:
            if tile == "10" or tile == "12":
                position = [x*16, y*16]
                torch_list.append(torch_types[tile](position))
            x += 1
        y += 1
    
'''
def display_map(display: pygame.Surface, scroll, tile_rects, map, dict):
    # TODO: optimize the rendering by only rendering whats actually needed
    y = 0
    for row in map:
        x = 0
        for tile in row:
            if tile != '-1' and tile != "10" and tile != "12":
                display.blit(dict[tile], (x*16-scroll.render_scroll[0], y*16-scroll.render_scroll[1]))
                if all(tile != str(x) for x in range(10,12)):
                    tile_rects.append(pygame.Rect(x*16,y*16,16,16))
            x += 1
        y += 1
'''

TILE = 16
SKIP_TILES = {"-1", "10", "12"}
def display_map(display: pygame.Surface, scroll, tile_rects, tilemap, tile_dict):

    scroll_x, scroll_y = scroll.render_scroll
    screen_w, screen_h = display.get_size()

    # visible tile range (add 1 tile padding to avoid pop-in)
    x0 = max(0, int(scroll_x // TILE) - 1)
    y0 = max(0, int(scroll_y // TILE) - 1)
    x1 = min(len(tilemap[0]), int(math.ceil((scroll_x + screen_w) / TILE)) + 1)
    y1 = min(len(tilemap),    int(math.ceil((scroll_y + screen_h) / TILE)) + 1)

    for y in range(y0, y1):
        row = tilemap[y]
        for x in range(x0, x1):
            tile = row[x]
            if tile in SKIP_TILES:
                continue

            world_x = x * TILE
            world_y = y * TILE

            display.blit(tile_dict[tile], (world_x - scroll_x, world_y - scroll_y))
            tile_rects.append(pygame.Rect(world_x, world_y, TILE, TILE))
