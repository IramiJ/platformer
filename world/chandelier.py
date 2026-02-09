import random, pygame
from entities.particles import simple_particle
class Chandelier:
    def __init__(self, loc):
        self.loc = loc
        self.particles = []
        self.img = pygame.image.load("assets/constants/chandelier.png").convert()
        self.img.set_colorkey((0,0,0))
        self.particle_spawns = [self.loc.copy() for x in range (3)]
        self.particle_spawns[0][0] += 4
        self.particle_spawns [0][1] += 4
        self.particle_spawns[1][0] += 8
        self.particle_spawns [1][1] += 4
        self.particle_spawns[2][0] += 12
        self.particle_spawns [2][1] += 4
    def add_particles(self):
        for spawn in self.particle_spawns:
            if random.randint(1, 20) == 20:
                self.particles.append(simple_particle(spawn.copy(), [random.randint(-10, 10)/100, 0], random.randint(14, 24)/10))
    def draw_particles(self, display, scroll):        
        for particle in self.particles:
            particle.loc[0] += particle.velocities[0]
            particle.loc[1] += particle.velocities[1]
            particle.velocities[1] += 0.02
            particle.radius -= 0.01
            pygame.draw.circle(display, (255,255,255), [particle.loc[0]-scroll.render_scroll[0], particle.loc[1]-scroll.render_scroll[1]], particle.radius)
            if particle.radius <= 0:
                self.particles.remove(particle)
        self.add_particles()
    def draw(self, display: pygame.Surface, scroll):
        display.blit(self.img, [self.loc[0]-scroll.render_scroll[0], self.loc[1]-scroll.render_scroll[1]])
        self.draw_particles(display, scroll)