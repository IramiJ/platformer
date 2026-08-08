from __future__ import annotations

import csv
import math
import os
from typing import TYPE_CHECKING

import pygame

from core.paths import require_asset_dir
from core.settings import TILE_SIZE

if TYPE_CHECKING:
    from pathlib import Path

    from world.scrolling import Scroll


def read_csv(filename: str | Path) -> list[list[str]]:
    tilemap: list[list[str]] = []
    with open(os.path.join(filename)) as data:
        data = csv.reader(data, delimiter=",")
        for row in data:
            tilemap.append(list(row))
    return tilemap


def last_x(tilemap: list[list[str]]) -> int:
    return len(tilemap[0]) * TILE_SIZE


def load_tiles(path: str | Path) -> dict[str, pygame.Surface]:
    tiles_by_id: dict[str, pygame.Surface] = {}
    files = os.listdir(path)
    for file in files:
        name = str(int(file.split(".")[0]))
        tiles_by_id[name] = pygame.image.load(path / file).convert()
        tiles_by_id[name].set_colorkey((0, 0, 0))
    return tiles_by_id


SKIP_TILES = {"-1"}
NON_COLLISION_TILES = {"-1", "9", "19", "29", "39", "47", "48"}
VALID_TILE_IDS = {
    tile_file.stem for tile_file in require_asset_dir("tiles").glob("*.png")
}


def display_map(
    display: pygame.Surface,
    scroll: Scroll,
    tilemap: list[list[str]],
    tile_dict: dict[str, pygame.Surface],
) -> None:

    scroll_x, scroll_y = scroll.render_scroll
    screen_w, screen_h = display.get_size()

    # visible tile range (add 1 tile padding to avoid pop-in)
    x0 = max(0, int(scroll_x // TILE_SIZE) - 1)
    y0 = max(0, int(scroll_y // TILE_SIZE) - 1)
    x1 = min(len(tilemap[0]), math.ceil((scroll_x + screen_w) / TILE_SIZE) + 1)
    y1 = min(len(tilemap), math.ceil((scroll_y + screen_h) / TILE_SIZE) + 1)

    for y in range(y0, y1):
        row = tilemap[y]
        for x in range(x0, x1):
            tile = row[x]
            if tile in SKIP_TILES:
                continue

            world_x = x * TILE_SIZE
            world_y = y * TILE_SIZE

            display.blit(tile_dict[tile], (world_x - scroll_x, world_y - scroll_y))


def update_tile_rects(
    display: pygame.Surface,
    scroll: Scroll,
    tile_rects: list[pygame.Rect],
    tilemap: list[list[str]],
) -> None:

    for y in range(len(tilemap)):
        row = tilemap[y]
        for x in range(len(row)):
            tile = row[x]
            if tile in NON_COLLISION_TILES:
                continue

            world_x = x * TILE_SIZE
            world_y = y * TILE_SIZE
            tile_rects.append(pygame.Rect(world_x, world_y, TILE_SIZE, TILE_SIZE))


def validate_tilemap(tilemap: list[list[str]]) -> None:
    if not tilemap:
        raise ValueError("Tilemap must be non empty")
    length = len(tilemap[0])
    for row in tilemap:
        if not row:
            raise ValueError("All rows must be non emtpy")
        if len(row) != length:
            raise ValueError("All rows in tile map must be equally wide")
        for tile in row:
            if not is_int(tile):
                raise ValueError("All tiles must be integers written as strings")
            if tile != "-1" and tile not in VALID_TILE_IDS:
                raise ValueError(f"Invalid Tile: {tile}")


def is_int(value: str) -> bool:
    try:
        number = int(value)
    except ValueError:
        return False
    return number.is_integer()
