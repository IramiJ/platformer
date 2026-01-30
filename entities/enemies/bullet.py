import pygame, math
from entities.entity import simple_entity

class Bullet(simple_entity):
        def __init__(self, loc, player):
            super().__init__('assets/enemies/shooter/bullet.png',  loc)
            self.start = self.loc.copy()
            self.base_img = self.img.copy()
            self.velocity = 2
            self.range = 200
            self.calc_angle(player)
            self.dmg_cd = 0
        def calc_angle(self, player):
            x = (self.get_rect().x-player.rect.x)
            y = (self.get_rect().y-player.rect.y)
            self.angle =  math.atan2(y, x) + math.pi
        def transform_img(self):
            self.img = pygame.transform.rotate(self.base_img, math.degrees(self.angle))
        def move(self, player, display, bullet_list):
            self.render(display, player.scroll)
            self.loc[0] += math.cos(self.angle) * self.velocity
            self.loc[1] += math.sin(self.angle) * self.velocity
            if self.dmg_cd == 0:
                self.dmg_player(player)
            self.remove(bullet_list)
        def remove(self, bullet_list):
             if math.sqrt((self.loc[0] - self.start[0])**2 + (self.loc[1] - self.start[1])**2) >= self.range:
                  bullet_list.remove(self)

        def dmg_player(self, player):
            if self.collision_test(player.rect):
                player.hp -= 1
                self.dmg_cd = 1