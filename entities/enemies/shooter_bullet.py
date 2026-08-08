from __future__ import annotations

import math
from typing import TYPE_CHECKING

import pygame

from core.paths import require_asset_file
from entities.entity import SimpleEntity

if TYPE_CHECKING:
    from entities.player.player import Player
    from world.scrolling import Scroll


class ShooterBullet(SimpleEntity):
    def __init__(self, loc: list[float], player: Player) -> None:
        super().__init__(require_asset_file("enemies/shooter/bullet.png"), loc)
        self.start = self.loc.copy()
        self.base_img = self.img.copy()
        self.velocity = 120
        self.range = 200
        self.calc_angle(player)
        self.dmg_cd = 0
        self.alive = True

    def calc_angle(self, player: Player) -> None:
        x = self.get_rect().x - player.rect.x
        y = self.get_rect().y - player.rect.y
        self.angle = math.atan2(y, x) + math.pi

    def transform_img(self) -> None:
        self.img = pygame.transform.rotate(self.base_img, math.degrees(self.angle))

    def move(self, entity: Player, scroll: Scroll, dt: float) -> None:
        self.loc[0] += math.cos(self.angle) * self.velocity * dt
        self.loc[1] += math.sin(self.angle) * self.velocity * dt
        if self.dmg_cd <= 0:
            self.dmg_entity(entity, scroll)
        self.check_alive()

    def check_alive(self) -> None:
        if (
            math.sqrt(
                (self.loc[0] - self.start[0]) ** 2 + (self.loc[1] - self.start[1]) ** 2
            )
            >= self.range
        ):
            self.alive = False

    def dmg_entity(self, entity: Player, scroll: Scroll) -> None:
        if self.collision_test(entity.rect):
            entity.take_dmg(scroll)
            self.dmg_cd = 1 / 60
