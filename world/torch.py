import random, pygame
from entities.particles import simple_particle
class Torch:
    def __init__(self, loc):
        self.loc = loc
        self.particles = []
        self.img = pygame.image.load("assets/constants/torch.png").convert()
        self.img.set_colorkey((0,0,0))
        self.particle_spawn = self.loc.copy()
        self.particle_spawn[0]+= 4
    def add_particles(self):
        if random.randint(0, 50) == 50:
            self.particles.append(simple_particle(self.particle_spawn.copy(), [random.randint(-10, 10)/100, 0], random.randint(14, 24)/10))
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