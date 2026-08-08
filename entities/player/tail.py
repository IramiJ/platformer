from __future__ import annotations

import math
from typing import TYPE_CHECKING

from core.paths import require_asset_file
from entities.entity import SimpleEntity

if TYPE_CHECKING:
    from pathlib import Path

    import pygame

TAIL_WAVE_INTERVAL = 0.1
TAIL_POINT_DURATION = 2.0


class Tail:
    def __init__(self, img: str | Path, loc: list[float]) -> None:
        self.img = img
        self.loc = loc
        self.points: list[Tail.Point] = []
        self.shift = 0
        self.dir = "r"
        self.wave_timer = TAIL_WAVE_INTERVAL
        for i in range(10):
            self.points.append(
                self.Point(
                    self.loc[0] - i, self.loc[1], require_asset_file("tail/grey.png")
                )
            )

    def update_points(self, dt: float) -> None:
        if self.dir == "r":
            self.update_right()
        if self.dir == "l":
            self.update_left()
        self.wave_timer -= dt
        while self.wave_timer <= 0:
            self.shift += math.pi / 2
            self.wave_timer += TAIL_WAVE_INTERVAL
        for i in range(len(self.points)):
            self.points[i].loc[1] = self.loc[1] + self.sin_pos(i)

    def update_right(self) -> None:
        for i in range(len(self.points)):
            self.points[i].loc[0] = self.loc[0] - i

    def update_left(self) -> None:
        for i in range(len(self.points)):
            self.points[i].loc[0] = self.loc[0] + i

    def sin_pos(self, x: float) -> float:
        if self.shift >= 2 * math.pi:
            self.shift = 0
        return 2 * math.sin((math.pi * x / 2) + self.shift)

    class Point(SimpleEntity):
        def __init__(self, x: float, y: float, img: str | Path) -> None:
            super().__init__(img, [x, y])
            self.dur = TAIL_POINT_DURATION
            self.show = False

        def draw(self, display: pygame.Surface, scroll: list[float]) -> None:
            if self.dur > 0:
                self.render(display, scroll)
