

import pygame, time

from ui.death_screen import Death_screen
from world.torch import Torch
pygame.init()
from ui.Font_renderer import Font
from ui.shopping import Shop
from world.tilemap import *
from entities.entity import *
from entities.player.player import Player
from entities.hp_bar import Hp_bar
from core.settings import Settings
from entities.animations import draw_constants, load_animation
# from entities.player.player_movements import player_movements
from world.scrolling import Scroll
from core.kb_event_handling import kb_events
from entities.enemies.enemies import Enemies
from entities.coins import Coins
from world.level_loader import Level_loader, update_level, reach_checkpoint, reload_level
from core.logic_variables import Logic_variables
from ui.pause_screen import Pause_screen
from ui.win_screen import Win_screen
from entities.player.render_buffs import render_buffs
from entities.player.render_ammo import Ammo
from world.texts import Texts

class Game():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.window_size = [640, 480]
        self.screen = pygame.display.set_mode(Settings.window_size)
        self.display = pygame.Surface((window_size[0]//2,window_size[1]//2))
        pygame.display.set_caption(Settings.caption)

        self.tiles = load_tiles('assets/tiles')
        self.level = Level_loader()
        self.level.load_level('world/levels/level1.json')
        self.player = Player(self.level.data['spawn'][0],self.level.data['spawn'][1],16,16)
        self.hp_bar = Hp_bar("assets/hp_bar/hp_bar_bg.png","assets/hp_bar/hp_bar_frame.png", 0, 0)
        self.small_font = Font('assets/fonts/small_font.png')
        self.large_font = Font('assets/fonts/large_font.png')
        self.coins = Coins()
        self.logic_variables = Logic_variables() 
        self.shop = Shop()
        self.pause_screen = Pause_screen()
        self.death_screen = Death_screen()
        self.win_screen = Win_screen()
        self.enemies = Enemies()
        self.ammo = Ammo()
        self.enemies.load_enemies(self.level)
        self.bullets = []
        self.torches = []
        self.sparks = []
        self.texts = Texts()
        self.texts.load_texts(self.level.data["texts"])
        load_torches(self.level.map, self.torches)
        self.scroll = Scroll()
        self.frames = 0
        self.current_fps = 0
        self.last_time = time.time()

    def run(self):
        while True:
            self.dt = self.clock.tick(Settings.fps) / 1000  
            self.dt *= 60 # Running the game on 60fps, regardless of the framerate
            # FPS counting
            self.frames += 1
            
            if time.time() - self.last_time >= 1:
                self.current_fps = self.frames
                self.frames = 0
                self.last_time = time.time()
            
            kb_events(self.player, self.shop, self.pause_screen)

            # Logic evaluations
            self.dead = (self.player.hp <= 0) 
            self.overlay_active = self.shop.displaying or self.pause_screen.displaying or self.win_screen.displaying or self.dead
            # Logic handling
            self.logic_variables.MOVEMENTS = not self.overlay_active
            self.logic_variables.RENDER = True
            # Draw logic  
            if logic_variables.RENDER:  
                self.display.fill((0,0,0))
                self.coins.draw_coins(self.display, self.scroll)       
                self.tile_rects = []
                display_map(self.display, self.scroll, self.tile_rects, self.level.map, self.tiles)
                self.player.update_frames(self.dt)
                self.player.draw(self.display, self.scroll, self.dt)
                self.texts.render_texts(self.display, self.scroll)
                self.hp_bar.draw(self.display, self.player.max_hp, self.player.hp)
                render_buffs(self.shop.data, self.display, self.player)
                self.ammo.render_ammo(self.display, self.player)
                for torch in self.torches:
                    torch.draw(self.display, self.scroll)
                for i, spark in sorted(enumerate(self.sparks), reverse=True):
                    spark.draw(self.display, self.scroll)
                self.large_font.render(self.display, f"fps: {self.current_fps}", [120, 0])


            # Overlay displays
            if self.shop.displaying:
                self.shop.show(self.display, self.player)
            elif self.pause_screen.displaying:
                self.pause_screen.render(self.display)
            elif self.win_screen.displaying:
                self.win_screen.render(self.display)
            elif self.dead:
                self.death_screen.render(self.display)
                if self.player.respawn:
                    self.player.revive(self.level)
                    reload_level(self.enemies, self.level, self.torches, self.player, self.texts)
                
            # Movement logic
            if self.logic_variables.MOVEMENTS and self.logic_variables.hitstop_timer <= 0:
                self.player.handle_movements(self.tile_rects, self.display, self.player.tail, self.scroll, self.dt)
                self.enemies.handle_enemies(self.player, self.display, self.bullets, self.scroll, self.tile_rects, self.logic_variables, self.sparks, self.dt)
                self.scroll.player_scrolling(self.player, self.level)
                for bullet in self.bullets:
                    bullet.move(self.player, self.display, self.bullets, self.scroll, self.dt)
                self.player.pistol.shoot(self.enemies.enemies, self.dt)
                # Player event logic 
                self.player.die_through_falling(self.level.data["max_y"])
                self.player.remove_buffs(["speed boost", "jump boost", "double coin"])
                self.player.update_mode_properties()
                self.player.apply_buffs()
                self.player.manage_attack_cd(self.dt)
                # Spark sword logic
                for i, spark in sorted(enumerate(self.sparks), reverse=True):
                    spark.move(1)
                    if not spark.alive:
                        self.sparks.pop(i)
            else:
                self.logic_variables.hitstop_timer -= 1
            self.surf = pygame.transform.scale(self.display,Settings.window_size)
            update_level(self.player, self.level, self.enemies, self.torches, self.texts, self.win_screen)
            reach_checkpoint(self.player, self.level)
            self.screen.blit(self.surf, (0,0))
            pygame.display.update()

clock = pygame.time.Clock()
window_size = [640, 480]
screen = pygame.display.set_mode(Settings.window_size)
display = pygame.Surface((window_size[0]//2,window_size[1]//2))
pygame.display.set_caption(Settings.caption)

tiles = load_tiles('assets/tiles')
level = Level_loader()
level.load_level('world/levels/level1.json')
player = Player(level.data['spawn'][0],level.data['spawn'][1],16,16)
hp_bar = Hp_bar("assets/hp_bar/hp_bar_bg.png","assets/hp_bar/hp_bar_frame.png", 0, 0)
small_font = Font('assets/fonts/small_font.png')
large_font = Font('assets/fonts/large_font.png')
coins = Coins()
logic_variables = Logic_variables() 
shop = Shop()
pause_screen = Pause_screen()
death_screen = Death_screen()
win_screen = Win_screen()
enemies = Enemies()
ammo = Ammo()
enemies.load_enemies(level)
bullets = []
torches = []
sparks = []
texts = Texts()
texts.load_texts(level.data["texts"])
load_torches(level.map, torches)
scroll = Scroll()
frames = 0
current_fps = 0
last_time = time.time()
#MAIN LOOP-------------------------------------------------------------------------------------------------------------------------------------------------------------
'''
while True:
    dt = clock.tick(Settings.fps) / 1000  
    dt *= 60 # Running the game on 60fps, regardless of the framerate
    # FPS counting
    frames += 1
    
    if time.time() - last_time >= 1:
        current_fps = frames
        frames = 0
        last_time = time.time()
    
    kb_events(player, shop, pause_screen)

    # Logic evaluations
    dead = (player.hp <= 0) 
    overlay_active = shop.displaying or pause_screen.displaying or win_screen.displaying or dead
    # Logic handling
    logic_variables.MOVEMENTS = not overlay_active
    logic_variables.RENDER = True
    # Draw logic  
    if logic_variables.RENDER:  
        display.fill((0,0,0))
        coins.draw_coins(display, scroll)       
        tile_rects = []
        display_map(display, scroll, tile_rects, level.map, tiles)
        player.update_frames(dt)
        player.draw(display, scroll, dt)
        texts.render_texts(display, scroll)
        hp_bar.draw(display, player.max_hp, player.hp)
        render_buffs(shop.data, display, player)
        ammo.render_ammo(display, player)
        for torch in torches:
            torch.draw(display, scroll)
        for i, spark in sorted(enumerate(sparks), reverse=True):
            spark.draw(display, scroll)
        large_font.render(display, f"fps: {current_fps}", [120, 0])


    # Overlay displays
    if shop.displaying:
        shop.show(display, player)
    elif pause_screen.displaying:
        pause_screen.render(display)
    elif win_screen.displaying:
        win_screen.render(display)
    elif dead:
        death_screen.render(display)
        if player.respawn:
            player.revive(level)
            reload_level(enemies, level, torches, player, texts)
        
    # Movement logic
    if logic_variables.MOVEMENTS and logic_variables.hitstop_timer <= 0:
        player.handle_movements( tile_rects, display, player.tail, scroll, dt)
        enemies.handle_enemies(player, display, bullets, scroll, tile_rects, logic_variables, sparks, dt)
        scroll.player_scrolling(player, level)
        for bullet in bullets:
            bullet.move(player, display, bullets, scroll, dt)
        player.pistol.shoot(enemies.enemies, dt)
        # Player event logic 
        player.die_through_falling(level.data["max_y"])
        player.remove_buffs(["speed boost", "jump boost", "double coin"])
        player.update_mode_properties()
        player.apply_buffs()
        player.manage_attack_cd(dt)
        # Spark sword logic
        for i, spark in sorted(enumerate(sparks), reverse=True):
            spark.move(1)
            if not spark.alive:
                sparks.pop(i)
    else:
        logic_variables.hitstop_timer -= 1
    surf = pygame.transform.scale(display,Settings.window_size)
    update_level(player, level, enemies, torches, texts, win_screen)
    reach_checkpoint(player, level)
    screen.blit(surf, (0,0))
    pygame.display.update()
'''

game = Game()
game.run()