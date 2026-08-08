from __future__ import annotations

from typing import TYPE_CHECKING

from core.paths import require_asset_file
from ui.font_renderer import Font
from world.coordinates import tile_to_pixel

if TYPE_CHECKING:
    import pygame

    from world.scrolling import Scroll


class Texts:
    def __init__(self) -> None:
        self.strings: dict[str, list[int]] = {}
        self.large_font = Font(require_asset_file("fonts/large_font.png"))

    def load_texts(self, data: dict[str, list[int]]) -> None:
        self.strings = data

    def render_texts(self, display: pygame.Surface, scroll: Scroll) -> None:
        for text in self.strings:
            self.large_font.render(
                display,
                text,
                [
                    tile_to_pixel(self.strings[text][0]) - scroll.render_scroll[0],
                    tile_to_pixel(self.strings[text][1]) - scroll.render_scroll[1],
                ],
            )
