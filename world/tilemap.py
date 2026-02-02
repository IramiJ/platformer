import os, csv, pygame


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

def display_map(display: pygame.Surface, scroll, tile_rects, map, dict):
    y = 0
    for row in map:
        x = 0
        for tile in row:
            if tile != '-1':
                display.blit(dict[tile], (x*16-scroll.render_scroll[0], y*16-scroll.render_scroll[1]))
                if all(tile != str(x) for x in range(9, 14)):
                    tile_rects.append(pygame.Rect(x*16,y*16,16,16))
            x += 1
        y += 1