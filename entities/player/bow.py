import pygame, math
from entities.entity import simple_entity, entity
from entities.animations import load_animation


class Bow: # TODO: rewrite this to a bow class
    def __init__(self, x, y):
        self.offsets = {"run": [(6, 16), (5, 16), (3, 16), (2, 15), (5, 17), (7, 15), (6, 16), (8, 16), (11, 14), (16, 15), (12, 16), (9, 16)], 
                        "idle": [(6, 16), (6, 16), (6,17)]} 
        self.angles = {"run": [0, -10, -25, -45, -25, 0, 0, 10, 25, 45, 35, 25],
                       "idle": [0, 0, 0]}
        self.loc = [x, y]
        self.img = pygame.image.load("assets/weapons/bow.png").convert()
        self.img.set_colorkey((0,0,0))
        self.arrows = []
        self.flip = False
        self.reloading = False
        self.add_ammo = False
        self.max_shoot_cd = 30
        self.shoot_cd = 1
        self.ammo = 5
        self.ammo_img = pygame.image.load("assets/weapons/cd_pistol.png").convert()
        self.ammo_img.set_colorkey((0,0,0))
        self.reload_cd = 0

    def draw(self, player, display, scroll):
        self.update_cds()
        
        self.set_flip(player)
        self.update_location(player.flip, player.rect, player.frame, player.action)
        frame = self.get_animation_frame(player.frame, player.action)
        angle = self.angles[player.action][frame] 
        self.draw_rotated(display, scroll, angle)

    def set_flip(self, player):
        self.flip = player.flip
    
    def update_location(self, player_flip, player_rect, player_frame, player_action):
        frame = self.get_animation_frame(player_frame, player_action)
        if player_flip:
            self.loc = [player_rect.left-(self.img.get_width())//2+(24-self.offsets[player_action][frame][0]), player_rect.y+self.offsets[player_action][frame][1]-self.img.get_height()]      
        else:
            self.loc = [player_rect.right-(24-self.offsets[player_action][frame][0])-(self.img.get_width())//2, player_rect.y+self.offsets[player_action][frame][1]-self.img.get_height()]

    def get_animation_frame(self, player_frame, player_action):
        if player_action == "run":
            return math.floor(player_frame / 4)
        elif player_action == "idle":
            return math.floor(player_frame / 20)
        return 0
    
    def shoot(self, enemy_list, dt):
        for arrow in self.arrows:
            arrow.move(enemy_list, self.arrows, dt)
        
    
    def update_cds(self):
        if self.shoot_cd > 0:
            self.shoot_cd -= 1
        if self.reload_cd > 0:
            self.reload_cd -= 1
            if self.reload_cd == 0:
                self.reloading = False
                self.add_ammo = True
        if self.add_ammo:
            self.ammo = 5
            self.add_ammo = False
        if self.ammo <= 0 and not self.reloading:
            self.reload()

    def add_arrow(self):
        if self.reload_cd == 0:
            if self.shoot_cd <= 0:
                b_loc = self.loc.copy()
                flip = bool(self.flip)
                self.arrows.append(Arrow(b_loc, flip))
                self.shoot_cd = self.max_shoot_cd
                self.ammo -= 1
        

    def reload(self):
        if not self.reloading:
            self.reload_cd = 120
            self.reloading = True

    # TODO: make a function which angles the bow depending on the location
    def draw_rotated(self, display, scroll, angle):
        img = pygame.transform.flip(self.img, self.flip, False)

        if self.flip:
            angle = -angle

        original_rect = img.get_rect(topleft=self.loc)

        handle_offset = pygame.Vector2(img.get_width()/2, 0)

        handle_pos = pygame.Vector2(original_rect.topleft) + handle_offset

        offset_from_center_to_hilt = handle_pos - pygame.Vector2(original_rect.center)

        rotated_img = pygame.transform.rotate(img, angle)
        rotated_offset = offset_from_center_to_hilt.rotate(-angle)

        rotated_center = handle_pos - rotated_offset
        rotated_rect = rotated_img.get_rect(center=rotated_center)

        display.blit(rotated_img, [rotated_rect.x - scroll.render_scroll[0],rotated_rect.y - scroll.render_scroll[1]])    

class Arrow(simple_entity):
        def __init__(self, loc, flip):
            super().__init__('assets/weapons/arrow.png',  loc)
            self.start = self.loc.copy()
            self.base_img = self.img.copy()
            self.velocity = 5
            self.range = 200
            self.dmg_cd = 0
            self.flip = flip
        def move(self, enemy_list, bullet_list, dt):
            self.dmg_entity(enemy_list)
            if not self.flip:
                self.loc[0] += self.velocity * dt
            else:
                self.loc[0] -= self.velocity * dt          
            self.remove(bullet_list)
            
        def remove(self, bullet_list):
            if math.sqrt((self.loc[0] - self.start[0])**2 + (self.loc[1] - self.start[1])**2) >= self.range:
                bullet_list.remove(self)

        def dmg_entity(self, enemies):
            
            if self.dmg_cd == 0:
                for enemy in enemies:
                    if self.collision_test(enemy.rect):
                        enemy.take_dmg(1)
                        enemy.stun()
                        self.dmg_cd = 1

