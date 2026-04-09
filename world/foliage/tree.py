import pygame, random
from .leaf import Leaf

class Tree:
    def __init__(self, loc):
        self.img = pygame.image.load("tests/tree_test/tree.png").convert()
        self.img.set_colorkey((0,0,0))
        self.loc = loc
    def render(self, display, scroll):
        display.blit(self.img, [self.loc[0]- scroll.render_scroll[0], self.loc[1] - scroll.render_scroll[1]])
    def generate_leaves(self, leaf_imgs, leaf_list):
        loc = self.loc.copy()
        loc[0] += random.randint(0, 40)
        loc[1] += random.randint(0, 10)
        leaf_list.append(Leaf(leaf_imgs[random.randint(0, 8)], loc, random.randint(1, 10)))