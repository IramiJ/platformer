from __future__ import annotations

import math
from typing import TYPE_CHECKING

import pygame

from core.paths import require_asset_dir, require_asset_file
from core.settings import REFERENCE_TICKS_PER_SECOND
from entities.animations import ANIMATION_TICKS_PER_SECOND
from entities.entity import Entity
from entities.particles import Particle

if TYPE_CHECKING:
    from entities.player.player import Player
    from world.scrolling import Scroll


class Sword(Entity):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, 21, 7)
        self.loc = [x, y]
        self.img = pygame.image.load(
            require_asset_file("weapons/broken_sword.png")
        ).convert()
        self.img.set_colorkey((0, 0, 0))
        self.particles: list[Particle] = []
        self.flip = False
        self.particle_cd = 1 / 60
        self.load_slice_animation()
        self.slice_frame = 0
        self.animation_database["idle"] = [self.img]
        """ Keeps track of the player hand """
        self.offsets = {
            "run": [
                (6, 16),
                (5, 16),
                (3, 16),
                (2, 15),
                (5, 17),
                (7, 15),
                (6, 16),
                (8, 16),
                (11, 14),
                (16, 15),
                (12, 16),
                (9, 16),
            ],
            "idle": [(6, 16), (6, 16), (6, 17)],
        }
        self.angles = {
            "run": [0, -10, -25, -45, -25, 0, 0, 10, 25, 45, 35, 25],
            "idle": [0, 0, 0],
        }

    def add_particles(self, dt: float) -> None:
        self.particle_cd = max(0.0, self.particle_cd - dt)
        if self.particle_cd <= 0:
            self.spawn_particles()

    def spawn_particles(self) -> None:
        for i in range(4):
            p = Particle(
                require_asset_file("particles/sword_particle.png"),
                [self.loc[0] + i, self.loc[1]],
                2.0,
            )
            p.y_velocity += i / 100 * REFERENCE_TICKS_PER_SECOND
            if self.flip:
                self.particles.append(p)
            else:
                p.loc[0] = self.loc[0] + 20 - i
                self.particles.append(p)
        self.particle_cd = 1.0

    def update_particles(self, dt: float) -> None:
        for particle in self.particles:
            particle.update(dt)
        self.particles = [particle for particle in self.particles if particle.alive]

    def load_slice_animation(self) -> None:
        path = require_asset_dir("weapons/sword/slice")
        dur = [1 for x in range(11)]
        animation_name = path.name
        self.slice_animation: list[pygame.Surface] = []
        for number, duration in enumerate(dur):
            animation_frame_id = f"{animation_name}{number}"
            img_loc = path / f"{animation_frame_id}.png"
            if not img_loc.is_file():
                raise FileNotFoundError(f"Missing sword slice frame: {img_loc}")
            animation_image = pygame.image.load(img_loc).convert_alpha()
            animation_image.set_colorkey((0, 0, 0))
            for i in range(duration):
                self.slice_animation.append(animation_image)

    def draw_slice(self, display: pygame.Surface, scroll: Scroll) -> None:
        if not self.flip:
            display.blit(
                pygame.transform.flip(
                    self.slice_animation[math.floor(self.slice_frame)], self.flip, False
                ),
                [
                    self.loc[0] + 10 - scroll.render_scroll[0],
                    self.loc[1] - scroll.render_scroll[1] - 16,
                ],
            )
        else:
            display.blit(
                pygame.transform.flip(
                    self.slice_animation[math.floor(self.slice_frame)], self.flip, False
                ),
                [
                    self.loc[0]
                    - self.slice_animation[math.floor(self.slice_frame)].get_width()
                    - scroll.render_scroll[0],
                    self.loc[1] - scroll.render_scroll[1] - 16,
                ],
            )

    def update_slice_frame(self, dt: float) -> None:
        self.slice_frame = (self.slice_frame + ANIMATION_TICKS_PER_SECOND * dt) % len(
            self.slice_animation
        )

    def draw(
        self,
        player_dash_state: bool,
        display: pygame.Surface,
        scroll: Scroll,
        player_frame: float,
        player_action: str,
    ) -> None:
        frame = self.get_animation_frame(player_frame, player_action)
        angle = self.angles[player_action][frame]

        if player_dash_state:
            self.draw_slice(display, scroll)
        self.draw_particles(display, scroll)
        self.draw_rotated(display, scroll, angle)

    def update(self, player: Player, dt: float) -> None:
        self.update_location(player)
        self.set_flip(player.flip)
        self.update_particles(dt)

        if player.mode == "melee" and player.dashing:
            self.update_slice_frame(dt)

    def set_flip(self, flip: bool) -> None:
        self.flip = flip

    def update_location(self, player: Player) -> None:
        frame = self.get_animation_frame(player.frame, player.action)
        if player.flip:
            self.loc = [
                player.rect.left
                - self.img.get_width()
                + (24 - self.offsets[player.action][frame][0]),
                player.rect.y + self.offsets[player.action][frame][1] - 2,
            ]
        else:
            self.loc = [
                player.rect.right - (24 - self.offsets[player.action][frame][0]),
                player.rect.y + self.offsets[player.action][frame][1] - 2,
            ]

    def draw_particles(self, display: pygame.Surface, scroll: Scroll) -> None:
        for particle in self.particles:
            particle.render(display, scroll)

    def get_animation_frame(self, player_frame: float, player_action: str) -> int:
        if player_action == "run":
            return math.floor(player_frame / 4)
        elif player_action == "idle":
            return math.floor(player_frame / 20)
        return 0

    def draw_rotated(
        self, display: pygame.Surface, scroll: Scroll, angle: float
    ) -> None:
        img = pygame.transform.flip(self.img, self.flip, False)

        if self.flip:
            angle = -angle

        original_rect = img.get_rect(topleft=self.loc)

        if self.flip:
            hilt_offset = pygame.Vector2(img.get_width(), img.get_height() / 2)
        else:
            hilt_offset = pygame.Vector2(0, img.get_height() / 2)

        hilt_pos = pygame.Vector2(original_rect.topleft) + hilt_offset

        offset_from_center_to_hilt = hilt_pos - pygame.Vector2(original_rect.center)

        rotated_img = pygame.transform.rotate(img, angle)
        rotated_offset = offset_from_center_to_hilt.rotate(-angle)

        rotated_center = hilt_pos - rotated_offset
        rotated_rect = rotated_img.get_rect(center=rotated_center)

        display.blit(
            rotated_img,
            [
                rotated_rect.x - scroll.render_scroll[0],
                rotated_rect.y - scroll.render_scroll[1],
            ],
        )
