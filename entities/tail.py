from entities.entity import simple_entity
from core.settings import Settings
import math, random
class Tail(simple_entity):
    def __init__(self, loc, img):
        super().__init__(loc, img)
        self.dur = 2* Settings.fps
        self.show = False
    def draw(self, display, scroll):
        if self.dur > 0: 
            self.render(display, scroll)
            self.dur -= 1
            self.loc[1] += round(math.sin((self.dur/Settings.fps)*4*math.pi))
            print(self.loc, self.dur)
        else:
            self.dur = 2*Settings.fps
