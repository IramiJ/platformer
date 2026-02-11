from entities.enemies.patroller import Patroller
from entities.enemies.chaser import Chaser
from entities.enemies.shooter import Shooter
class Enemies:
    def __init__(self):
        self.enemy_types = {"Patroller": Patroller, "Chaser": Chaser, "Shooter": Shooter}
        self.enemies = []
    def handle_enemies(self, player, display, bullet_list, scroll, tiles, logic_variables, sparks):
        for enemy in self.enemies:
            if isinstance(enemy, Chaser):
                enemy.move(player, tiles)
            elif not isinstance(enemy, Shooter):
                enemy.move()
            enemy.update_frames()
            enemy.render(display, scroll.render_scroll)
            if isinstance(enemy, Shooter):
                enemy.attack(player, bullet_list, scroll)
            else:
                enemy.attack(player, scroll)
            player.attack(enemy, logic_variables, sparks)
        self.enemies = [e for e in self.enemies if e.alive]
    def load_enemies(self, level):
        self.enemies = []
        enemies = level.data["enemies"]
        for enemy_name, spawns in enemies.items():
            enemy_class = self.enemy_types.get(enemy_name)
            for (x, y) in spawns:
                self.enemies.append(enemy_class(x*16,y*16,16,16))
    
        


