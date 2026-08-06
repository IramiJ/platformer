from core.paths import require_asset_file
from entities.entity import simple_entity
from entities.player.player import Player


class Coins:
    def __init__(self):
        self.objects = []

    def draw_coins(self, display, scroll):
        for coin in self.objects:
            coin.render(display, scroll.render_scroll)

    def coin_collisions(self, player: Player):
        for coin in self.objects:
            if coin.collision_test(player.rect):
                coin.alive = False
                if player.double_coin_buff:
                    player.coin_amount += 2
                else:
                    player.coin_amount += 1
        self.objects = [coin for coin in self.objects if coin.alive]


class Coin(simple_entity):
    def __init__(self, loc):
        super().__init__(require_asset_file("collectables/coin.png"), loc)
        self.alive = True
