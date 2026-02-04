from entities.entity import simple_entity

class Sword(simple_entity):
    def __init__(self, loc):
        super().__init__("assets/constants/sword.png", loc)
        self.img.set_colorkey((0,0,0))