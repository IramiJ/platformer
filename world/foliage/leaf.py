from __future__ import annotations

import math
import random
from typing import TYPE_CHECKING

import pygame

from core.asset_cache import load_image
from core.settings import REFERENCE_TICKS_PER_SECOND

if TYPE_CHECKING:
    from pathlib import Path

    from world.scrolling import Scroll

    from .wind import Wind

WIND_ACCELERATION = 0.02 * REFERENCE_TICKS_PER_SECOND**2


class Leaf:
    def __init__(self, img: str | Path, loc: list[float], duration: float) -> None:
        self.img = load_image(img)

        self.loc = [float(loc[0]), float(loc[1])]
        self.max_duration = duration
        self.duration = float(self.max_duration)
        self.alive = True

        w, h = self.img.get_width(), self.img.get_height()
        self.rect = pygame.FRect(self.loc[0], self.loc[1], w, h)

        self.vx = random.uniform(-0.2, 0.2) * REFERENCE_TICKS_PER_SECOND
        self.vy = random.uniform(0.1, 0.6) * REFERENCE_TICKS_PER_SECOND

        self.gravity = random.uniform(0.015, 0.03) * REFERENCE_TICKS_PER_SECOND**2
        self.drag_per_second = (
            random.uniform(0.985, 0.995) ** REFERENCE_TICKS_PER_SECOND
        )
        self.terminal_vy = random.uniform(1.2, 2.2) * REFERENCE_TICKS_PER_SECOND

        self.phase = random.uniform(0, math.tau)
        self.flutter_amp = random.uniform(0.15, 0.5)
        self.flutter_speed = random.uniform(2.0, 5.0)

    def render(self, display: pygame.Surface, scroll: Scroll) -> None:
        display.blit(
            self.img,
            (
                self.loc[0] - scroll.render_scroll[0],
                self.loc[1] - scroll.render_scroll[1],
            ),
        )

    def update(self, wind: Wind, dt: float) -> None:
        self.phase += self.flutter_speed * dt
        flutter = math.sin(self.phase) * self.flutter_amp

        self.vy += self.gravity * dt
        self.vx += (wind.current + flutter) * WIND_ACCELERATION * dt

        drag = self.drag_per_second**dt
        self.vx *= drag
        self.vy *= drag

        self.vy = min(self.vy, self.terminal_vy)

        self.loc[0] += self.vx * dt
        self.loc[1] += self.vy * dt

        self.rect.x, self.rect.y = self.loc[0], self.loc[1]
