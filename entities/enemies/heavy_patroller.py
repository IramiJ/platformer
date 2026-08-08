import pygame

from .patroller import Patroller


class HeavyPatroller(Patroller):
    def __init__(self, x: float, y: float, width: int = 24, height: int = 24) -> None:
        super().__init__(x, y, width, height)
        self.max_hp = 6
        self.current_hp = 6
        self.true_velocity = 60

    def move(self, dt: float, tiles: list[pygame.Rect]) -> None:
        self.movement = [0, 0]
        if self.direction == "r":
            self.move_right()
        if self.direction == "l":
            self.move_left()
        """ actual movement of the enemy """
        self.move_with_tile_collisions(dt, tiles)

    def move_right(self) -> None:
        if self.rect.x >= self.spawn_point[0] + self.distance:
            self.direction = "l"
            self.flip = True
        else:
            self.movement[0] += self.true_velocity

    def move_left(self) -> None:
        if self.rect.x <= self.spawn_point[0] - self.distance:
            self.direction = "r"
            self.flip = False
        else:
            self.movement[0] -= self.true_velocity
