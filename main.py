import pygame
import time
from ui.death_screen import Death_screen


from ui.Font_renderer import Font
from ui.shopping import Shop
from world.tilemap import load_tiles, display_map, update_tile_rects
from entities.entity import entity, simple_entity
from entities.player.player import Player
from entities.hp_bar import Hp_bar
from core.settings import Settings, TILE_SIZE
from world.scrolling import Scroll
from core.kb_event_handling import Keyboard_event_handler
from entities.enemies.enemies import Enemies
from world.level_loader import (
    Level_loader,
    initialize_player,
    update_level,
    reach_checkpoint,
)
from core.logic_variables import Logic_variables
from ui.pause_screen import Pause_screen
from ui.win_screen import Win_screen
from entities.player.buff_renderer import Buff_renderer
from entities.player.render_ammo import Ammo
from world.texts import Texts
from ui.minimap import Minimap
from world.foliage.leafSystem import LeafSystem
from world.foliage.tree import Tree
from world.coordinates import tile_position_to_pixel, tile_to_pixel
from world.tilemap import last_x
from core.paths import assets_path, PROJECT_ROOT

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.window_size = [640, 480]
        self.screen = pygame.display.set_mode(Settings.window_size)
        self.display = pygame.Surface(
            (self.window_size[0] // 2, self.window_size[1] // 2)
        )
        pygame.display.set_caption(Settings.caption)

        self.tiles = load_tiles(assets_path("tiles"))
        self.level = Level_loader()
        self.level.load_level(PROJECT_ROOT / "world/levels/level1.json")
        self.player = Player(
            tile_to_pixel(self.level.data["spawn"][0]), tile_to_pixel(self.level.data["spawn"][1]), 24, 24
        )
        self.hp_bar = Hp_bar(
            assets_path("hp_bar/hp_bar_bg.png"), assets_path("hp_bar/hp_bar_frame.png"), 0, 0
        )
        self.small_font = Font(assets_path("fonts/small_font.png"))
        self.large_font = Font(assets_path("fonts/large_font.png"))
        self.logic_variables = Logic_variables()
        self.shop = Shop()
        self.pause_screen = Pause_screen()
        self.death_screen = Death_screen()
        self.win_screen = Win_screen()
        self.enemies = Enemies()
        self.ammo = Ammo()
        self.enemies.load_enemies(self.level)
        self.bullets = []
        self.sparks = []
        self.tile_rects = []
        self.minimap = Minimap()
        self.texts = Texts()
        self.texts.load_texts(self.level.data["texts"])
        self.scroll = Scroll()
        self.frames = 0
        self.current_fps = 0
        self.last_time = time.time()
        self.keyboard_event_handler = Keyboard_event_handler()
        self.buff_renderer = Buff_renderer(self.small_font, self.shop.data)
        self.leafSystem = LeafSystem()
        self.tree = Tree([240, 320])

    def run(self):
        while True:
            self.update_dt()
            self.update_fps_counter()

            self.handle_input()

            self.evaluate_game_state()

            self.update()

            self.render()

            self.present()

    def render(self):
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

    def update_dt(self):
        self.dt = self.clock.tick(Settings.fps) / 1000

    def update_fps_counter(self):
        self.frames += 1

        if time.time() - self.last_time >= 1:
            self.current_fps = self.frames
            self.frames = 0
            self.last_time = time.time()

    def evaluate_overlay_state(self):
        self.dead = self.player.hp <= 0
        self.overlay_active = (
            self.shop.displaying
            or self.pause_screen.displaying
            or self.win_screen.displaying
            or self.dead
        )

    def update_logic_variables(self):
        self.logic_variables.MOVEMENTS = not self.overlay_active
        self.logic_variables.RENDER = True

    def display_overlays(self):
        if self.shop.displaying:
            self.shop.show(self.display, self.player)
        elif self.pause_screen.displaying:
            self.pause_screen.render(self.display)
        elif self.win_screen.displaying:
            self.win_screen.render(self.display)
        elif self.dead:
            self.death_screen.render(self.display)

    def move_bullets(self):
        for bullet in self.bullets:
            bullet.move(self.player, self.scroll, self.dt)
        self.bullets = [
            bullet
            for bullet in self.bullets
            if bullet.alive
        ]

    def render_bullets(self):
        for bullet in self.bullets:
            bullet.render(self.display, self.scroll.render_scroll)

    def draw_sparks(self):
        for i, spark in sorted(enumerate(self.sparks), reverse=True):
            spark.draw(self.display, self.scroll)

    def move_sparks(self):
        for i, spark in sorted(enumerate(self.sparks), reverse=True):
            spark.move(self.dt)
        self.sparks = [
            spark
            for spark in self.sparks
            if spark.alive
        ]

    def render_fps_count(self):
        self.large_font.render(self.display, f"fps: {self.current_fps}", [120, 0])

    def show_remaining_enemies(self):
        self.small_font.render(
            self.display,
            f"{self.enemies.current_enemy_amount}/{self.enemies.max_enemy_amount} enemies left",
            [0, 25],
        )

    def fill_display(self):
        self.display.fill((0, 0, 0))

    def render_map(self):
        display_map(self.display, self.scroll, self.level.map, self.tiles)

    def update_tile_rects(self):
        self.tile_rects = []
        update_tile_rects(self.display, self.scroll, self.tile_rects, self.level.map)

    def draw_render_surf(self):
        self.surf = pygame.transform.scale(self.display, Settings.window_size)
        self.screen.blit(self.surf, (0, 0))

    def handle_input(self):
        self.keyboard_event_handler.handle_keyboard_events(
            self.player, self.shop, self.pause_screen, self.win_screen
        )

    def reload_on_respawn(self):
        if self.player.respawn:
            self.reset_session()

    def evaluate_game_state(self):
        self.evaluate_overlay_state()
        self.update_logic_variables()

    def update(self):
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
        

    def update_gameplay(self):
        self.update_tile_rects()
        self.player.update(self.tile_rects, self.enemies.enemies, self.level.max_y_px, self.dt)
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

    def initialize_loaded_level(self):
        self.enemies.load_enemies(self.level)
        self.texts.load_texts(self.level.data["texts"])
        initialize_player(self.player, self.level)
        self.reset_transient_state()
        self.update_tile_rects()

    def reset_session(self):
        self.level.id = 1
        self.player.hp = self.player.max_hp
        self.player.buffs.clear()
        self.player.respawn = False

        self.shop.displaying = False
        self.pause_screen.displaying = False
        self.win_screen.displaying = False

        self.level.reload_level()
        self.initialize_loaded_level()
    
    def present(self):
        self.draw_render_surf()
        pygame.display.update()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    pygame.init()
    main()
