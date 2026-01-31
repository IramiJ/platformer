from entities.entity import simple_entity

class Coins:
    def __init__(self):
        self.objects = []
        self.objects.append(simple_entity('assets/collectables/coin.png', [160, 308]))
        self.amount = 1000

    def handle_coins(self, display, player, scroll):
        for coin in self.objects:
            coin.render(display, scroll.render_scroll)
            if coin.collision_test(player.rect):
                self.objects.remove(coin)
                if player.double_coin_buff:
                    self.amount += 2
                else:
                    self.amount += 1