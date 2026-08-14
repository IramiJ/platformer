from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, TypedDict

import pygame

from core.paths import PROJECT_ROOT
from core.settings import TILE_SIZE
from world.tilemap import read_csv, validate_tilemap

from .coordinates import tile_position_to_pixel, tile_to_pixel

if TYPE_CHECKING:
    from collections.abc import Mapping

    from entities.enemies.enemies import Enemies
    from entities.player.player import Player
    from ui.win_screen import WinScreen
    from world.texts import Texts


class LevelData(TypedDict):
    """Holds all fields that are required in a level data file"""

    id: int
    map: str
    spawn: list[int]
    max_y: int
    enemies: dict[str, list[list[int]]]
    checkpoints: list[list[int]]
    end_coordinates: list[int]
    texts: dict[str, list[int]]


class LevelValidationError(ValueError):
    """Custom error that is being thrown during level validation"""


def is_position(value: object) -> bool:
    return (
        isinstance(value, list)
        and len(value) == 2
        and all(type(number) is int for number in value)
    )


def validate_level(data: Mapping[str, object], filename: str | Path) -> None:
    """Takes care of the entire level validation process. At the end, every error is being thrown with proper error messages."""
    errors: list[str] = []

    required_fields = {
        "id": int,
        "map": str,
        "spawn": list,
        "max_y": int,
        "enemies": dict,
        "checkpoints": list,
        "end_coordinates": list,
        "texts": dict,
    }

    for field, expected_type in required_fields.items():
        if field not in data:
            errors.append(f"Required field '{field} is missing")
        elif not isinstance(data[field], expected_type):
            errors.append(
                f"'{field}' must be {expected_type.__name__}, but type is {type(data[field]).__name__}"
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
            errors.append(f"Map-file doesn't exist: {data['map']}")

    if errors:
        details = "\n".join(f"- {error}" for error in errors)
        raise LevelValidationError(f"Invalid level data: {filename}\n{details}")


def validate_enemies(enemies: object, errors: list[str]) -> None:
    """Validates everything regarding the enemies, including their names and their positions on the map"""
    if not isinstance(enemies, dict):
        return

    valid_enemy_names = {"Patroller", "Heavy_Patroller", "Shooter", "Chaser"}

    for enemy_name, positions in enemies.items():
        if enemy_name not in valid_enemy_names:
            errors.append(f"Unknown enemy type: '{enemy_name}'")

        if not isinstance(positions, list):
            errors.append(f"'enemies.{enemy_name}' must be a list")
            continue

        for index, position in enumerate(positions):
            if not is_position(position):
                errors.append(f"'enemies.{enemy_name}[{index}] must be [x, y]")


def validate_texts(texts: object, errors: list[str]) -> None:
    """
    Validates all the big texts you can see on the screen in the individual levels.
    """
    if not isinstance(texts, dict):
        errors.append("field 'texts' is not a dictionary")
        return
    for text, position in texts.items():
        if not isinstance(text, str):
            errors.append("Every text key must be a string")

        if not is_position(position):
            errors.append(f"Position of text '{text}' must be [x, y]")


class LevelLoader:
    """Load Level configuration and tilemap data from disk.

    Coordinates in level JSON files are stored in tile-space.
    Derived runtime values such as 'max_y_px' are converted to pixel space when the level is loaded

    """

    def __init__(self) -> None:
        self.id = 1
        self.max_y_px = 0
        self.end_rect: pygame.Rect | None = None
        self.data: LevelData
        self.map: list[list[str]]

    def load_level(self, json_file: str | Path) -> None:
        """
        The level loader takes a JSON file and loads all data into a dictionary.

        The level is also being validated here and all checks regarding the level are being ran here.
        """
        with open(json_file, "r") as file:
            self.data = json.load(file)
        validate_level(self.data, json_file)
        self.map = read_csv(PROJECT_ROOT / self.data["map"])
        validate_tilemap(self.map)
        self.max_y_px = tile_to_pixel(self.data["max_y"])
        self.end_rect = pygame.Rect(
            *tile_position_to_pixel(self.data["end_coordinates"]),
            TILE_SIZE,
            TILE_SIZE,
        )

    def reload_level(self) -> None:
        self.load_level(PROJECT_ROOT / f"world/levels/level{self.id}.json")

    def next_level(self) -> None:
        self.id += 1
        self.load_level(PROJECT_ROOT / f"world/levels/level{self.id}.json")


def update_level(
    player: Player,
    level: LevelLoader,
    enemies: Enemies,
    texts: Texts,
    win_screen: WinScreen,
) -> bool:
    """
    First is being checked, whether or not the player has actually reached the end of the level.

    After that, the next level is being loaded. Assuming there is no errors, the next level will be loaded properly.

    If there is any errors, an error message will be thrown.
    """
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
        print(f"Error while reading the level files: {error}")
        return False

    return True


def initialize_player(player: Player, level: LevelLoader) -> None:
    """Sets up all the important things regarding the player, such as his spawn point, and reseting all his movements"""
    player.spawn_point = tile_position_to_pixel(level.data["spawn"])
    player.rect.x, player.rect.y = tile_position_to_pixel(level.data["spawn"])
    player.movement = [0, 0]


def reach_checkpoint(player: Player, level: LevelLoader) -> None:
    """If the player touches a checkpoint, his spawnpoint will be set to the location of the checkpoint."""
    for checkpoint in level.data["checkpoints"]:
        if player.rect.collidepoint(
            (checkpoint[0] * TILE_SIZE, checkpoint[1] * TILE_SIZE)
        ):
            player.spawn_point = [checkpoint[0] * TILE_SIZE, checkpoint[1] * TILE_SIZE]
            return
