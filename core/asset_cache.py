from __future__ import annotations

from functools import cache
from pathlib import Path
from typing import TYPE_CHECKING

import pygame

from core.paths import require_asset_file

if TYPE_CHECKING:
    from ui.font_renderer import Font


@cache
def load_image(relative_path: str, alpha: bool = False) -> pygame.Surface:
    image = pygame.image.load(require_asset_file(relative_path))
    image = image.convert_alpha() if alpha else image.convert()
    image.set_colorkey((0, 0, 0))
    return image


@cache
def load_image_file(path: Path, alpha: bool = False) -> pygame.Surface:
    image = pygame.image.load(path)
    image = image.convert_alpha() if alpha else image.convert()
    image.set_colorkey((0, 0, 0))
    return image


@cache
def load_font(relative_path: str) -> Font:
    from ui.font_renderer import Font

    return Font(require_asset_file(relative_path))
