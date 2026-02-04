from entities.entity import simple_entity
import random
from entities.particles import Particle

class Sword(simple_entity):
    def __init__(self, loc):
        super().__init__("assets/constants/sword.png", loc)
        self.img.set_colorkey((0,0,0))
        self.particles = []
        self.flip = False
        self.particle_cd = 1
    def add_particles(self):
        if self.particle_cd == 0:
            for i in range(0, self.img.get_width()):                
                if self.flip:
                    self.particles.append(Particle("assets/particles/sword_particle.png", [self.loc[0]+i, self.loc[1]], 120))
                else:
                    self.particles.append(Particle("assets/particles/sword_particle.png", [self.loc[0]+self.img.get_width()-i, self.loc[1]], 120))
            self.particle_cd = 60
        else:
            self.particle_cd -= 1
        for particle in self.particles:
            particle.duration -= 1
