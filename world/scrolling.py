from entities.player.player import Player
from world.level_loader import Level_loader
from world.tilemap import last_x
from random import randint
from core.settings import TILE_SIZE, Settings

class Scroll:
    def __init__(self):
        self.true_scroll = [0, 0]
        self.shake_offset = [0, 0]
        self.shake_timer = 0
        self.shake_strength = 0
        self.render_scroll = [
            a + b for a, b in zip(self.true_scroll, self.shake_offset)
        ]

    def player_scrolling(self, player: Player, level: Level_loader) -> None:
        if player.rect.x < (Settings.window_size[0]/2 - TILE_SIZE)/2:
            self.true_scroll[0] = 0
        elif player.rect.x + 16 > last_x(level.map) - Settings.window_size[0]/2:
            self.true_scroll[0] = -(Settings.window_size[0] - TILE_SIZE/2) + last_x(level.map)
        else:
            self.true_scroll[0] = player.rect.x - (Settings.window_size[0]/2 - TILE_SIZE)/2
        if player.rect.y > level.max_y_px:
            self.true_scroll[1] = 0
        else:
            self.true_scroll[1] = player.rect.y - Settings.window_size[1]/5
        self.render_scroll = [
            a + b for a, b in zip(self.true_scroll, self.shake_offset)
        ]
        self.shake()

    def shake(self) -> None:
        if self.shake_timer > 0:
            self.shake_offset = [
                randint(-self.shake_strength, self.shake_strength),
                randint(-self.shake_strength, self.shake_strength),
            ]
            self.shake_timer -= 1
        else:
            self.shake_offset = [0, 0]
