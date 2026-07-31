import pygame
import math
from entities.entity import simple_entity


class Shooter_Bullet(simple_entity):
    def __init__(self, loc, player):
        super().__init__("assets/enemies/shooter/bullet.png", loc)
        self.start = self.loc.copy()
        self.base_img = self.img.copy()
        self.velocity = 120
        self.range = 200
        self.calc_angle(player)
        self.dmg_cd = 0
        self.alive = True

    def calc_angle(self, player):
        x = self.get_rect().x - player.rect.x
        y = self.get_rect().y - player.rect.y
        self.angle = math.atan2(y, x) + math.pi

    def transform_img(self):
        self.img = pygame.transform.rotate(self.base_img, math.degrees(self.angle))

    def move(self, entity, scroll, dt):
        self.loc[0] += math.cos(self.angle) * self.velocity * dt
        self.loc[1] += math.sin(self.angle) * self.velocity * dt
        if self.dmg_cd <= 0:
            self.dmg_entity(entity, scroll)
        self.check_alive()

    def check_alive(self):
        if (
            math.sqrt(
                (self.loc[0] - self.start[0]) ** 2 + (self.loc[1] - self.start[1]) ** 2
            )
            >= self.range
        ):
            self.alive = False

    def dmg_entity(self, entity, scroll):
        if self.collision_test(entity.rect):
            entity.take_dmg(scroll)
            self.dmg_cd = 1/60
