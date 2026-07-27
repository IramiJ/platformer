from entities.entity import simple_entity
from entities.player.player import Player


class Coins:
    def __init__(self):
        self.objects = []
        self.objects.append(simple_entity("assets/collectables/coin.png", [160, 308]))

    def draw_coins(self, display, scroll):
        for coin in self.objects:
            coin.render(display, scroll.render_scroll)

    def coin_collisions(self, player: Player):
        for coin in self.objects:
            if coin.collision_test(player.rect):
                self.objects.remove(coin)
                if player.double_coin_buff:
                    player.cion_amount += 2
                else:
                    player.coin_amount += 1
