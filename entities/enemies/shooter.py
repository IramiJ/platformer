from __future__ import annotations

import math
from typing import TYPE_CHECKING

from core.paths import require_asset_dir, require_asset_file
from entities.animations import load_animation
from entities.enemies.enemy import Enemy
from entities.enemies.shooter_bullet import ShooterBullet
from entities.hp_bar import HpBar

if TYPE_CHECKING:
    import pygame

    from entities.player.player import Player
    from world.scrolling import Scroll


class Shooter(Enemy):
    def __init__(self, x: float, y: float, width: int, height: int) -> None:
        super().__init__(x, y, width, height)
        self.spawn_point = [self.x, self.y]
        self.aggro_range = 300
        self.action = "idle"
        self.max_hp = 2
        self.current_hp = 2
        self.animation_database["idle"] = load_animation(
            require_asset_dir("enemies/shooter/idle"), [20, 20, 20, 20, 20, 20], self
        )
        self.animation_database["shoot"] = load_animation(
            require_asset_dir("enemies/shooter/shoot"), [20, 20], self
        )
        self.hp_bar = HpBar(
            require_asset_file("hp_bar/enemy_hp_bar_bg.png"),
            require_asset_file("hp_bar/enemy_hp_bar_frame.png"),
            self.x,
            self.y - 20,
        )
        self.attack_cd = 0
        self.collision_cd = 0
        self.stunned = False
        self.stun_cd = 0
        self.shoot_count = 0

    def render(self, display: pygame.Surface, scroll: list[float]) -> None:
        if not self.alive:
            return
        self.draw(display, scroll)
        hp_bar_position = (self.rect.x - scroll[0], self.rect.y - scroll[1] - 20)
        self.hp_bar.draw(display, self.max_hp, self.current_hp, hp_bar_position)

    def move(self, dt: float, tiles: list[pygame.Rect]) -> None:
        self.movement = [0, 0]
        self.set_y_momentum(dt)
        self.movement[1] += self.y_momentum
        self.move_with_tile_collisions(dt, tiles)

    def attack(
        self,
        player: Player,
        bullet_list: list[ShooterBullet],
        scroll: Scroll,
        dt: float,
    ) -> None:
        self.handle_stun_state(dt)
        if not self.stunned:
            self.reduce_attack_cd(dt)
            self.check_attack_state(player, bullet_list)
        self.update_player_phsyical_dmg(player, scroll, dt)

    def check_attack_state(
        self, player: Player, bullet_list: list[ShooterBullet]
    ) -> None:
        if (
            math.sqrt(
                (self.spawn_point[0] - player.rect.x) ** 2
                + (self.spawn_point[1] - player.rect.y) ** 2
            )
            <= self.aggro_range
        ):
            self.shoot(bullet_list, player)
        else:
            self.change_action("idle")

    def shoot(self, bullet_list: list[ShooterBullet], player: Player) -> None:
        self.change_action("shoot")
        if self.attack_cd <= 0:
            if self.shoot_count == 2:
                self.attack_cd = 2
                self.shoot_count = 0
            else:
                self.attack_cd = 0.5
            bullet_list.append(ShooterBullet(self.spawn_point.copy(), player))
            self.shoot_count += 1

    def stun(self) -> None:
        self.stun_cd = 1 / 3
        self.stunned = True

    def handle_stun_state(self, dt: float) -> None:
        if self.stunned:
            self.stun_cd = max(0.0, self.stun_cd - dt)
            if self.stun_cd <= 0:
                self.stunned = False

    def reduce_attack_cd(self, dt: float) -> None:
        if self.attack_cd > 0:
            self.attack_cd = max(0, self.attack_cd - dt)

    def update_player_phsyical_dmg(
        self, player: Player, scroll: Scroll, dt: float
    ) -> None:
        if self.collision_cd > 0:
            self.collision_cd = max(0.0, self.collision_cd - dt)

        elif self.rect.colliderect(player.rect) and not player.dashing:
            player.take_dmg(scroll)
            self.collision_cd = 0.5
