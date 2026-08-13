from __future__ import annotations

import time
from typing import TYPE_CHECKING

import pygame

from core.asset_cache import load_font
from core.kb_event_handling import KeyboardEventHandler
from core.logic_variables import LogicVariables
from core.paths import PROJECT_ROOT, require_asset_dir, require_asset_file
from core.profiler import Profiler
from core.settings import Settings
from entities.enemies.enemies import Enemies
from entities.hp_bar import HpBar
from entities.player.buff_renderer import BuffRenderer
from entities.player.player import Player
from entities.player.render_ammo import Ammo
from ui.death_screen import DeathScreen
from ui.minimap import Minimap
from ui.pause_screen import PauseScreen
from ui.shopping import Shop
from ui.win_screen import WinScreen
from world.coordinates import tile_to_pixel
from world.foliage.leaf_system import LeafSystem
from world.foliage.tree import Tree
from world.level_loader import (
    LevelLoader,
    initialize_player,
    reach_checkpoint,
    update_level,
)
from world.scrolling import Scroll
from world.texts import Texts
from world.tilemap import display_map, load_tiles, update_tile_rects

if TYPE_CHECKING:
    from entities.enemies.shooter_bullet import ShooterBullet
    from entities.spark import Spark


class Game:
    """Owns the main pygame runtime and coordinates all game systems.

    Game wires together input, rendering, level loading, player state, enemies,
    projectiles, UI overlays, camera scrolling, and transient visual effects.
    It controls the frame loop and decides which systems update depending on
    pause, shop, death, win, and hitstop state.
    """

    def __init__(self, profiling: bool = False) -> None:
        self.profiler = Profiler(enabled=profiling)
        self.clock = pygame.time.Clock()
        self.window_size: list[int] = [640, 480]
        self.screen = pygame.display.set_mode(Settings.window_size)
        self.display = pygame.Surface(
            (self.window_size[0] // 2, self.window_size[1] // 2)
        )
        pygame.display.set_caption(Settings.caption)
        self.surf = pygame.Surface(Settings.window_size)

        with self.profiler.measure("assets.tiles"):
            self.tiles = load_tiles(require_asset_dir("tiles"))
        with self.profiler.measure("level.load"):
            self.level = LevelLoader()
            self.level.load_level(PROJECT_ROOT / "world/levels/level1.json")
        with self.profiler.measure("assets.player"):
            self.player = Player(
                tile_to_pixel(self.level.data["spawn"][0]),
                tile_to_pixel(self.level.data["spawn"][1]),
                24,
                24,
            )
        with self.profiler.measure("assets.hud"):
            self.hp_bar = HpBar(
                require_asset_file("hp_bar/hp_bar_bg.png"),
                require_asset_file("hp_bar/hp_bar_frame.png"),
                0,
                0,
            )
            self.small_font = load_font("fonts/small_font.png")
            self.large_font = load_font("fonts/large_font.png")
        self.logic_variables = LogicVariables()
        with self.profiler.measure("assets.overlays"):
            self.shop = Shop()
            self.pause_screen = PauseScreen()
            self.death_screen = DeathScreen()
            self.win_screen = WinScreen()
        with self.profiler.measure("assets.enemies"):
            self.enemies = Enemies()
            self.enemies.load_enemies(self.level)
        with self.profiler.measure("assets.ammo"):
            self.ammo = Ammo()
        self.bullets: list[ShooterBullet] = []
        self.sparks: list[Spark] = []
        self.tile_rects: list[pygame.Rect] = []
        self.minimap = Minimap()
        with self.profiler.measure("assets.texts"):
            self.texts = Texts()
            self.texts.load_texts(self.level.data["texts"])
        self.scroll = Scroll()
        self.frames = 0
        self.current_fps = 0
        self.last_time = time.time()
        self.keyboard_event_handler = KeyboardEventHandler()
        with self.profiler.measure("assets.buffs"):
            self.buff_renderer = BuffRenderer(self.small_font, self.shop.data)
        with self.profiler.measure("assets.foliage"):
            self.leafSystem = LeafSystem()
            self.tree = Tree([240, 320])
        self.dt: float
        self.dead: bool
        self.overlay_active: bool
        self.surf: pygame.Surface

    def run(self) -> None:
        """Run the main game loop until the process exits."""
        while True:
            self.update_dt()
            self.run_frame()
            self.profiler.finish_frame()

    def run_frame(self) -> None:
        """Process one frame after ``dt`` has been set."""
        with self.profiler.measure("cpu_frame"):
            self.update_fps_counter()

            with self.profiler.measure("input"):
                self.handle_input()

            self.evaluate_game_state()

            with self.profiler.measure("update"):
                self.update()

            with self.profiler.measure("render"):
                self.render()

            with self.profiler.measure("present"):
                self.present()

    def render(self) -> None:
        """
        Takes care of all the render logic, such as the player, the enemies, the UI, projectiles and so on.
        """
        if self.logic_variables.RENDER:
            self.fill_display()
            self.render_map()
            self.enemies.render_enemies(self.display, self.scroll)
            self.render_bullets()
            self.show_remaining_enemies()
            self.tree.render(self.display, self.scroll)
            self.leafSystem.render_leaves(self.display, self.scroll)
            self.player.run_render_logic(self.display, self.scroll)
            self.texts.render_texts(self.display, self.scroll)
            self.hp_bar.draw(self.display, self.player.max_hp, self.player.hp)
            self.buff_renderer.render_buffs(self.display, self.player)
            self.ammo.render_ammo(self.display, self.player)
            self.draw_sparks()
            self.minimap.render(self.display)
            self.render_fps_count()
            self.display_overlays()

    def update_dt(self) -> None:
        self.dt = self.clock.tick(Settings.fps) / 1000

    def update_fps_counter(self) -> None:
        self.frames += 1

        if time.time() - self.last_time >= 1:
            self.current_fps = self.frames
            self.frames = 0
            self.last_time = time.time()

    def evaluate_overlay_state(self) -> None:
        self.dead = self.player.hp <= 0
        self.overlay_active = (
            self.shop.displaying
            or self.pause_screen.displaying
            or self.win_screen.displaying
            or self.dead
        )

    def update_logic_variables(self) -> None:
        self.logic_variables.MOVEMENTS = not self.overlay_active
        self.logic_variables.RENDER = True

    def display_overlays(self) -> None:
        if self.shop.displaying:
            self.shop.show(self.display, self.player)
        elif self.pause_screen.displaying:
            self.pause_screen.render(self.display)
        elif self.win_screen.displaying:
            self.win_screen.render(self.display)
        elif self.dead:
            self.death_screen.render(self.display)

    def move_bullets(self) -> None:
        for bullet in self.bullets:
            bullet.move(self.player, self.scroll, self.dt)
        self.bullets = [bullet for bullet in self.bullets if bullet.alive]

    def render_bullets(self) -> None:
        for bullet in self.bullets:
            bullet.render(self.display, self.scroll.render_scroll)

    def draw_sparks(self) -> None:
        for i, spark in sorted(enumerate(self.sparks), reverse=True):
            spark.draw(self.display, self.scroll)

    def move_sparks(self) -> None:
        for i, spark in sorted(enumerate(self.sparks), reverse=True):
            spark.move(self.dt)
        self.sparks = [spark for spark in self.sparks if spark.alive]

    def render_fps_count(self) -> None:
        self.large_font.render(self.display, f"fps: {self.current_fps}", [120, 0])

    def show_remaining_enemies(self) -> None:
        self.small_font.render(
            self.display,
            f"{self.enemies.current_enemy_amount}/{self.enemies.max_enemy_amount} enemies left",
            [0, 25],
        )

    def fill_display(self) -> None:
        self.display.fill((0, 0, 0))

    def render_map(self) -> None:
        display_map(self.display, self.scroll, self.level.map, self.tiles)

    def update_tile_rects(self) -> None:
        self.tile_rects = []
        update_tile_rects(self.display, self.scroll, self.tile_rects, self.level.map)

    def draw_render_surf(self) -> None:
        pygame.transform.scale(self.display, Settings.window_size, self.surf)
        self.screen.blit(self.surf, (0, 0))

    def handle_input(self) -> None:
        self.keyboard_event_handler.handle_keyboard_events(
            self.player, self.shop, self.pause_screen, self.win_screen
        )

    def reload_on_respawn(self) -> None:
        """
        When respawning, resets the entire game session to the beginning
        """
        if self.player.respawn:
            self.reset_session()

    def evaluate_game_state(self) -> None:
        """
        Determines which overlay needs to be displayed
        """
        self.evaluate_overlay_state()
        self.update_logic_variables()

    def update(self) -> None:
        """
        Takes care of all non-render logic, such as gameplay updates, UI updates and hitstops.
        """
        if self.dead:
            self.reload_on_respawn()
            return
        if self.win_screen.displaying:
            return
        if self.pause_screen.displaying:
            return
        if self.shop.displaying:
            self.shop.update(self.player)
            return
        if self.logic_variables.MOVEMENTS and self.logic_variables.hitstop_timer > 0:
            self.logic_variables.hitstop_timer = max(
                0.0, self.logic_variables.hitstop_timer - self.dt
            )
            return

        self.update_gameplay()

    def update_gameplay(self) -> None:
        """
        Takes care of all the updates surrounding the player, the map the enemies, projectiles, the level and the minimap
        """
        self.update_tile_rects()
        self.player.update(
            self.tile_rects, self.enemies.enemies, self.level.max_y_px, self.dt
        )
        with self.profiler.measure("enemies"):
            self.enemies.update_enemies(
                self.player,
                self.bullets,
                self.scroll,
                self.tile_rects,
                self.logic_variables,
                self.sparks,
                self.dt,
            )
        self.scroll.player_scrolling(self.player, self.level, self.dt)
        self.move_bullets()
        self.move_sparks()
        self.leafSystem.update(self.tree, self.dt)
        self.minimap.update_map(
            [self.player.rect.x, self.player.rect.y], self.level.map
        )
        if update_level(
            self.player,
            self.level,
            self.enemies,
            self.texts,
            self.win_screen,
        ):
            self.initialize_loaded_level()
        reach_checkpoint(self.player, self.level)

    def reset_transient_state(self) -> None:
        """
        Clear temporary effects and movement state after respawn or level changes.
        """
        # Clearing projectiles
        self.bullets.clear()
        self.player.bow.arrows.clear()
        self.sparks.clear()
        self.player.sword.particles.clear()
        self.leafSystem.leaves.clear()

        # Clearing player movements:
        self.player.movement = [0, 0]
        self.player.y_momentum = 0
        self.player.air_timer = 0
        self.player.moving_left = False
        self.player.moving_right = False

        # Clearing Dashes
        self.player.dashing = False
        self.player.dash_timer = 0
        self.player.dash_cooldown = 0
        self.player.dmg_cd = 0

        # Bow
        self.player.bow.shoot_cd = 0
        self.player.bow.reload_cd = 0
        self.player.bow.reloading = False
        self.player.bow.add_ammo = False

        # Global effects
        self.logic_variables.hitstop_timer = 0
        self.scroll.shake_timer = 0
        self.scroll.shake_strength = 0
        self.scroll.shake_offset = [0, 0]
        self.scroll.shake_sample_timer = 0

    def initialize_loaded_level(self) -> None:
        """Initializes everything regarding the level, such as enemies, the player, the texts on the screen and the map"""
        self.enemies.load_enemies(self.level)
        self.texts.load_texts(self.level.data["texts"])
        initialize_player(self.player, self.level)
        self.reset_transient_state()
        self.update_tile_rects()

    def reset_session(self) -> None:
        """Resets everything to the beginning level, as if you were to restart the game entirely"""
        self.level.id = 1
        self.player.hp = self.player.max_hp
        self.player.buffs.clear()
        self.player.respawn = False

        self.shop.displaying = False
        self.pause_screen.displaying = False
        self.win_screen.displaying = False

        self.level.reload_level()
        self.initialize_loaded_level()

    def present(self) -> None:
        self.draw_render_surf()
        pygame.display.update()


def main(profiling: bool = False) -> None:
    game = Game(profiling=profiling)
    game.run()


if __name__ == "__main__":
    import sys

    pygame.init()
    main(profiling="--profile" in sys.argv[1:])
