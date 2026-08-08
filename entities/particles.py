from __future__ import annotations

import random
from typing import TYPE_CHECKING

import pygame

from core.asset_cache import load_image
from core.settings import REFERENCE_TICKS_PER_SECOND

if TYPE_CHECKING:
    from pathlib import Path

    from world.scrolling import Scroll

PARTICLE_GRAVITY = 0.01 * REFERENCE_TICKS_PER_SECOND**2
PARTICLE_JITTER_INTERVAL = 1.0 / REFERENCE_TICKS_PER_SECOND


class Particle:
    def __init__(self, img: str | Path, loc: list[float], duration: float) -> None:
        self.img = load_image(img)
        self.loc = loc
        self.max_duration = duration
        self.duration = float(self.max_duration)
        self.alive = True
        self.rect = pygame.FRect(
            self.loc[0], self.loc[1], self.img.get_width(), self.img.get_height()
        )
        self.x_velocity = 0
        self.y_velocity = 0.2 * REFERENCE_TICKS_PER_SECOND
        self.jitter_timer = 0.0

    def update(self, dt: float) -> None:
        self.increase_velocity(dt)
        self.update_location(dt)
        self.duration = max(0.0, self.duration - dt)
        if self.duration <= 0:
            self.alive = False

    def render(self, display: pygame.Surface, scroll: Scroll) -> None:
        display.blit(
            self.img,
            [
                self.loc[0] - scroll.render_scroll[0],
                self.loc[1] - scroll.render_scroll[1],
            ],
        )

    def update_location(self, dt: float) -> None:
        self.loc[0] += self.x_velocity * dt
        self.loc[1] += self.y_velocity * dt
        self.rect.topleft = self.loc

    def increase_velocity(self, dt: float) -> None:
        self.y_velocity += PARTICLE_GRAVITY * dt
        self.jitter_timer -= dt
        while self.jitter_timer < 0:
            self.x_velocity = random.randint(-10, 10) / 30 * REFERENCE_TICKS_PER_SECOND
            self.jitter_timer += PARTICLE_JITTER_INTERVAL
