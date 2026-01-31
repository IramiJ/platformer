from world.tilemap import last_x
from random import randint

class Scroll:
    def __init__(self):
        self.true_scroll = [0, 0]
        self.shake_offset = [0, 0]
        self.shake_timer = 0
        self.shake_strength = 0
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
        self.shake()
    def shake(self):
        if self.shake_timer > 0:
            self.shake_offset = [randint(-self.shake_strength, self.shake_strength), randint(-self.shake_strength, self.shake_strength)]
            self.shake_timer -= 1
        else:
            self.shake_offset = [0, 0]

