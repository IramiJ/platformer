from pathlib import Path

import pygame

from core.asset_cache import load_image


class Entity:
    def __init__(self, x: float, y: float, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.FRect(self.x, self.y, self.width, self.height)
        self.action = "idle"
        self.frame: float = 0
        self.img_id: str | None = None
        self.flip = False
        self.img: pygame.Surface | None = None
        self.movement: list[float] = [0, 0]
        self.animation_database: dict[str, list[str] | list[pygame.Surface]] = {}
        self.animation_frames: dict[str, pygame.Surface] = {}

    def change_action(self, new_action: str) -> None:
        if self.action != new_action:
            self.action = new_action
            self.frame = 0


class SimpleEntity:
    def __init__(self, img: str | Path, loc: list[float]) -> None:
        self.loc = loc
        self.img = load_image(img)

    def render(self, surf: pygame.Surface, scroll: list[float]) -> None:
        surf.blit(self.img, (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(
            self.loc[0], self.loc[1], self.img.get_width(), self.img.get_height()
        )

    def collision_test(self, rect: pygame.Rect | pygame.FRect) -> bool:
        r = self.get_rect()
        return r.colliderect(rect)
