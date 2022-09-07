

import pygame, sys, os, csv
pygame.init()
from Font_renderer import Font
from shopping import Shop

clock = pygame.time.Clock()
#WINDOW-------------------------------------------------------------------------------------------------------------------------------------------------------------
window_size = [640, 480]
screen = pygame.display.set_mode(window_size)
display = pygame.Surface((320,240))
pygame.display.set_caption("cat game")
#PLAYER----------------------------------------------------------------------------------------------------------------------------------------------------------------
moving_left = False
moving_right = False
global velocity
global jump_momentum
global double_coin_buff
velocity = 2
y_momentum = 0
jump_momentum = -10
double_coin_buff = False
air_timer = 0
coin_amount = 1000
class entity():
    def __init__(self,x,y,width,height):
        self.x = x 
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.action = 'idle'
        self.frame = 0
        self.img_id = None
        self.flip = False
        self.img = None
        self.movement = [0,0]
        self.animation_database = {}

class simple_entity():
    def __init__(self,img,loc):
        self.loc = loc
        self.img = pygame.image.load(img).convert()
    def render(self,surf,scroll):
        surf.blit(self.img, (self.loc[0]-scroll[0], self.loc[1]-scroll[1]))
    def get_rect(self):
        return pygame.Rect(self.loc[0], self.loc[1], self.img.get_width(), self.img.get_height())
    def collision_test(self, rect):
        r = self.get_rect()
        return r.colliderect(rect)

coins = []
for i in range(5):
    coins.append(simple_entity('assets/collectables/coin.png', [160*i, 308]))

player = entity(0,304,16,16)
player.buffs = []
#BUFFS----------------------------------------------------------------------------------------------------------------------------------------------------------------
def apply_buffs():
    global double_coin_buff
    global velocity
    global jump_momentum
    for buff in player.buffs:
        if buff == 'speed_boost':
            velocity = 4
        if buff == 'jump_boost':
            jump_momentum = -15
        if buff == 'double_coins':
            double_coin_buff = True
def load_tiles(path):
    dict = {}
    files = os.listdir(path)
    for file in files:
        name = str(int(file.split('.')[0]) - 1)
        dict[name] = pygame.image.load(path + '/' + file).convert()
        dict[name].set_colorkey((0,0,0))
    return dict
dict = load_tiles('assets/tiles')
#GAME MAP-------------------------------------------------------------------------------------------------------------------------------------------------------------
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
map = read_csv('map0.csv')
def last_x(map):
    counter = -1
    for i in map[0]:
        counter += 1
    return counter * 16
    
#COLLISIONS-----------------------------------------------------------------------------------------------------------------------------------------------------------
def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types
scroll = [0,0]
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
player.animation_database = {}
player.animation_database['idle'] = load_animation('assets/char/idle', [15, 15])
player.animation_database['run'] = load_animation('assets/char/run', [5,5,5,5])

def change_action(action_var, frame, new_action):
    if action_var != new_action:
        action_var = new_action
        frame = 0
    return action_var, frame
#DYING----------------------------------------------------------------------------------------------------------------------------------------------------------------
def dying():
    if player.rect.y > 500:
        player.rect.x = 0
        player.rect.y = 304
#OTHERS-------------------------------------------------------------------------------------------------------------------------------------------------------------
def draw_constants():
    coin_count = pygame.image.load('assets/constants/coins.png').convert()
    display.blit(coin_count, (0,0))
small_font = Font('assets/fonts/small_font.png')
large_font = Font('assets/fonts/large_font.png')
shop = Shop()
#MAIN LOOP-------------------------------------------------------------------------------------------------------------------------------------------------------------
while True:              
    display.fill((0,0,0))
    for coin in coins:
        coin.render(display, scroll)
        if coin.collision_test(player.rect):
            coins.remove(coin)
            if double_coin_buff:
                coin_amount += 2
            else:
                coin_amount += 1
    if player.rect.x < 150:
        scroll[0] += player.rect.x - scroll[0] -150 + (150-player.rect.x) 
    elif player.rect.x + 16 > last_x(map) - 150:
        scroll[0] += player.rect.x - scroll[0] -300 + (last_x(map)-player.rect.x) 
    else:
        scroll[0] += player.rect.x - scroll[0] -150
    scroll[1] += player.rect.y - scroll[1] - 100
    tile_rects = []
    y = 0
    for row in map:
        x = 0
        for tile in row:
            if tile != '-1':
                display.blit(dict[tile], (x*16-scroll[0], y*16-scroll[1]))
                if tile != '9' and tile != '10' and tile != '11':
                    tile_rects.append(pygame.Rect(x*16,y*16,16,16))
            x += 1
        y += 1

    y_momentum += 0.2

    player.movement = [0, 0]
    if moving_right:
        player.movement[0] += velocity
    if moving_left:
        player.movement[0] -= velocity
    player.movement[1] += y_momentum
    y_momentum += 0.2
    if y_momentum > 7:
        y_momentum = 7
    
    if player.movement[0] > 0:
        player.action, player.frame = change_action(player.action,player.frame,'run')
        player.flip = False
    if player.movement[0] < 0:
        player.action, player.frame = change_action(player.action,player.frame,'run')
        player.flip = True
    if player.movement[0] == 0:
        player.action, player.frame = change_action(player.action,player.frame,'idle')

    player.rect, collisions = move(player.rect, player.movement, tile_rects)

    if collisions['bottom']:
        y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

    if collisions['top']:
        y_momentum = 0

    player.frame += 1
    if player.frame >= len(player.animation_database[player.action]):
        player.frame = 0
    player.img_id = player.animation_database[player.action][player.frame]
    player.img = animation_frames[player.img_id]
    display.blit(pygame.transform.flip(player.img,player.flip,False), [player.rect.x-scroll[0], player.rect.y-scroll[1]])
    draw_constants()
    large_font.render(display,str(coin_amount), (16,0))
    dying()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_SPACE:
                if air_timer < 6:
                    y_momentum = jump_momentum
            if event.key == pygame.K_b:
                shop.change_displaying()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_LEFT:
                moving_left = False
    if shop.displaying:
        shop.render(display)
        moving_right = False
        moving_left = False
        coin_amount = shop.buy(coin_amount,player.buffs)
    apply_buffs()
    surf = pygame.transform.scale(display,window_size)
    screen.blit(surf, (0,0))
    pygame.display.update()
    clock.tick(60)