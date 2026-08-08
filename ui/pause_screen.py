import pygame

from core.paths import require_asset_file
from ui.font_renderer import Font


class PauseScreen:
    def __init__(self) -> None:
        self.small_font = Font(require_asset_file("fonts/small_font.png"))
        self.large_font = Font(require_asset_file("fonts/large_font.png"))
        self.displaying = False

    def render(self, surf: pygame.Surface) -> None:
        surf.fill((0, 0, 0))
        self.large_font.render(surf, "PAUSE", (144, 0))

    def change_displaying(self) -> None:
        self.displaying = not self.displaying
