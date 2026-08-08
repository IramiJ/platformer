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


class Chaser(Enemy):
    """
    Chases the enemy once he is within a certain aggression range
    """

    def __init__(self, x: float, y: float, width: int, height: int) -> None:
        super().__init__(x, y, width, height)
        self.spawn_point = (self.x, self.y)
        self.aggro_range = 100
        self.action = "run"
        self.max_hp = 4
        self.current_hp = 4
        self.animation_database["idle"] = load_animation(
            require_asset_dir("enemies/chaser/idle"), [20, 20, 20, 20, 20, 20], self
        )
        self.animation_database["run"] = load_animation(
            require_asset_dir("enemies/chaser/run"), [5, 5, 5, 5, 5, 5], self
        )
        self.hp_bar = HpBar(
            require_asset_file("hp_bar/enemy_hp_bar_bg.png"),
            require_asset_file("hp_bar/enemy_hp_bar_frame.png"),
            self.x,
            self.y - 20,
        )
        self.direction = "r"
        self.velocity = 30
        self.move_burst_increase = 120
        self.true_velocity = self.velocity + self.move_burst_increase
        self.attack_cd = 0
        self.stunned = False
        self.stun_cd = 0

    def render(self, display: pygame.Surface, scroll: list[float]) -> None:
        if not self.alive:
            return
        self.draw(display, scroll)
        hp_bar_position = (self.rect.x - scroll[0], self.rect.y - scroll[1] - 20)
        self.hp_bar.draw(display, self.max_hp, self.current_hp, hp_bar_position)

    def move_to_player(self, player: Player) -> None:
        if player.rect.x < self.rect.x:
            self.change_action("run")
            self.direction = "l"
            self.flip = True
            self.movement[0] -= self.true_velocity
        elif player.rect.x > self.rect.x:
            self.change_action("run")
            self.direction = "r"
            self.flip = False
            self.movement[0] += self.true_velocity
        elif player.rect.x == self.rect.x:
            self.movement[0] = 0

    def return_to_spawnpoint(self) -> None:
        self.move_burst_increase = 0
        if self.rect.x < self.spawn_point[0]:
            self.change_action("run")
            self.direction = "r"
            self.flip = False
            self.movement[0] += self.true_velocity
        else:
            self.change_action("run")
            self.direction = "l"
            self.flip = True
            self.movement[0] -= self.true_velocity

    def move(self, player: Player, tiles: list[pygame.Rect], dt: float) -> None:
        if self.stunned:
            self.stun_cd = max(0.0, self.stun_cd - dt)

            if self.stun_cd <= 0:
                self.stunned = False

            return

        self.movement = [0.0, 0.0]

        distance_to_player = abs(self.rect.x - player.rect.x)
        distance_to_spawn = abs(self.rect.x - self.spawn_point[0])

        if distance_to_player <= self.aggro_range:
            self.move_burst(dt)
            self.true_velocity = self.velocity + self.move_burst_increase
            self.move_to_player(player)

        elif distance_to_spawn < 1:
            self.rect.x = self.spawn_point[0]
            self.move_burst_increase = 0
            self.true_velocity = self.velocity
            self.change_action("idle")

        else:
            self.move_burst_increase = 0
            self.true_velocity = self.velocity
            self.return_to_spawnpoint()
        self.set_y_momentum(dt)
        self.movement[1] += self.y_momentum
        self.move_with_tile_collisions(dt, tiles)

    def attack(self, player: Player, scroll: Scroll, dt: float) -> None:
        if self.stunned:
            return
        if self.attack_cd > 0:
            self.attack_cd = max(0.0, self.attack_cd - dt)
        else:
            if self.rect.colliderect(player.rect) and not player.dashing:
                player.take_dmg(scroll)
                self.attack_cd = 0.5

    def stun(self) -> None:
        self.stunned = True
        self.stun_cd = 1 / 3

    def move_burst(self, dt: float) -> None:
        if self.move_burst_increase <= 0:
            self.move_burst_increase = 120
        else:
            self.move_burst_increase = max(0.0, self.move_burst_increase - 180 * dt)
