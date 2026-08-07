import random

import pygame

from core.settings import REFERENCE_TICKS_PER_SECOND

PARTICLE_GRAVITY = 0.01 * REFERENCE_TICKS_PER_SECOND**2
PARTICLE_JITTER_INTERVAL = 1.0 / REFERENCE_TICKS_PER_SECOND


class Particle:
    def __init__(self, img, loc, duration):
        self.img = pygame.image.load(img).convert()
        self.img.set_colorkey((0, 0, 0))
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

    def update(self, dt):
        self.increase_velocity(dt)
        self.update_location(dt)
        self.duration = max(0.0, self.duration - dt)
        if self.duration <= 0:
            self.alive = False

    def render(self, display, scroll):
        display.blit(
            self.img,
            [
                self.loc[0] - scroll.render_scroll[0],
                self.loc[1] - scroll.render_scroll[1],
            ],
        )

    def update_location(self, dt):
        self.loc[0] += self.x_velocity * dt
        self.loc[1] += self.y_velocity * dt
        self.rect.topleft = self.loc

    def increase_velocity(self, dt):
        self.y_velocity += PARTICLE_GRAVITY * dt
        self.jitter_timer -= dt
        while self.jitter_timer < 0:
            self.x_velocity = random.randint(-10, 10) / 30 * REFERENCE_TICKS_PER_SECOND
            self.jitter_timer += PARTICLE_JITTER_INTERVAL
