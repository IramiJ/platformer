from entities.enemies.patroller import Patroller
from entities.enemies.chaser import Chaser
from entities.enemies.shooter import Shooter
class Enemies:
    def __init__(self):
        self.enemies = [Patroller(88, 304, 16, 16), Chaser(88, 304, 16, 16), Shooter(88, 304, 16, 16)]
    def handle_enemies(self, player, display, bullet_list):
        for enemy in self.enemies:
            if isinstance(enemy, Chaser):
                enemy.move(player)
            elif not isinstance(enemy, Shooter):
                enemy.move()
            enemy.update_frames()
            enemy.render(display, player.scroll)
            if isinstance(enemy, Shooter):
                enemy.attack(player, bullet_list)
            else:
                enemy.attack(player)
            player.attack(enemy)
        self.enemies = [e for e in self.enemies if e.alive]
        


