import pygame, sys, os, random, math
pygame.init()

screen = pygame.display.set_mode((500, 500))
display = pygame.Surface((250, 250))
clock = pygame.time.Clock()



class Wind:
    def __init__(self):
        self.current = 0.0
        self.target = 0.0
        self.timer = 0.0
        self.gust_strength = 0.0
        self.gust_time = 0.0
        self.winding = False
        self.leaf_spawn_rate = 5
    def update(self, dt):
        if self.winding:
            self.wind_up()
            self.leaf_spawn_rate = 2
        else:
            self.leaf_spawn_rate = 5
        if self.gust_time > 0:
            fade = max(0, self.gust_time)
            self.target = self.gust_strength * min(1, fade * 2)
            self.gust_time -= dt
        else:
            self.target = random.uniform(-0.5, 0.2)
        self.current += (self.target - self.current) * 0.05

    def wind_up(self):
        self.gust_strength = random.uniform(-6.0, -3.0)  
        self.gust_time = random.uniform(0.8, 2.0)
wind = Wind()
class Leaf:
    def __init__(self, img, loc, duration):
        self.img = pygame.image.load(img).convert()
        self.img.set_colorkey((0,0,0))

        self.loc = [float(loc[0]), float(loc[1])]
        self.max_duration = duration
        self.duration = float(self.max_duration)

        w, h = self.img.get_width(), self.img.get_height()
        self.rect = pygame.FRect(self.loc[0], self.loc[1], w, h)

        self.vx = random.uniform(-0.2, 0.2)
        self.vy = random.uniform(0.1, 0.6)

        self.gravity = random.uniform(0.015, 0.03)     
        self.drag = random.uniform(0.985, 0.995)       
        self.terminal_vy = random.uniform(1.2, 2.2)    


        self.phase = random.uniform(0, math.tau)
        self.flutter_amp = random.uniform(0.15, 0.5)
        self.flutter_speed = random.uniform(2.0, 5.0)

    def render(self, display: pygame.Surface, dt: float):
        self.update(dt)
        display.blit(self.img, (self.loc[0], self.loc[1]))

    def update(self, dt: float):
        self.phase += self.flutter_speed * dt
        flutter = math.sin(self.phase) * self.flutter_amp

        self.vy += self.gravity * (dt * 60)                 
        self.vx += (wind.current + flutter) * 0.02 * (dt * 60) 

        drag = self.drag ** (dt * 60)
        self.vx *= drag
        self.vy *= drag

        if self.vy > self.terminal_vy:
            self.vy = self.terminal_vy

        self.loc[0] += self.vx * (dt * 60)
        self.loc[1] += self.vy * (dt * 60)

        self.rect.x, self.rect.y = self.loc[0], self.loc[1]
    
class Tree:
    def __init__(self, loc):
        self.img = pygame.image.load("tree.png").convert()
        self.img.set_colorkey((0,0,0))
        self.loc = loc
    def render(self, display: pygame.Surface):
        display.blit(self.img, self.loc)
    def add_leaves(self, leaf_imgs, leaf_list):
        loc = self.loc.copy()
        loc[0] += random.randint(0, 40)
        loc[1] += random.randint(0, 10)
        leaf_list.append(Leaf(leaf_imgs[random.randint(0, 8)], loc, random.randint(1, 10)))

leaf_imgs = []
leaf_list = []
def load_leaves(path):
    for leaf in os.listdir(path):
        img_path = path + "/" + leaf
        leaf_imgs.append(img_path)



def render_leaves(surface: pygame.Surface, leaf_list, dt: float):
    for leaf in leaf_list[:]:
        leaf.render(surface, dt)
        leaf.duration -= dt
        # optional cleanup when "dead" or off-screen:
        if leaf.duration <= 0 or leaf.loc[1] > 260:
            leaf_list.remove(leaf)

t1 = Tree([100,100])
load_leaves("leaves")
while True:
    dt = clock.tick(60) / 1000
    wind.update(dt)
    display.fill((0,0,0))
    t1.render(display)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                wind.winding = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                wind.winding = False

    if random.randint(1, wind.leaf_spawn_rate) == 1:
        t1.add_leaves(leaf_imgs, leaf_list)
    render_leaves(display, leaf_list, dt)
    
    screen.blit(pygame.transform.scale(display, (500, 500)))
    print(wind.leaf_spawn_rate)
    pygame.display.update()
    