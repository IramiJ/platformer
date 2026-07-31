import pygame
import random
from .leaf import Leaf
from core.settings import REFERENCE_TICKS_PER_SECOND
from core.paths import assets_path

LEAF_SPAWNS_PER_SECOND = REFERENCE_TICKS_PER_SECOND / 11.0


class Tree:
    def __init__(self, loc):
        self.img = pygame.image.load(assets_path("foliage/tree.png")).convert()
        self.img.set_colorkey((0, 0, 0))
        self.loc = loc
        self.leaf_spawn_timer = self.next_leaf_spawn_delay()

    def render(self, display, scroll):
        display.blit(
            self.img,
            [
                self.loc[0] - scroll.render_scroll[0],
                self.loc[1] - scroll.render_scroll[1],
            ],
        )

    def next_leaf_spawn_delay(self):
        return random.expovariate(LEAF_SPAWNS_PER_SECOND)

    def generate_leaves(self, leaf_imgs, leaf_list, dt):
        self.leaf_spawn_timer -= dt

        while self.leaf_spawn_timer <= 0:
            self.spawn_leaf(leaf_imgs, leaf_list)
            self.leaf_spawn_timer += self.next_leaf_spawn_delay()

    def spawn_leaf(self, leaf_imgs, leaf_list):
        loc = self.loc.copy()
        loc[0] += random.randint(0, 40)
        loc[1] += random.randint(0, 10)
        leaf_list.append(Leaf(random.choice(leaf_imgs), loc, random.randint(1, 10)))
