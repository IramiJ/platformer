from entities.entity import entity
from entities.animations import load_animation
import random, pygame, math
from entities.particles import Particle

class Sword(entity):
    def __init__(self, x, y):
        super().__init__(x,y,21,7)
        self.img = pygame.image.load("assets/constants/curve_sword.png").convert()
        self.img.set_colorkey((0,0,0))
        self.particles = []
        self.flip = False
        self.particle_cd = 1
        self.load_slice_animation()
        self.slice_frame = 0
        self.animation_database["idle"] = [self.img]
    def add_particles(self):
        if self.particle_cd == 0:
            self.spawn_particles()
        else:
            self.particle_cd -= 1

        self.decrease_particles_duration()
    def spawn_particles(self):
        for i in range(0, 4):
            p = Particle("assets/particles/sword_particle.png", [self.loc[0]+i, self.loc[1]], 120)
            p.y_velocity += i/100                
            if self.flip:                   
                self.particles.append(p)                    
            else:
                p.loc[0] = self.loc[0]+20-i
                self.particles.append(p)
        self.particle_cd = 60

    def decrease_particles_duration(self):
        for particle in self.particles:
            particle.duration -= 1

    def load_slice_animation(self):
        path = "assets/weapons/sword/slice"
        dur = [1 for x in range(11)]
        animation_name = path.split('/')[-1]
        self.slice_animation = []
        n = 0
        for frame in dur:
            animation_frame_id = animation_name + str(n)
            img_loc = path + '/' + animation_frame_id + '.png'
            animation_image = pygame.image.load(img_loc).convert_alpha()
            animation_image.set_colorkey((0,0,0))
            for i in range(frame):
                self.slice_animation.append(animation_image)
            n +=1 

    def draw_slice(self, display: pygame.Surface, scroll, dt):
        if not self.flip:
            display.blit(pygame.transform.flip(self.slice_animation[math.floor(self.slice_frame)],self.flip,False), [self.loc[0]+10-scroll.render_scroll[0], self.loc[1]-scroll.render_scroll[1]-16])
        else:
            display.blit(pygame.transform.flip(self.slice_animation[math.floor(self.slice_frame)],self.flip,False), [self.loc[0]-self.slice_animation[math.floor(self.slice_frame)].get_width()+10-scroll.render_scroll[0], self.loc[1]-scroll.render_scroll[1]-16])
        self.update_slice_frame(dt)

    def update_slice_frame(self, dt):
        self.slice_frame += dt    
        if self.slice_frame >= len(self.slice_animation):
            self.slice_frame = 0

    def draw(self, player_flip, player_dash_state, player_rect, display, scroll, dt):
        self.set_flip(player_flip)
        self.update_location(player_flip, player_rect)

        if player_dash_state:
            self.draw_slice(display, scroll, dt)

        self.add_particles()
        display.blit(pygame.transform.flip(self.img, self.flip, False), [self.loc[0] - scroll.render_scroll[0], self.loc[1] - scroll.render_scroll[1]])
        self.draw_particles(display, scroll)
        
    def set_flip(self, flip):
        self.flip = flip
    
    def update_location(self, player_flip, player_rect):
        if not player_flip:
            self.loc = [player_rect.right-6, player_rect.y+6]
        else:
            self.loc = [player_rect.left-self.img.get_width()+6, player_rect.y+6]
    
    def draw_particles(self, display, scroll):
        for particle in self.particles:
            particle.render(display, scroll)
