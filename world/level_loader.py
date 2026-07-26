from __future__ import annotations
from pathlib import Path

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

class LevelValidationError(ValueError):
    pass

def is_position(value) -> bool:
    return (
        isinstance(value, list)
        and len(value) == 2
        and all(type(number) is int for number in value)
    )

def validate_level(data: dict, filename: str) -> None:
        errors = []
        
        required_fields = {
            "id": int,
            "map": str,
            "spawn": list,
            "max_y": int,
            "enemies": dict,
            "checkpoints": list,
            "end_coordinates": list,
            "texts": dict
        }

        for field, expected_type in required_fields.items():
            if field not in data:
                errors.append(f"Required field '{field} is missing")
            elif not isinstance(data[field], expected_type):
                errors.append(
                    f"'{field}' must be {expected_type.__name__}, but type ist {type(data[field]).__name__}"
                )
        if "spawn" in data and not is_position(data["spawn"]):
            errors.append("'spawn' must be a position like [1, 1]")

        if "end_coordinates" in data and not is_position(data["end_coordinates"]):
            errors.append("'end_coordinates' must be a position like [1, 1]")

        if "checkpoints" in data and isinstance(data["checkpoints"], list):
            for index, checkpoint in enumerate(data["checkpoints"]):
                if not is_position(checkpoint):
                    errors.append(f"'checkpoints[{index}] must be a position like [1, 1]")

        validate_enemies(data.get("enemies"), errors)
        validate_texts(data.get("texts"), errors)

        if isinstance(data.get("map"), str):
            project_root = Path(__file__).resolve().parents[1]
            map_path = project_root / data["map"]

            if not map_path.is_file():
                errors.append(f"Map-file doesn't exist: {data["map"]}")

        if errors:
            details = "\n".join(f"- {error}" for error in errors)
            raise LevelValidationError(f"Invalid Leveldata: {filename}\n{details}")

def validate_enemies(enemies, errors):
    if not isinstance(enemies, dict):
        return

    valid_enemy_names = {"Patroller", "Heavy_Patroller", "Shooter", "Chaser"}

    for enemy_name, positions in enemies.items():
        if enemy_name not in valid_enemy_names:
            if enemy_name not in valid_enemy_names:
                errors.append(f"Unknown enemy type: '{enemy_name}'")

        if not isinstance(positions, list):
            errors.append(f"'enemies.{enemy_name}' musst be a list")
            continue

        for index, position in enumerate(positions):
            if not is_position(position):
                errors.append(f"'enemies.{enemy_name}[{index}] musst be [x, y]")

def validate_texts(texts, errors):
    if not isinstance(texts, dict):
        pass
    for text, position in texts.items():
        if not isinstance(text, str):
            errors.append("Every text key must be a string")

        if not is_position(position):
            errors.append(f"Position of text '{text}' must be [x, y]")

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
        validate_level(self.data, json_file)
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

    




def update_level(player: Player, level: Level_loader, enemies: Enemies, texts: Texts, win_screen) -> bool:
    if not player.rect.colliderect(level.end_rect):
        return False
    try:
        level.next_level()
    except FileNotFoundError as error:
        print(f"No next level found: {error}")
        win_screen.displaying = True
        return False
    except json.JSONDecodeError as error:
        print(f"Invalid JSON: {error}")
        return False
    except PermissionError as error:
        print(f"Permission error: {error}")
        return False
    except UnicodeDecodeError as error:
        print(f"Level file has invalid encoding: {error}")
        return False
    except OSError as error:
        print(f"Error while readinf the level files: {error}")
        return False
    
    enemies.load_enemies(level)
    texts.load_texts(level.data["texts"])
    initialize_player(player, level)

    return True


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
