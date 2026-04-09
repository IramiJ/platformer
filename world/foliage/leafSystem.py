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

    def render_leaves(self, display: pygame.Surface, scroll):
        for leaf in self.leaves[:]:
            leaf.render(display, scroll)
            if leaf.duration <= 0:
                self.leaves.remove(leaf)
    
    def update_leaves(self, dt):
        dt_seconds = dt / 60
        self.wind.update(dt_seconds)
        for leaf in self.leaves[:]:
            leaf.update(self.wind, dt_seconds)
            leaf.duration -= dt_seconds
