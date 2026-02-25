from entities.enemies.patroller import Patroller
from entities.enemies.chaser import Chaser
from entities.enemies.shooter import Shooter
from .heavy_patroller import Heavy_Patroller
import pygame

class Enemies:
    def __init__(self):
        self.enemy_types = {"Patroller": Patroller, "Chaser": Chaser, "Shooter": Shooter, "Heavy_Patroller": Heavy_Patroller}
        self.enemies = []
    def handle_enemies(self, player, display, bullet_list, scroll, tiles, logic_variables, sparks, dt):
        for enemy in self.enemies:
            if isinstance(enemy, Chaser):
                enemy.move(player, tiles, dt)
            elif not isinstance(enemy, Shooter):
                enemy.move(dt)
            enemy.update_frames(dt)
            enemy.render(display, scroll.render_scroll)
#            pygame.draw.rect(display, (255,0,0), pygame.Rect(enemy.rect.left - scroll.render_scroll[0], enemy.rect.top - scroll.render_scroll[1], 16, 16))
            if isinstance(enemy, Shooter):
                enemy.attack(player, bullet_list, scroll)
            else:
                enemy.attack(player, scroll)
            player.attack(enemy, logic_variables, sparks, dt)
        length = int(len(self.enemies))
        self.enemies = [e for e in self.enemies if e.alive]
        if len(self.enemies) < length:
            player.coin_amount += 2
    def load_enemies(self, level):
        self.enemies = []
        enemies = level.data["enemies"]
        for enemy_name, spawns in enemies.items():
            enemy_class = self.enemy_types.get(enemy_name)
            for (x, y) in spawns:
                self.enemies.append(enemy_class(x*16,y*16,16,16))
    
        


