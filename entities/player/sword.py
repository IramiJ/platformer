from entities.entity import entity
from entities.animations import load_animation
import random, pygame
from entities.particles import Particle

class Sword(entity):
    def __init__(self, x, y):
        super().__init__(x,y,21,7)
        self.img = pygame.image.load("assets/constants/curve_sword.png").convert()
        self.img.set_colorkey((0,0,0))
        self.particles = []
        self.flip = False
        self.particle_cd = 1
        self.load_slice()
        self.slice_frame = 0
        self.animation_database["idle"] = [self.img]
    def add_particles(self):
        if self.particle_cd == 0:
            for i in range(0, 4):
                p = Particle("assets/particles/sword_particle.png", [self.loc[0]+i, self.loc[1]], 120)
                p.y_velocity += i/100                
                if self.flip:                   
                    self.particles.append(p)                    
                else:
                    p.loc[0] = self.loc[0]+20-i
                    self.particles.append(p)
            self.particle_cd = 60
        else:
            self.particle_cd -= 1
        for particle in self.particles:
            particle.duration -= 1
    def load_slice(self):
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
    def draw_slice(self, display: pygame.Surface, scroll):
        if not self.flip:
            display.blit(pygame.transform.flip(self.slice_animation[self.slice_frame],self.flip,False), [self.loc[0]+10-scroll.render_scroll[0], self.loc[1]-scroll.render_scroll[1]-16])
        else:
            display.blit(pygame.transform.flip(self.slice_animation[self.slice_frame],self.flip,False), [self.loc[0]-self.slice_animation[self.slice_frame].get_width()+10-scroll.render_scroll[0], self.loc[1]-scroll.render_scroll[1]-16])
        if self.slice_frame < len(self.slice_animation)-1:
            self.slice_frame += 1
        else:
            self.slice_frame = 0

    def draw(self, player, display, scroll):
        self.flip = player.flip     
        if not player.flip:
            self.loc = [player.rect.right-6, player.rect.y+6]
        else:
            
            self.loc = [player.rect.left-self.img.get_width()+6, player.rect.y+6]
        if player.dashing:
            self.draw_slice(display, scroll)
        self.add_particles()
        display.blit(pygame.transform.flip(self.img, self.flip, False), [self.loc[0] - scroll.render_scroll[0], self.loc[1] - scroll.render_scroll[1]])
        for particle in self.particles:
            particle.render(display, scroll)
        

