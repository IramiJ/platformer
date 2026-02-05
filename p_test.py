import sys, pygame, random

clock = pygame.time.Clock()
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((500, 500), 0,32)

particles = []

while True:
    screen.fill((0,0,0))

    particles.append([[250,250], [random.randint(0, 20)/10 - 1, -2], random.randint(4, 6)])
    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[1][1] += 0.1
        particle[2] -= 0.1
        pygame.draw.circle(screen, (255,255,255), particle[0], particle[2])
    print(particles)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    clock.tick(60)
    pygame.display.update()