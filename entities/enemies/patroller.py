from __future__ import annotations

from typing import TYPE_CHECKING

from core.paths import require_asset_dir, require_asset_file
from entities.animations import load_animation
from entities.enemies.enemy import Enemy
from entities.hp_bar import HpBar

if TYPE_CHECKING:
    import pygame

    from entities.player.player import Player
    from world.scrolling import Scroll


class Patroller(Enemy):
    """
    A simple enemy walking left and right, while also having bursts in his movements.
    """

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        super().__init__(x, y, width, height)
        self.spawn_point = (self.x, self.y)
        self.distance = 50
        self.action = "run"
        self.animation_database["run"] = load_animation(
            require_asset_dir("enemies/patroller/run"), [5, 5, 5, 5, 5, 5], self
        )
        self.hp_bar = HpBar(
            require_asset_file("hp_bar/enemy_hp_bar_bg.png"),
            require_asset_file("hp_bar/enemy_hp_bar_frame.png"),
            self.x,
            self.y - 20,
        )
        self.direction = "r"
        self.velocity = 72
        self.burst_velocity = 36
        self.true_velocity = self.velocity + self.burst_velocity
        self.attack_cd = 0
        self.stunned = False
        self.stun_cd = 0
        self.bursting = False
        self.burst_cd = 0

    def render(self, display: pygame.Surface, scroll: list[float]) -> None:
        if not self.alive:
            return
        self.draw(display, scroll)
        hp_bar_position = (self.rect.x - scroll[0], self.rect.y - scroll[1] - 20)
        self.hp_bar.draw(display, self.max_hp, self.current_hp, hp_bar_position)

    def move(self, dt: float, tiles: list[pygame.Rect]) -> None:
        if self.stunned:
            self.stun_cd = max(0.0, self.stun_cd - dt)
            if self.stun_cd <= 0:
                self.stunned = False
        else:
            self.movement = [0, 0]
            self.handle_burst(dt)
            if self.direction == "r":
                self.move_right()
            if self.direction == "l":
                self.move_left()
            self.set_y_momentum(dt)
            self.movement[1] += self.y_momentum
            self.move_with_tile_collisions(dt, tiles)

    def move_right(self) -> None:
        if self.rect.x >= self.spawn_point[0] + self.distance:
            self.direction = "l"
            self.flip = True
            self.activate_burst()
        else:
            self.movement[0] += self.true_velocity

    def move_left(self) -> None:
        if self.rect.x <= self.spawn_point[0] - self.distance:
            self.direction = "r"
            self.flip = False
            self.activate_burst()
        else:
            self.movement[0] -= self.true_velocity

    def attack(self, player: Player, scroll: Scroll, dt: float) -> None:
        if self.attack_cd > 0:
            self.attack_cd = max(0.0, self.attack_cd - dt)
        else:
            if self.rect.colliderect(player.rect) and not player.dashing:
                player.take_dmg(scroll)
                self.attack_cd = 0.5

    def stun(self) -> None:
        self.stun_cd = 1 / 3
        self.stunned = True

    def activate_burst(self) -> None:
        self.bursting = True
        self.burst_cd = 0.5

    def handle_burst(self, dt: float) -> None:
        if self.bursting:
            self.true_velocity = self.velocity + self.burst_velocity
            self.burst_cd = max(0.0, self.burst_cd - dt)
            if self.burst_cd <= 0:
                self.bursting = False
        else:
            self.true_velocity = self.velocity
