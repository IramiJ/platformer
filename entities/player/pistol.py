from entities.entity import simple_entity

class Pistol(simple_entity):
    def __init__(self, loc):
        super().__init__("assets/constants/pistol.png", loc)
        self.img.set_colorkey((0,0,0))
        self.flip = False
    