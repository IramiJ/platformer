import pygame

from core.asset_cache import load_font


class WinScreen:
    def __init__(self) -> None:
        self.small_font = load_font("fonts/small_font.png")
        self.large_font = load_font("fonts/large_font.png")
        self.displaying = False

    def render(self, surf: pygame.Surface) -> None:
        surf.fill((0, 0, 0))
        self.large_font.render(surf, "YOU WON", (130, 0))

    def change_displaying(self) -> None:
        self.displaying = not self.displaying
