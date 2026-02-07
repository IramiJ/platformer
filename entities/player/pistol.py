import pygame

class Pistol:
    def __init__(self, x, y):
        self.loc = [x, y]
        self.img = pygame.image.load("assets/constants/pistol.png").convert()
        self.img.set_colorkey((0,0,0))
    def draw(self, player, display, scroll):
        sign = -1 if player.flip else 1
        if sign == 1:
            self.loc = [player.rect.right-6, player.rect.y+6]
        else:
            self.loc = [player.rect.left-self.img.get_width()+6, player.rect.y+6]
        display.blit(pygame.transform.flip(self.img, player.flip, False), [self.loc[0] - scroll.render_scroll[0], self.loc[1] - scroll.render_scroll[1]])