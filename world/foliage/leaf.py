import pygame, random, math

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

    def render(self, display: pygame.Surface, scroll):
        display.blit(self.img, (self.loc[0]-scroll.render_scroll[0], self.loc[1] - scroll.render_scroll[1]))

    def update(self, wind,  dt: float):
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