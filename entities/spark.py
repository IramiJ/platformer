from __future__ import annotations

import math
from typing import TYPE_CHECKING

import pygame

from core.settings import REFERENCE_TICKS_PER_SECOND

if TYPE_CHECKING:
    from world.scrolling import Scroll

SPARK_SPEED_DECAY_PER_REFERENCE_TICK = 0.1


class Spark:
    def __init__(
        self,
        loc: list[float],
        angle: float,
        speed: float,
        color: tuple[int, int, int],
        scale: float = 1,
    ) -> None:
        self.loc = loc
        self.angle = angle
        self.speed = speed
        self.scale = scale
        self.color = color
        self.alive = True

    def point_towards(self, angle: float, rate: float) -> None:
        rotate_direction = (
            (angle - self.angle + math.pi * 3) % (math.pi * 2)
        ) - math.pi
        try:
            rotate_sign = abs(rotate_direction) / rotate_direction
        except ZeroDivisionError:
            rotate_sign = 1
        if abs(rotate_direction) < rate:
            self.angle = angle
        else:
            self.angle += rate * rotate_sign

    def calculate_movement(self, dt: float, speed: float | None = None) -> list[float]:
        if speed is None:
            speed = self.speed
        return [
            math.cos(self.angle) * speed * dt,
            math.sin(self.angle) * speed * dt,
        ]

    def velocity_adjust(
        self,
        friction: float,
        force: float,
        terminal_velocity: float,
        dt: float,
    ) -> None:
        movement = self.calculate_movement(dt)
        movement[1] = min(terminal_velocity, movement[1] + force * dt)
        movement[0] *= friction
        self.angle = math.atan2(movement[1], movement[0])

    def move(self, dt: float) -> None:
        decay_per_second = (
            SPARK_SPEED_DECAY_PER_REFERENCE_TICK * REFERENCE_TICKS_PER_SECOND
        )
        active_dt = min(dt, self.speed / decay_per_second)
        new_speed = max(0.0, self.speed - decay_per_second * active_dt)
        if new_speed < 1e-9:
            new_speed = 0.0
        average_speed = (self.speed + new_speed) / 2
        legacy_step_correction = SPARK_SPEED_DECAY_PER_REFERENCE_TICK / 2
        movement = self.calculate_movement(
            active_dt * REFERENCE_TICKS_PER_SECOND,
            average_speed + legacy_step_correction,
        )
        self.loc[0] += movement[0]
        self.loc[1] += movement[1]

        """
        More Settings for the spark behaviour
        self.point_towards(math.pi / 2, 0.02)
        self.velocity_adjust(0.975, 0.2, 8, dt)
        self.angle += 0.1
        """
        self.speed = new_speed

        if self.speed <= 0:
            self.alive = False

    def draw(self, surf: pygame.Surface, scroll: Scroll) -> None:
        if self.alive:
            points = [
                [
                    self.loc[0]
                    + math.cos(self.angle) * self.speed * self.scale
                    - scroll.render_scroll[0],
                    self.loc[1]
                    + math.sin(self.angle) * self.speed * self.scale
                    - scroll.render_scroll[1],
                ],
                [
                    self.loc[0]
                    + math.cos(self.angle + math.pi / 2) * self.speed * self.scale * 0.3
                    - scroll.render_scroll[0],
                    self.loc[1]
                    + math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3
                    - scroll.render_scroll[1],
                ],
                [
                    self.loc[0]
                    - math.cos(self.angle) * self.speed * self.scale * 3.5
                    - scroll.render_scroll[0],
                    self.loc[1]
                    - math.sin(self.angle) * self.speed * self.scale * 3.5
                    - scroll.render_scroll[1],
                ],
                [
                    self.loc[0]
                    + math.cos(self.angle - math.pi / 2) * self.speed * self.scale * 0.3
                    - scroll.render_scroll[0],
                    self.loc[1]
                    - math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3
                    - scroll.render_scroll[1],
                ],
            ]
            pygame.draw.polygon(surf, self.color, points)
