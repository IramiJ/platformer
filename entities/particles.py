import pygame, random

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
        self.loc[1] += random.randint(1, 10) / 100
        display.blit(self.img, [self.loc[0]+self.x_velocity-scroll.render_scroll[0], self.loc[1]+self.y_velocity-scroll.render_scroll[1]])
