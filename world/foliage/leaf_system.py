from __future__ import annotations

import os
from typing import TYPE_CHECKING

from core.asset_cache import load_image_file
from core.paths import require_asset_dir
from core.settings import REFERENCE_TICKS_PER_SECOND

from .wind import Wind

if TYPE_CHECKING:
    import pygame

    from world.scrolling import Scroll

    from .leaf import Leaf
    from .tree import Tree

FOLIAGE_SIMULATION_STEP = 1.0 / REFERENCE_TICKS_PER_SECOND


class LeafSystem:
    def __init__(self) -> None:
        self.wind = Wind()
        self.update_accumulator = 0.0
        self.leaf_imgs: list[pygame.Surface] = []
        self.leaves: list[Leaf] = []
        for leaf in os.listdir(path := require_asset_dir("foliage/leaves")):
            img_path = path / leaf
            self.leaf_imgs.append(load_image_file(img_path))

    def render_leaves(self, display: pygame.Surface, scroll: Scroll) -> None:
        for leaf in self.leaves[:]:
            leaf.render(display, scroll)

    def update_leaves(self, dt: float) -> None:
        self.wind.update(dt)
        for leaf in self.leaves[:]:
            leaf.update(self.wind, dt)
            leaf.duration -= dt
            if leaf.duration <= 0:
                leaf.alive = False
        self.leaves = [leaf for leaf in self.leaves if leaf.alive]

    def update(self, tree: Tree, dt: float) -> None:
        self.update_accumulator += dt
        while self.update_accumulator + 1e-12 >= FOLIAGE_SIMULATION_STEP:
            tree.generate_leaves(self.leaf_imgs, self.leaves, FOLIAGE_SIMULATION_STEP)
            self.update_leaves(FOLIAGE_SIMULATION_STEP)
            self.update_accumulator -= FOLIAGE_SIMULATION_STEP
