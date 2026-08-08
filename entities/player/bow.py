from __future__ import annotations

import math
from typing import TYPE_CHECKING

import pygame

from core.paths import require_asset_file
from entities.entity import SimpleEntity

if TYPE_CHECKING:
    from entities.enemies.enemy import Enemy
    from entities.player.player import Player
    from world.scrolling import Scroll


class Bow:
    def __init__(self, x: float, y: float) -> None:
        self.offsets: dict[str, list[tuple[int, int]]] = {
            "run": [
                (6, 16),
                (5, 16),
                (3, 16),
                (2, 15),
                (5, 17),
                (7, 15),
                (6, 16),
                (8, 16),
                (11, 14),
                (16, 15),
                (12, 16),
                (9, 16),
            ],
            "idle": [(6, 16), (6, 16), (6, 17)],
        }
        self.angles: dict[str, list[int]] = {
            "run": [0, -10, -25, -45, -25, 0, 0, 10, 25, 45, 35, 25],
            "idle": [0, 0, 0],
        }
        self.loc = [x, y]
        self.img = pygame.image.load(require_asset_file("weapons/bow.png")).convert()
        self.img.set_colorkey((0, 0, 0))
        self.arrows: list[Arrow] = []
        self.flip = False
        self.reloading = False
        self.add_ammo = False
        self.max_shoot_cd = 0.5
        self.shoot_cd = 1 / 60
        self.ammo = 5
        self.ammo_img = pygame.image.load(
            require_asset_file("weapons/cd_pistol.png")
        ).convert()
        self.ammo_img.set_colorkey((0, 0, 0))
        self.max_reload_cd = 2.0
        self.reload_cd = 0

    def update(self, player: Player, dt: float) -> None:
        self.update_cds(dt)
        self.set_flip(player)
        self.update_location(player)

    def draw(self, player: Player, display: pygame.Surface, scroll: Scroll) -> None:
        frame = self.get_animation_frame(player.frame, player.action)
        angle = self.angles[player.action][frame]
        self.draw_rotated(display, scroll, angle)

    def set_flip(self, player: Player) -> None:
        self.flip = player.flip

    def update_location(self, player: Player) -> None:
        frame = self.get_animation_frame(player.frame, player.action)
        if player.flip:
            self.loc = [
                player.rect.left
                - (self.img.get_width()) // 2
                + (24 - self.offsets[player.action][frame][0]),
                player.rect.y
                + self.offsets[player.action][frame][1]
                - self.img.get_height(),
            ]
        else:
            self.loc = [
                player.rect.right
                - (24 - self.offsets[player.action][frame][0])
                - (self.img.get_width()) // 2,
                player.rect.y
                + self.offsets[player.action][frame][1]
                - self.img.get_height(),
            ]

    def get_animation_frame(self, player_frame: float, player_action: str) -> int:
        if player_action == "run":
            return math.floor(player_frame / 4)
        elif player_action == "idle":
            return math.floor(player_frame / 20)
        return 0

    def move_arrows(self, enemy_list: list[Enemy], dt: float) -> None:
        for arrow in self.arrows:
            arrow.move(enemy_list, dt)
        self.arrows = [arrow for arrow in self.arrows if arrow.alive]

    def update_cds(self, dt: float) -> None:
        if self.shoot_cd > 0:
            self.shoot_cd = max(0, self.shoot_cd - dt)
        if self.reload_cd > 0:
            self.reload_cd = max(0, self.reload_cd - dt)
            if self.reload_cd <= 0:
                self.reloading = False
                self.add_ammo = True
        if self.add_ammo:
            self.ammo = 5
            self.add_ammo = False
        if self.ammo <= 0 and not self.reloading:
            self.reload()

    def add_arrow(self) -> None:
        if self.reload_cd <= 0 and self.shoot_cd <= 0:
            arrow_loc = self.loc.copy()
            flip = bool(self.flip)
            self.arrows.append(Arrow(arrow_loc, flip))
            self.shoot_cd = self.max_shoot_cd
            self.ammo -= 1

    def reload(self) -> None:
        if not self.reloading:
            self.reload_cd = self.max_reload_cd
            self.reloading = True

    def draw_rotated(
        self, display: pygame.Surface, scroll: Scroll, angle: float
    ) -> None:
        img = pygame.transform.flip(self.img, self.flip, False)

        if self.flip:
            angle = -angle

        original_rect = img.get_rect(topleft=self.loc)

        handle_offset = pygame.Vector2(img.get_width() / 2, 0)

        handle_pos = pygame.Vector2(original_rect.topleft) + handle_offset

        offset_from_center_to_hilt = handle_pos - pygame.Vector2(original_rect.center)

        rotated_img = pygame.transform.rotate(img, angle)
        rotated_offset = offset_from_center_to_hilt.rotate(-angle)

        rotated_center = handle_pos - rotated_offset
        rotated_rect = rotated_img.get_rect(center=rotated_center)

        display.blit(
            rotated_img,
            [
                rotated_rect.x - scroll.render_scroll[0],
                rotated_rect.y - scroll.render_scroll[1],
            ],
        )


class Arrow(SimpleEntity):
    def __init__(self, loc: list[float], flip: bool) -> None:
        super().__init__(require_asset_file("weapons/arrow.png"), loc)
        self.start = self.loc.copy()
        self.base_img = self.img.copy()
        self.velocity = 300
        self.range = 200
        self.dmg_cd = 0
        self.flip = flip
        self.alive = True

    def move(self, enemy_list: list[Enemy], dt: float) -> None:
        self.dmg_entity(enemy_list)
        if not self.flip:
            self.loc[0] += self.velocity * dt
        else:
            self.loc[0] -= self.velocity * dt
        self.check_alive()

    def check_alive(self) -> None:
        if (
            math.sqrt(
                (self.loc[0] - self.start[0]) ** 2 + (self.loc[1] - self.start[1]) ** 2
            )
            >= self.range
        ):
            self.alive = False

    def dmg_entity(self, enemies: list[Enemy]) -> None:

        if self.dmg_cd == 0:
            for enemy in enemies:
                if self.collision_test(enemy.rect):
                    enemy.take_dmg(1)
                    enemy.stun()
                    self.dmg_cd = 1

    def render(self, display: pygame.Surface, scroll: list[float]) -> None:
        display.blit(
            pygame.transform.flip(self.img, self.flip, False),
            (self.loc[0] - scroll[0], self.loc[1] - scroll[1]),
        )
