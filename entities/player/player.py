from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from world.level_loader import Level_loader
    from world.scrolling import Scroll

from entities.entity import entity
from entities.player.tail import Tail
from entities.player.sword import Sword
from entities.player.bow import Bow
from entities.animations import load_animation, ANIMATION_TICKS_PER_SECOND
from core.settings import REFERENCE_TICKS_PER_SECOND
from entities.spark import Spark
from world.collisions import move_collisions
import math
import pygame
import random


class Player(entity):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.spawn_point = [self.rect.x, self.rect.y]
        self.moving_left = False
        self.moving_right = False
        self.coin_amount = 1000
        self.y_momentum = 0
        self.velocity = 180
        self.jump_momentum = -600
        self.buffs = {}
        self.air_timer = 0
        self.double_coin_buff = False
        self.animation_database = {}
        self.scroll = [0, 0]
        self.movement = [0, 0]
        self.animation_frames = {}
        self.dashing = False
        self.dash_timer = 0
        self.dash_duration = 1/3
        self.dash_speed = 360
        self.max_dash_cd = 1.0
        self.dash_cooldown = 0
        self.max_hp = 5
        self.hp = 5
        self.dmg = 1
        self.animation_database["idle"] = load_animation(
            "assets/char/idle", [20, 20, 20], self
        )
        self.animation_database["run"] = load_animation(
            "assets/char/run", [4 for _ in range(12)], self
        )
        self.dmg_cd = 0
        self.cd_obj = entity(self.x, self.y + 15, 16, 16)
        self.cd_obj.animation_database["idle"] = load_animation(
            "assets/cooldown/idle", [4 for x in range(15)], self.cd_obj
        )
        self.tail = Tail("assets/tail/grey.png", [self.rect.x - 2, self.rect.y + 8])
        self.sword = Sword(self.rect.x, self.rect.y)
        self.bow = Bow(self.rect.x, self.rect.y)
        self.action = "idle"
        self.mode = "melee"
        self.respawn = False
        self.histstop_timer = 0

    def update(self, tile_rects: list[pygame.Rect], enemy_list, max_y: int, dt: float):
        self.update_movements(tile_rects, enemy_list, max_y, dt)
        self.update_frames(dt)
        self.bow.update(self, dt)
        self.sword.update(self, dt)

    def update_movements(self, tile_rects: list[pygame.Rect], enemy_list, max_y: int, dt: float) -> None:
        self.update_mode_properties()
        self.apply_buffs(dt)
        self.handle_movements(tile_rects, dt)
        self.bow.move_arrows(enemy_list, dt)
        self.die_through_falling(max_y)
        self.remove_buffs(["speed boost", "jump boost", "double coin"])
        self.manage_attack_cd(dt)

    def run_render_logic(self, display: pygame.Surface, scroll: Scroll) -> None:
        self.draw(display, scroll)
        self.draw_dash_cd(display, scroll)
        # self.draw_tail_points(display, scroll)

    def die_through_falling(self, max_y: int) -> None:
        if self.rect.y > max_y:
            self.set_respawn_location()

    def remove_buffs(self, buff_list):
        for buff in buff_list:
            if buff not in self.buffs:
                if buff == "speed boost":
                    self.velocity = 180
                elif buff == "jump boost":
                    self.jump_momentum = -600
                elif buff == "double coin":
                    self.double_coin_buff = False

    def apply_buffs(self, dt):
        c = self.buffs.copy()
        for buff in c:
            if self.buffs[buff] > 0:
                if buff == "speed boost":
                    self.velocity += 120
                    self.buffs[buff] = max(0.0, self.buffs[buff] - dt)
                elif buff == "jump boost":
                    self.jump_momentum = -900
                    self.buffs[buff] = max(0.0, self.buffs[buff] - dt)
                elif buff == "double coin":
                    self.double_coin_buff = True
                    self.buffs[buff] = max(0.0, self.buffs[buff] - dt)
            else:
                self.buffs.pop(buff)

    def update_frames(self, dt: float):
        animation = self.animation_database[self.action]
        self.frame = (
            self.frame + ANIMATION_TICKS_PER_SECOND * dt
        ) % len(animation)
        self.img_id = animation[math.floor(self.frame)]
        self.img = self.animation_frames[self.img_id]

    def draw(self, display: pygame.Surface, scroll: Scroll) -> None:
        """
        Hitbox for debugging purposes
        pygame.draw.rect(display, (255,0,0), pygame.Rect(self.rect.left - scroll.render_scroll[0], self.rect.top - scroll.render_scroll[1], 16, 16))
        """
        display.blit(
            pygame.transform.flip(self.img, self.flip, False),
            [
                self.rect.x - scroll.render_scroll[0],
                self.rect.y - scroll.render_scroll[1],
            ],
        )
        if self.mode == "melee":
            self.sword.draw(
                self.dashing,
                display,
                scroll,
                self.frame,
                self.action,
            )
        elif self.mode == "ranged":
            self.bow.draw(self, display, scroll)
        for arrow in self.bow.arrows:
            arrow.render(display, scroll.render_scroll)
        

    def dash(self) -> None:
        if not self.dashing and self.dash_cooldown <= 0:
            self.dashing = True
            self.dash_timer = self.dash_duration
            self.dash_cooldown = self.max_dash_cd

    def switch_mode(self) -> None:
        if self.mode == "melee":
            self.mode = "ranged"
        elif self.mode == "ranged" and not self.bow.reloading:
            self.mode = "melee"

    def update_mode_properties(self) -> None:
        if self.mode == "melee":
            self.velocity = 180
            self.dash_duration = 1/3
            self.dmg = 2
        elif self.mode == "ranged":
            self.velocity = 240
            self.dash_duration = 1/6
            self.dmg = 1

    def attack(self, enemy, logic_variables, sparks: list[Spark], dt: float) -> None:
        if self.dmg_cd <= 0 and self.dashing and self.mode == "melee":
            if self.rect.colliderect(enemy.rect):
                self.attack_on_hit(enemy, logic_variables, sparks)

                self.match_damage_cooldown()
                self.heal_on_stun(enemy, sparks)

    def attack_on_hit(self, enemy, logic_variables, sparks):
        enemy.take_dmg(self.dmg)
        self.activate_hitstop(logic_variables)
        sparks.append(
            Spark(
                [enemy.rect.x, enemy.rect.y],
                random.randint(0, 360),
                random.randint(3, 6),
                (255, 255, 255),
                2,
            )
        )

    def heal_on_stun(self, enemy, sparks: list[Spark]) -> None:
        if enemy.stunned:
            sparks.append(
                Spark(
                    [enemy.rect.x, enemy.rect.y],
                    random.randint(0, 360),
                    random.randint(3, 6),
                    (255, 255, 255),
                    2,
                )
            )
            self.heal(2)
        else:
            self.heal(1)

    def match_damage_cooldown(self) -> None:
        self.dmg_cd = self.dash_cooldown

    def manage_attack_cd(self, dt) -> None:
        if self.dmg_cd > 0:
            self.dmg_cd = max(0.0, self.dmg_cd - dt)

    def take_dmg(self, scroll) -> None:
        self.hp -= 1
        scroll.shake_timer = 1/6
        scroll.shake_strength = 3

    def set_respawn_location(self) -> None:
        self.rect.x = self.spawn_point[0]
        self.rect.y = self.spawn_point[1]

    def activate_hitstop(self, logic_variables) -> None:
        logic_variables.hitstop_timer = 1/20

    def heal(self, amount: int) -> None:
        if self.hp + amount < self.max_hp:
            self.hp += amount
        else:
            self.hp = self.max_hp

    def handle_movements(self, tile_rects: list[pygame.Rect], dt: float) -> None:
        self.movement = [0, 0]
        if self.dashing:
            self.handle_dash(dt)
        else:
            self.move_left()
            self.move_right()
            self.movement[1] += self.y_momentum
            # self.tail.loc[1] = self.rect.y + 8

        self.set_y_momentum(dt)

        self.set_dash(dt)

        self.determine_action()

        self.rect, collisions = move_collisions(
            self.rect, self.movement, tile_rects, dt
        )

        self.handle_y_collisions(collisions, dt)
        """
        Tail points
        self.tail.update_points(dt)
        self.update_tail_points(dt)
        """
    def update_tail_points(self, dt: float) -> None:
        for i in range(len(self.tail.points)):
            if self.tail.points[i].show:
                point = self.tail.points[i]
                point.dur -= (i + 1) * REFERENCE_TICKS_PER_SECOND * dt
                if point.dur <= 0:
                    point.dur = 2.0

    def draw_tail_points(self, display: pygame.Surface, scroll: Scroll) -> None:
        for i in range(len(self.tail.points)):
            if self.tail.points[i].show:
                self.tail.points[i].draw(display, scroll.render_scroll)

    def set_dash(self, dt: float) -> None:
        if self.dash_cooldown > 0:
            self.dash_cooldown = max(0.0, self.dash_cooldown - dt)

    def set_y_momentum(self, dt: float) -> None:
        self.y_momentum += 1440 * dt
        if self.y_momentum > 420.0:
            self.y_momentum = 420.0

    def determine_action(self) -> None:
        if self.movement[0] > 0:
            self.change_action("run")
            self.flip = False
        if self.movement[0] < 0:
            self.change_action("run")
            self.flip = True
        if self.movement[0] == 0:
            self.change_action("idle")

    def move_right(self) -> None:
        if self.moving_right:
            self.movement[0] += self.velocity
            for point in self.tail.points:
                point.show = True
            self.tail.loc[0] = self.rect.x - 1 + self.movement[0]
            self.tail.dir = "r"

    def move_left(self) -> None:
        if self.moving_left:
            self.movement[0] -= self.velocity
            self.tail.loc[0] = self.rect.x + 17 + self.movement[0]
            for point in self.tail.points:
                point.show = True
            self.tail.dir = "l"

    def handle_dash(self, dt: float) -> None:
        self.y_momentum = 0
        self.movement[0] = self.dash_speed * (-1 if self.flip else 1)
        self.dash_timer = max(0.0, self.dash_timer - dt)
        if self.dash_timer <= 0:
            self.dashing = False

    def handle_y_collisions(self, collisions: dict[str, bool], dt: float) -> None:
        if collisions["bottom"]:
            self.y_momentum = 0
            self.air_timer = 0
        else:
            self.air_timer += dt

        if collisions["top"]:
            self.y_momentum = 0

    def draw_dash_cd(self, display, scroll):
        if self.dash_cooldown <= 0:
            return

        animation = self.cd_obj.animation_database[self.cd_obj.action]

        progress = 1.0 - self.dash_cooldown / self.max_dash_cd

        frame = int(progress * len(animation) - 1)
        frame = max(0, min(frame, len(animation) - 1))

        img_id = animation[frame]
        img = self.cd_obj.animation_frames[img_id]

        display.blit(
            pygame.transform.flip(
                img,
                self.cd_obj.flip,
                False,
            ),
            [
                self.rect.x - scroll.render_scroll[0],
                self.rect.y - 30 - scroll.render_scroll[1],
            ],
        )
