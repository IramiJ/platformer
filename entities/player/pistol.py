import pygame

class Pistol:
    def __init__(self, x, y):
        self.loc = [x, y]
        self.img = pygame.image.load("assets/constants/pistol.png").convert()
        self.img.set_colorkey((0,0,0))
