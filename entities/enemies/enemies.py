from __future__ import annotations

from typing import TYPE_CHECKING

from core.settings import TILE_SIZE
from entities.enemies.chaser import Chaser
from entities.enemies.patroller import Patroller
from entities.enemies.shooter import Shooter
from world.coordinates import tile_to_pixel

from .heavy_patroller import HeavyPatroller

if TYPE_CHECKING:
    import pygame

    from core.logic_variables import LogicVariables
    from entities.enemies.enemy import Enemy
    from entities.enemies.shooter_bullet import ShooterBullet
    from entities.player.player import Player
    from entities.spark import Spark
    from world.level_loader import LevelLoader
    from world.scrolling import Scroll


class Enemies:
    """
    Manages all the enemies in the game
    """

    def __init__(self) -> None:
        self.enemy_types: dict[str, type[Enemy]] = {
            "Patroller": Patroller,
            "Chaser": Chaser,
            "Shooter": Shooter,
            "Heavy_Patroller": HeavyPatroller,
        }
        self.max_enemy_amount = 0
        self.current_enemy_amount = 0
        self.enemies: list[Enemy] = []
        self.active_range_x = TILE_SIZE * 20
        self.active_range_y = TILE_SIZE * 15

    def enemy_is_active(self, enemy: Enemy, player: Player) -> bool:
        return (
            abs(enemy.rect.centerx - player.rect.centerx) <= self.active_range_x
            and abs(enemy.rect.centery - player.rect.centery) <= self.active_range_y
        )

    def update_enemies(
        self,
        player: Player,
        bullet_list: list[ShooterBullet],
        scroll: Scroll,
        tiles: list[pygame.Rect],
        logic_variables: LogicVariables,
        sparks: list[Spark],
        dt: float,
    ) -> None:
        """
        Makes updates to all the enemies regarding attacks, damage, moves and their alive/dead cycle
        """
        for enemy in self.enemies:
            enemy.update_dmg_timer(dt)
            if self.enemy_is_active(enemy, player):
                if isinstance(enemy, Chaser):
                    enemy.move(player, tiles, dt)
                else:
                    enemy.move(dt, tiles)

                if isinstance(enemy, Shooter):
                    enemy.attack(player, bullet_list, scroll, dt)
                else:
                    enemy.attack(player, scroll, dt)

                player.attack(enemy, logic_variables, sparks, dt)
            enemy.update_frames(dt)

        length = len(self.enemies)
        self.enemies = [enemy for enemy in self.enemies if enemy.alive]

        killed_enemy_count = length - len(self.enemies)
        if killed_enemy_count >= 1:
            if player.double_coin_buff:
                player.coin_amount += 4 * killed_enemy_count
            else:
                player.coin_amount += 2 * killed_enemy_count

        self.current_enemy_amount = len(self.enemies)

    def render_enemies(self, display: pygame.Surface, scroll: Scroll) -> None:
        for enemy in self.enemies:
            enemy.render(display, scroll.render_scroll)

    """
    Hitbox for debugging purposes
    pygame.draw.rect(display, (255,0,0), pygame.Rect(enemy.rect.left - scroll.render_scroll[0], enemy.rect.top - scroll.render_scroll[1], 16, 16))
    """

    def load_enemies(self, level: LevelLoader) -> None:
        """
        Loads all enemies of the level loader into the enemy list of this class
        """
        self.enemies = []
        enemies = level.data["enemies"]

        for enemy_name, spawns in enemies.items():
            enemy_class = self.enemy_types.get(enemy_name)

            for x, y in spawns:
                enemy = enemy_class(tile_to_pixel(x), tile_to_pixel(y), 16, 16)
                enemy.update_frames(0)
                self.enemies.append(enemy)

        self.max_enemy_amount = len(self.enemies)
