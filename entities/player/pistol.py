import pygame, math
from entities.entity import simple_entity, entity
from entities.animations import load_animation


class Pistol:
    def __init__(self, x, y):
        self.loc = [x, y]
        self.img = pygame.image.load("assets/constants/pistol.png").convert()
        self.img.set_colorkey((0,0,0))
        self.bullets = []
        self.flip = False
        self.reloading = False
        self.add_ammo = False
        self.shoot_cd = 60
        self.ammo = 5
        self.ammo_img = pygame.image.load("assets/constants/cd_pistol.png").convert()
        self.ammo_img.set_colorkey((0,0,0))
        self.reload_cd = 0

    def draw(self, player, display, scroll):
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
        
        self.flip = player.flip
        sign = -1 if player.flip else 1
        if sign == 1:
            self.loc = [player.rect.right-6, player.rect.y+6]
        else:
            self.loc = [player.rect.left-self.img.get_width()+6, player.rect.y+6]
        display.blit(pygame.transform.flip(self.img, player.flip, False), [self.loc[0] - scroll.render_scroll[0], self.loc[1] - scroll.render_scroll[1]])
        for bullet in self.bullets:
            bullet.render(display, scroll.render_scroll)
        print(self.ammo)
    def shoot(self, enemy_list):
        for bullet in self.bullets:
            bullet.move(enemy_list, self.bullets)
            

    def add_bullet(self):
        if self.reload_cd == 0:
            if self.shoot_cd <= 0:
                b_loc = self.loc.copy()
                flip = bool(self.flip)
                self.bullets.append(Bullet(b_loc, flip))
                self.shoot_cd = 60
                self.ammo -= 1
        

    def reload(self):
        self.reload_cd = 120
        self.reloading = True


class Bullet(simple_entity):
        def __init__(self, loc, flip):
            super().__init__('assets/constants/pistol_bullet.png',  loc)
            self.start = self.loc.copy()
            self.base_img = self.img.copy()
            self.velocity = 5
            self.range = 200
            self.dmg_cd = 0
            self.flip = flip
        def move(self, enemy_list, bullet_list):
            self.dmg_entity(enemy_list)
            if not self.flip:
                self.loc[0] += self.velocity
            else:
                self.loc[0] -= self.velocity           
            self.remove(bullet_list)
            
        def remove(self, bullet_list):
             if math.sqrt((self.loc[0] - self.start[0])**2 + (self.loc[1] - self.start[1])**2) >= self.range:
                  bullet_list.remove(self)

        def dmg_entity(self, enemies):
            if self.dmg_cd == 0:
                for enemy in enemies:
                    if self.collision_test(enemy.rect):
                        enemy.take_dmg()
                        self.dmg_cd = 1

