from entities.entity import simple_entity
from core.settings import Settings
from math import sin, pi
class Tail(simple_entity):
    def __init__(self, loc, img):
        super().__init__(loc, img)
        self.dur = 2* Settings.fps
    def draw(self, display, scroll):
        if self.dur > 0: 
            self.render(display, scroll)
            self.dur -= 1
            self.loc[1] += round(sin((self.dur / Settings.fps)*pi)*4)
