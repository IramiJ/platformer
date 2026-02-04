import pygame, random, math

class Particle:
    def __init__(self, img, loc, duration):
        self.img = pygame.image.load(img).convert()
        self.img.set_colorkey((0,0,0))
        self.loc = loc
        self.max_duration = duration
        self.duration = int(self.max_duration)
        self.rect = pygame.FRect(self.loc[0], self.loc[1], self.img.get_width(), self.img.get_height())
        self.x_velocity = 0
        self.y_velocity = 0.2
    def render(self, display, scroll):
        self.increase_velocity()
        self.loc[0] += self.x_velocity
        self.loc[1] += self.y_velocity
        display.blit(self.img, [self.loc[0]-scroll.render_scroll[0], self.loc[1]-scroll.render_scroll[1]])
    def increase_velocity(self):
        self.y_velocity += 0.01
        self.x_velocity = random.randint(-10, 10) / 30
