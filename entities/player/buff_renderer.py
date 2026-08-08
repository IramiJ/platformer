from __future__ import annotations

import math
from typing import TYPE_CHECKING

import pygame

from core.asset_cache import load_image

if TYPE_CHECKING:
    from entities.player.player import Player
    from ui.font_renderer import Font


class BuffRenderer:
    def __init__(self, font: Font, buff_list: dict[str, dict[str, str]]) -> None:
        self.font = font
        self.buff_list = buff_list
        self.imgs: dict[str, pygame.Surface] = {}
        for buff in buff_list:
            self.imgs[buff] = load_image(buff_list[buff]["asset_path"])

    def render_buffs(self, display: pygame.Surface, player: Player) -> None:
        y_offset = 0
        for buff in self.buff_list:
            if buff in player.buffs:
                location = [320 - self.imgs[buff].get_width() - 20, 20 + y_offset]
                self.font.render(
                    display,
                    str(math.ceil(player.buffs[buff])),
                    [320 - 10, 40 + y_offset],
                )
                display.blit(self.imgs[buff], location)
                y_offset += self.imgs[buff].get_height()
