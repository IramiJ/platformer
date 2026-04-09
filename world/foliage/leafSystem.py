import pygame, os
from .wind import Wind

class LeafSystem:
    def __init__(self):
        self.wind = Wind()
        self.leaf_imgs = []
        self.leaves = []
        for leaf in os.listdir(path := "tests/tree_test/leaves"):
            img_path = path + "/" + leaf
            self.leaf_imgs.append(img_path)
    def render_leaves(self, display: pygame.Surface, dt: float):
        for leaf in self.leaves[:]:
            leaf.render(display, dt)
            leaf.duration -= dt
            # optional cleanup when "dead" or off-screen:
            if leaf.duration <= 0 or leaf.loc[1] > 700:
                self.leaves.remove(leaf)
    
    def update_leaves(self, dt):
        for leaf in self.leaves[:]:
            leaf.update(self.wind, dt)