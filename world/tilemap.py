from __future__ import annotations

import csv
import math
import os
import pygame

from .torch import Torch
from .chandelier import Chandelier
from core.settings import TILE_SIZE

from typing import TYPE_CHECKING

if TYPE_CHECKING: 
    from world.scrolling import Scroll

def load_map(path: str) -> list[list[str]]:
    f = open(path + ".txt", "r")
    data = f.read()
    f.close()
    data = data.split("\n")
    tilemap = []
    for row in data:
        tilemap.append(list(row))
    return tilemap


def read_csv(filename: str) -> list[list[str]]:
    tilemap = []
    with open(os.path.join(filename)) as data:
        data = csv.reader(data, delimiter=",")
        for row in data:
            tilemap.append(list(row))
    return tilemap


def last_x(tilemap: list[list[str]]) -> int:
    return len(tilemap[0]) * TILE_SIZE


def load_tiles(path: str) -> dict[str, pygame.Surface]:
    tiles_by_id = {}
    files = os.listdir(path)
    for file in files:
        name = str(int(file.split(".")[0]))
        tiles_by_id[name] = pygame.image.load(path + "/" + file).convert()
        tiles_by_id[name].set_colorkey((0, 0, 0))
    return tiles_by_id


def load_torches(tilemap: list[list[str]], torch_list) -> None:
    torch_types = {"10": Torch, "12": Chandelier}
    y = 0
    torch_list.clear()
    for row in tilemap:
        x = 0
        for tile in row:
            if tile == "10" or tile == "12":
                position = [x * TILE_SIZE, y * TILE_SIZE]
                torch_list.append(torch_types[tile](position))
            x += 1
        y += 1


SKIP_TILES = {"-1"}
NON_COLLISION_TILES = {"-1", "8", "19", "29", "39", "47", "48"}


def display_map(display: pygame.Surface, scroll: Scroll, tilemap: list[list[str]], tile_dict: dict[str, pygame.Surface]) -> None:

    scroll_x, scroll_y = scroll.render_scroll
    screen_w, screen_h = display.get_size()

    # visible tile range (add 1 tile padding to avoid pop-in)
    x0 = max(0, int(scroll_x // TILE_SIZE) - 1)
    y0 = max(0, int(scroll_y // TILE_SIZE) - 1)
    x1 = min(len(tilemap[0]), int(math.ceil((scroll_x + screen_w) / TILE_SIZE)) + 1)
    y1 = min(len(tilemap), int(math.ceil((scroll_y + screen_h) / TILE_SIZE)) + 1)

    for y in range(y0, y1):
        row = tilemap[y]
        for x in range(x0, x1):
            tile = row[x]
            if tile in SKIP_TILES:
                continue

            world_x = x * TILE_SIZE
            world_y = y * TILE_SIZE

            display.blit(tile_dict[tile], (world_x - scroll_x, world_y - scroll_y))


def update_tile_rects(display: pygame.Surface, scroll: Scroll, tile_rects: list[pygame.Rect], tilemap: list[list[str]]) -> None:
    scroll_x, scroll_y = scroll.render_scroll
    screen_w, screen_h = display.get_size()

    x0 = max(0, int(scroll_x // TILE_SIZE) - 1)
    y0 = max(0, int(scroll_y // TILE_SIZE) - 1)
    x1 = min(len(tilemap[0]), int(math.ceil((scroll_x + screen_w) / TILE_SIZE)) + 1)
    y1 = min(len(tilemap), int(math.ceil((scroll_y + screen_h) / TILE_SIZE)) + 1)

    for y in range(y0, y1):
        row = tilemap[y]
        for x in range(x0, x1):
            tile = row[x]
            if tile in NON_COLLISION_TILES:
                continue

            world_x = x * TILE_SIZE
            world_y = y * TILE_SIZE
            tile_rects.append(pygame.Rect(world_x, world_y, TILE_SIZE, TILE_SIZE))
