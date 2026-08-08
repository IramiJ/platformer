from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pygame

from core.asset_cache import load_image, load_image_file
from core.settings import REFERENCE_TICKS_PER_SECOND

if TYPE_CHECKING:
    from entities.entity import Entity

ANIMATION_TICKS_PER_SECOND = REFERENCE_TICKS_PER_SECOND


def load_animation(path: str | Path, dur: list[int], entity: Entity) -> list[str]:
    path = Path(path)
    animation_name = path.name
    animation_frame_data: list[str] = []
    for number, duration in enumerate(dur):
        animation_frame_id = f"{animation_name}{number}"
        img_loc = path / f"{animation_frame_id}.png"
        if not img_loc.is_file():
            raise FileNotFoundError(f"Missing animation frame: {img_loc}")
        animation_image = load_image_file(str(img_loc), alpha=True)
        entity.animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(duration):
            animation_frame_data.append(animation_frame_id)
    return animation_frame_data


def draw_constants(display: pygame.Surface) -> None:
    coin_count = load_image("constants/coins.png")
    display.blit(coin_count, (0, 0))
