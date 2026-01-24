from entities.entity import simple_entity
from core.settings import Settings
import math, random
class Tail():
    def __init__(self,  img, loc):
        self.img = img
        self.loc = loc
        self.points = []
        for i in range(10):
            self.points.append(self.Point(self.loc[0]-i, self.loc[1], 'assets/tail/grey.png'))
    
    def update_points(self):
        for i in range(len(self.points)):
            self.points[i].loc[0] = self.loc[0]-i
            self.points[i].loc[1] = self.loc[1] + math.sin(math.pi*i/2)

    class Point(simple_entity):
        def __init__(self, x, y, img):
            super().__init__(img, [x, y])
            self.dur = 2* Settings.fps
            self.show = False
        def draw(self, display, scroll):
            if self.dur > 0:
                self.render(display, scroll)
                self.dur -= 1
                self.loc[1] += round(math.sin((self.dur/Settings.fps)*4*math.pi))
            else:
                self.dur = 2*Settings.fps
            print(self.dur)
        
