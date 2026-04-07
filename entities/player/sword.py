from entities.entity import entity
from entities.animations import load_animation
import random, pygame, math
from entities.particles import Particle

class Sword(entity):
    def __init__(self, x, y):
        super().__init__(x,y,21,7)
        self.img = pygame.image.load("assets/weapons/broken_sword.png").convert()
        self.img.set_colorkey((0,0,0))
        self.particles = []
        self.flip = False
        self.particle_cd = 1
        self.load_slice_animation()
        self.slice_frame = 0
        self.animation_database["idle"] = [self.img]
        # Keeps track of the player hand
        self.offsets = {"run": [(6, 16), (5, 16), (3, 16), (2, 15), (5, 17), (7, 15), (6, 16), (8, 16), (11, 14), (16, 15), (12, 16), (9, 16)], 
                        "idle": [(6, 16), (6, 16), (6,17)]} 
        self.angles = {"run": [0, -10, -25, -45, -25, 0, 0, 10, 25, 45, 35, 25],
                       "idle": [0, 0, 0]}
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
            display.blit(pygame.transform.flip(self.slice_animation[math.floor(self.slice_frame)],self.flip,False), [self.loc[0]-self.slice_animation[math.floor(self.slice_frame)].get_width()-scroll.render_scroll[0], self.loc[1]-scroll.render_scroll[1]-16])
        self.update_slice_frame(dt)

    def update_slice_frame(self, dt):
        self.slice_frame += dt    
        if self.slice_frame >= len(self.slice_animation):
            self.slice_frame = 0

    def draw(self, player_flip, player_dash_state, player_rect, display, scroll, player_frame, player_action, dt):
        self.set_flip(player_flip)
        self.update_location(player_flip, player_rect, player_frame, player_action)
        frame = self.get_animation_frame(player_frame, player_action)
        angle = self.angles[player_action][frame]
        
        if player_dash_state:
            self.draw_slice(display, scroll, dt)
        '''
        self.add_particles()
        self.draw_particles(display, scroll)
        '''
        # display.blit(pygame.transform.flip(self.img, self.flip, False), [self.loc[0] - scroll.render_scroll[0], self.loc[1] - scroll.render_scroll[1]])
        self.draw_rotated(display, scroll, angle)
        
        
    def set_flip(self, flip):
        self.flip = flip
    
    def update_location(self, player_flip, player_rect, player_frame, player_action):
        frame = self.get_animation_frame(player_frame, player_action)
        if player_flip:
            self.loc = [player_rect.left-self.img.get_width()+(24-self.offsets[player_action][frame][0]), player_rect.y+self.offsets[player_action][frame][1]-2]      
        else:
            self.loc = [player_rect.right-(24-self.offsets[player_action][frame][0]), player_rect.y+self.offsets[player_action][frame][1]-2]
    
    def draw_particles(self, display, scroll):
        for particle in self.particles:
            particle.render(display, scroll)
    
    def get_animation_frame(self, player_frame, player_action):
        if player_action == "run":
            return math.floor(player_frame / 4)
        elif player_action == "idle":
            return math.floor(player_frame / 20)
        return 0
    def draw_rotated(self, display, scroll, angle):
        img = pygame.transform.flip(self.img, self.flip, False)

        if self.flip:
            angle = -angle

        original_rect = img.get_rect(topleft=self.loc)

        if self.flip:
            hilt_offset = pygame.Vector2(img.get_width(), img.get_height() / 2)
        else:
            hilt_offset = pygame.Vector2(0, img.get_height() / 2)

        hilt_pos = pygame.Vector2(original_rect.topleft) + hilt_offset

        offset_from_center_to_hilt = hilt_pos - pygame.Vector2(original_rect.center)

        rotated_img = pygame.transform.rotate(img, angle)
        rotated_offset = offset_from_center_to_hilt.rotate(-angle)

        rotated_center = hilt_pos - rotated_offset
        rotated_rect = rotated_img.get_rect(center=rotated_center)

        display.blit(rotated_img, [rotated_rect.x - scroll.render_scroll[0],rotated_rect.y - scroll.render_scroll[1]])
