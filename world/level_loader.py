from __future__ import annotations

import json
import pygame
from typing import TYPE_CHECKING

from world.tilemap import read_csv
from core.settings import TILE_SIZE
from .coordinates import tile_position_to_pixel, tile_to_pixel

if TYPE_CHECKING:
    from entities.enemies.enemies import Enemies
    from entities.player.player import Player
    from world.texts import Texts


class Level_loader:

    """Load Level configuartion and tilemap data from disk.
    
    Coordinates in level JSON files are stored in tile-space. 
    Derived runtime values such as 'max_y_px' are converted to pixel space when the level is loaded
    
    """

    def __init__(self):
        self.id = 1
        self.max_y_px = 0
        self.end_rect = None

    def load_level(self, json_file: str) -> None:
        with open(json_file, "r") as file:
            self.data = json.load(file)
        self.map = read_csv(self.data["map"])
        self.max_y_px = tile_to_pixel(self.data["max_y"])
        self.end_rect = pygame.Rect(
            *tile_position_to_pixel(self.data["end_coordinates"]),
            TILE_SIZE,
            TILE_SIZE,
        )

    def reload_level(self) -> None:
        self.load_level(f"world/levels/level{self.id}.json")

    def next_level(self) -> None:
        self.id += 1
        self.load_level(f"world/levels/level{self.id}.json")

    def validate_level(self):
        pass


def update_level(player: Player, level: Level_loader, enemies: Enemies, texts: Texts, win_screen) -> None:
    if player.rect.colliderect(level.end_rect):
        try:
            level.next_level()
        except:
            win_screen.displaying = True
        enemies.load_enemies(level)
        texts.load_texts(level.data["texts"])
        initialize_player(player, level)


def reload_level(enemies: Enemies, level: Level_loader, player: Player, texts: Texts) -> None:
    level.reload_level()
    enemies.load_enemies(level)
    texts.load_texts(level.data["texts"])
    initialize_player(player, level)


def initialize_player(player: Player, level: Level_loader) -> None:
    player.spawn_point = tile_position_to_pixel(level.data["spawn"])
    player.rect.x, player.rect.y = tile_position_to_pixel(level.data["spawn"])
    player.movement = [0, 0]


def reach_checkpoint(player: Player, level: Level_loader) -> None:
    for checkpoint in level.data["checkpoints"]:
        if player.rect.collidepoint((checkpoint[0] * TILE_SIZE, checkpoint[1] * TILE_SIZE)):
            player.spawn_point = [checkpoint[0] * TILE_SIZE, checkpoint[1] * TILE_SIZE]
            return
