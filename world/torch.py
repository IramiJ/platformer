import random, pygame
from entities.particles import simple_particle
class Torch:
    def __init__(self, loc):
        self.loc = loc
        self.particles = []
        self.img = pygame.image.load("assets/constants/torch.png").convert()
        self.img.set_colorkey((0,0,0))
    def add_particles(self):
        loc = self.loc.copy()
        loc[0] += self.img.get_width() // 2
        self.particles.append(simple_particle(loc, [random.randint(0,20)/10-1, -1], random.randint(14, 24)/10))
    def draw_particles(self, display, scroll):        
        for particle in self.particles:
            particle.loc[0] += particle.velocities[0]
            particle.loc[1] += particle.velocities[1]
            particle.velocities[1] += 0.15
            particle.radius -= 0.05
            pygame.draw.circle(display, (255,255,255), [particle.loc[0]-scroll.render_scroll[0], particle.loc[1]-scroll.render_scroll[1]], particle.radius)
            if particle.radius <= 0:
                self.particles.remove(particle)
        self.add_particles()
    def draw(self, display: pygame.Surface, scroll):
        display.blit(self.img, [self.loc[0]-scroll.render_scroll[0], self.loc[1]-scroll.render_scroll[1]])
        self.draw_particles(display, scroll)