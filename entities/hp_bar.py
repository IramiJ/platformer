from pathlib import Path

import pygame


class HpBar:
    def __init__(self, bg: str | Path, frame: str | Path, x: float, y: float) -> None:
        self.bg = pygame.image.load(bg).convert()
        self.bg.set_colorkey((0, 0, 0))
        self.frame = pygame.image.load(frame).convert()
        self.frame.set_colorkey((0, 0, 0))
        self.x = x
        self.y = y
        self.width = self.frame.get_width()
        self.height = self.frame.get_height()

    def draw(
        self,
        display: pygame.Surface,
        max_hp: int,
        current_hp: int,
        position: tuple[float, float] | None = None,
    ) -> None:

        if position is None:
            x, y = self.x, self.y
        else:
            x, y = position

        display.blit(self.frame, (x, y))
        fill_width = int(self.width * (current_hp / max_hp))
        fill_rect = pygame.Rect(0, 0, fill_width, self.height)
        display.blit(self.bg, (x, y), fill_rect)
