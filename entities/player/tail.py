from entities.entity import simple_entity
import math
import random
from core.paths import assets_path

TAIL_WAVE_INTERVAL = 0.1
TAIL_POINT_DURATION = 2.0


class Tail:
    def __init__(self, img, loc):
        self.img = img
        self.loc = loc
        self.points = []
        self.shift = 0
        self.dir = "r"
        self.wave_timer = TAIL_WAVE_INTERVAL
        for i in range(10):
            self.points.append(
                self.Point(self.loc[0] - i, self.loc[1], assets_path("tail/grey.png"))
            )

    def update_points(self, dt):
        if self.dir == "r":
            self.update_right()
        if self.dir == "l":
            self.update_left()
        self.wave_timer -= dt
        while self.wave_timer <= 0:
            self.shift += math.pi / 2
            self.wave_timer += TAIL_WAVE_INTERVAL
        for i in range(len(self.points)):
            self.points[i].loc[1] = self.loc[1] + self.sin_pos(i)

    def update_right(self):
        for i in range(len(self.points)):
            self.points[i].loc[0] = self.loc[0] - i

    def update_left(self):
        for i in range(len(self.points)):
            self.points[i].loc[0] = self.loc[0] + i

    def sin_pos(self, x):
        if self.shift >= 2 * math.pi:
            self.shift = 0
        return 2 * math.sin((math.pi * x / 2) + self.shift)

    class Point(simple_entity):
        def __init__(self, x, y, img):
            super().__init__(img, [x, y])
            self.dur = TAIL_POINT_DURATION
            self.show = False

        def draw(self, display, scroll):
            if self.dur > 0:
                self.render(display, scroll)
