import os, csv, pygame
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
    

def display_map(display: pygame.Surface, scroll, tile_rects, map, dict):
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