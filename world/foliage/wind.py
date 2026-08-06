import random

from core.settings import REFERENCE_TICKS_PER_SECOND

WIND_SIMULATION_STEP = 1.0 / REFERENCE_TICKS_PER_SECOND
WIND_BLEND_PER_REFERENCE_TICK = 0.05


class Wind:
    def __init__(self):
        self.current = 0.0
        self.target = 0.0
        self.timer = 0.0
        self.gust_strength = 0.0
        self.gust_time = 0.0
        self.winding = False
        self.leaf_spawn_rate = 5

    def update(self, dt):
        self.timer += dt
        while self.timer + 1e-12 >= WIND_SIMULATION_STEP:
            self.update_reference_step(WIND_SIMULATION_STEP)
            self.timer -= WIND_SIMULATION_STEP

    def update_reference_step(self, dt):
        if self.winding:
            self.wind_up()
            self.winding = False
            self.leaf_spawn_rate = 2
        else:
            self.leaf_spawn_rate = 5
        if self.gust_time > 0:
            fade = max(0, self.gust_time)
            self.target = self.gust_strength * min(1, fade * 2)
            self.gust_time -= dt
        else:
            self.target = random.uniform(-0.5, 0.2)

        self.current += (self.target - self.current) * WIND_BLEND_PER_REFERENCE_TICK

    def wind_up(self):
        self.gust_strength = random.uniform(-6.0, -3.0)
        self.gust_time = random.uniform(0.8, 2.0)
