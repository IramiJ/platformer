from random import randint

from core.settings import REFERENCE_TICKS_PER_SECOND, TILE_SIZE, Settings
from entities.player.player import Player
from world.level_loader import LevelLoader
from world.tilemap import last_x

SHAKE_SAMPLE_INTERVAL = 1.0 / REFERENCE_TICKS_PER_SECOND


class Scroll:
    def __init__(self) -> None:
        self.true_scroll: list[float] = [0, 0]
        self.shake_offset: list[float] = [0, 0]
        self.shake_timer: float = 0
        self.shake_sample_timer: float = 0
        self.shake_strength: int = 0
        self.render_scroll: list[float] = [
            a + b for a, b in zip(self.true_scroll, self.shake_offset)
        ]

    def player_scrolling(self, player: Player, level: LevelLoader, dt: float) -> None:
        if player.rect.x < (Settings.window_size[0] / 2 - TILE_SIZE) / 2:
            self.true_scroll[0] = 0
        elif (
            player.rect.x - Settings.window_size[0] / 4 + TILE_SIZE
            > last_x(level.map) - Settings.window_size[0] / 2
        ):
            self.true_scroll[0] = last_x(level.map) - Settings.window_size[0] / 2
        else:
            self.true_scroll[0] = (
                player.rect.x - (Settings.window_size[0] / 2 - TILE_SIZE) / 2
            )
        if player.rect.y > level.max_y_px:
            self.true_scroll[1] = 0
        else:
            self.true_scroll[1] = player.rect.y - Settings.window_size[1] / 5
        self.shake(dt)
        self.render_scroll = [
            a + b for a, b in zip(self.true_scroll, self.shake_offset)
        ]

    def shake(self, dt: float) -> None:
        if self.shake_timer > 0:
            self.shake_sample_timer -= dt
            while self.shake_sample_timer < 0:
                self.shake_offset = [
                    randint(-self.shake_strength, self.shake_strength),
                    randint(-self.shake_strength, self.shake_strength),
                ]
                self.shake_sample_timer += SHAKE_SAMPLE_INTERVAL
            self.shake_timer = max(0.0, self.shake_timer - dt)
        else:
            self.shake_offset = [0, 0]
            self.shake_sample_timer = 0
