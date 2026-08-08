import math

import pygame

from core.settings import REFERENCE_TICKS_PER_SECOND
from entities.animations import ANIMATION_TICKS_PER_SECOND
from entities.entity import Entity
from world.collisions import collision_test, move_collisions

DAMAGE_FLASH_DURATION = 5.0 / REFERENCE_TICKS_PER_SECOND
WHITE_FLASH_DURATION = 1.0 / REFERENCE_TICKS_PER_SECOND


class Enemy(Entity):
    """
    The parent class for all enemies in the game.

    Gives them more funcitonality than just a regular entity, such as animations, hp, damage management and collisions.
    """

    def __init__(self, x: float, y: float, width: int, height: int) -> None:
        super().__init__(x, y, width, height)
        self.animation_database: dict[str, list[str]]
        self.max_hp = 3
        self.current_hp = 3
        self.velocity = 60
        self.alive = True
        self.dmg_timer = 0
        self.y_momentum = 0

    def update_frames(self, dt: float) -> None:
        animation = self.animation_database[self.action]
        self.frame = (self.frame + ANIMATION_TICKS_PER_SECOND * dt) % len(animation)
        self.img_id = animation[math.floor(self.frame)]
        self.img = self.animation_frames[self.img_id]

    def update_dmg_timer(self, dt: float) -> None:
        if self.dmg_timer <= 0:
            return
        else:
            self.dmg_timer = max(0.0, self.dmg_timer - dt)

    def draw_dmg_timer(self, to_blit: pygame.Surface) -> None:
        if self.dmg_timer > 0:
            if self.dmg_timer > DAMAGE_FLASH_DURATION - WHITE_FLASH_DURATION:
                to_blit.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_ADD)
            else:
                to_blit.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_ADD)

    def draw(self, display: pygame.Surface, scroll: list[float]) -> None:
        to_blit = self.img.copy()
        self.draw_dmg_timer(to_blit)
        display.blit(
            pygame.transform.flip(to_blit, self.flip, False),
            [self.rect.x - scroll[0], self.rect.y - scroll[1]],
        )

    def die(self) -> None:
        self.current_hp = 0
        self.alive = False

    def take_dmg(self, dmg: int) -> None:
        if not self.alive:
            return
        self.dmg_timer = DAMAGE_FLASH_DURATION
        self.current_hp -= dmg
        self.taking_dmg = True
        if self.current_hp <= 0:
            self.die()

    def handle_tile_collisions(self, tiles: list[pygame.Rect]) -> None:
        hit_list = collision_test(self.rect, tiles)
        for tile in hit_list:
            if self.movement[1] > 0:
                self.rect.bottom = tile.top
                self.y_momentum = 0
            if self.movement[0] > 0:
                self.rect.right = tile.left
            elif self.movement[0] < 0:
                self.rect.left = tile.right

    def collision(self, tiles: list[pygame.Rect]) -> None:
        self.handle_tile_collisions(tiles)

    def move_with_tile_collisions(self, dt: float, tiles: list[pygame.Rect]) -> None:
        self.rect, collisions = move_collisions(self.rect, self.movement, tiles, dt)
        if collisions["bottom"] or collisions["top"]:
            self.y_momentum = 0

    def set_y_momentum(self, dt: float) -> None:
        self.y_momentum += 1440 * dt
        self.y_momentum = min(self.y_momentum, 420.0)
