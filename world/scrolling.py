from world.tilemap import last_x

class Scroll:
    def __init__(self):
        self.true_scroll = [0, 0]
        self.shake_offset = [0, 0]
        self.render_scroll = [a+b for a, b in zip(self.true_scroll, self.shake_offset)]

    def player_scrolling(self, player, map):
        if player.rect.x < 150:
            self.true_scroll[0] -= self.true_scroll[0]
        elif player.rect.x + 16 > last_x(map) - 150:
            self.true_scroll[0]  += -self.true_scroll[0] -300 + last_x(map)
        else:
            self.true_scroll[0] += player.rect.x - self.true_scroll[0] -150
        self.true_scroll[1] += player.rect.y - self.true_scroll[1] - 100
        self.render_scroll = [a+b for a, b in zip(self.true_scroll, self.shake_offset)]