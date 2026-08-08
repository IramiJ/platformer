from __future__ import annotations

import random
from typing import TYPE_CHECKING

import pygame

from core.paths import require_asset_file
from core.settings import REFERENCE_TICKS_PER_SECOND

from .leaf import Leaf

if TYPE_CHECKING:
    from pathlib import Path

    from world.scrolling import Scroll

LEAF_SPAWNS_PER_SECOND = REFERENCE_TICKS_PER_SECOND / 11.0


class Tree:
    def __init__(self, loc: list[float]) -> None:
        self.img = pygame.image.load(require_asset_file("foliage/tree.png")).convert()
        self.img.set_colorkey((0, 0, 0))
        self.loc = loc
        self.leaf_spawn_timer = self.next_leaf_spawn_delay()

    def render(self, display: pygame.Surface, scroll: Scroll) -> None:
        display.blit(
            self.img,
            [
                self.loc[0] - scroll.render_scroll[0],
                self.loc[1] - scroll.render_scroll[1],
            ],
        )

    def next_leaf_spawn_delay(self) -> float:
        return random.expovariate(LEAF_SPAWNS_PER_SECOND)

    def generate_leaves(
        self, leaf_imgs: list[Path], leaf_list: list[Leaf], dt: float
    ) -> None:
        self.leaf_spawn_timer -= dt

        while self.leaf_spawn_timer <= 0:
            self.spawn_leaf(leaf_imgs, leaf_list)
            self.leaf_spawn_timer += self.next_leaf_spawn_delay()

    def spawn_leaf(self, leaf_imgs: list[Path], leaf_list: list[Leaf]) -> None:
        loc = self.loc.copy()
        loc[0] += random.randint(0, 40)
        loc[1] += random.randint(0, 10)
        leaf_list.append(Leaf(random.choice(leaf_imgs), loc, random.randint(1, 10)))
