from entities.entity import entity
from entities.player.tail import Tail
from entities.player.sword import Sword
from entities.player.pistol import Pistol
from entities.animations import load_animation
from entities.spark import Spark
from world.collisions import move_collisions
import math, pygame, random

class Player(entity):
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height)
        self.spawn_point = [self.rect.x, self.rect.y]
        self.moving_left = False
        self.moving_right = False
        self.coin_amount = 1000
        self.y_momentum = 0
        self.velocity = 3
        self.jump_momentum = -10
        self.buffs = {}
        self.air_timer = 0
        self.double_coin_buff = False
        self.animation_database = {}
        self.scroll = [0,0]
        self.movement = [0, 0]
        self.animation_frames = {}
        self.dashing = False
        self.dash_timer = 0
        self.dash_duration = 10
        self.dash_speed = 6
        self.max_dash_cd = 60
        self.dash_cooldown = 0
        self.max_hp = 5
        self.hp = 5
        self.dmg = 1
        self.animation_database['idle'] = load_animation('assets/char/idle', [20,20,20], self)
        self.animation_database['run'] = load_animation('assets/char/run', [4 for _ in range(12)], self)
        self.dmg_cd = 0
        self.cd_obj = entity(self.x, self.y + 15, 16, 16)
        self.cd_obj.animation_database['idle'] = load_animation('assets/cooldown/idle', [4 for x in range(15)], self.cd_obj)
        self.tail = Tail('assets/tail/grey.png',[self.rect.x-2, self.rect.y+8])
        self.sword = Sword(self.rect.x, self.rect.y)
        self.pistol = Pistol(self.rect.x, self.rect.y)
        self.action = "idle"
        self.mode = "melee"
        self.respawn = False
        self.histstop_timer = 0

    def update_movements(self, tile_rects, enemy_list, max_y,  dt):
        self.handle_movements(tile_rects, dt)
        self.pistol.shoot(enemy_list, dt)
        self.die_through_falling(max_y) # self.level.data["max_y"]
        self.remove_buffs(["speed boost", "jump boost", "double coin"])
        self.update_mode_properties()
        self.apply_buffs()
        self.manage_attack_cd(dt)
    
    def run_render_logic(self, display, scroll, dt):
        self.update_frames(dt)
        self.draw(display, scroll, dt)
        self.draw_dash_cd(display, scroll)
        # self.draw_tail_points(display, scroll)
    
    def die_through_falling(self, max_y):
        if self.rect.y > max_y:
            self.set_respawn_location()
    
    def remove_buffs(self, buff_list):
        for buff in buff_list:
            if buff not in self.buffs:
                if buff == "speed boost":
                    self.velocity = 3
                elif buff == "jump boost":
                    self.jump_momentum = -10
                elif buff == "double coin":
                    self.double_coin_buff = False

    def apply_buffs(self):
        c = self.buffs.copy()
        for buff in c:
            if self.buffs[buff] > 0:
                if buff == 'speed boost':
                    self.velocity += 2
                    self.buffs[buff] -= 1
                elif buff == 'jump boost':
                    self.jump_momentum = -15
                    self.buffs[buff] -= 1
                elif buff == 'double coin':
                    self.double_coin_buff = True
                    self.buffs[buff] -= 1
            else:
                self.buffs.pop(buff)
            
    def update_frames(self, dt):
        self.frame += dt
        if self.frame >= len(self.animation_database[self.action]):
            self.frame = 0
        self.img_id = self.animation_database[self.action][math.floor(self.frame)]
        self.img = self.animation_frames[self.img_id]


    def draw(self, display, scroll, dt):
#        pygame.draw.rect(display, (255,0,0), pygame.Rect(self.rect.left - scroll.render_scroll[0], self.rect.top - scroll.render_scroll[1], 16, 16))
        display.blit(pygame.transform.flip(self.img,self.flip,False), [self.rect.x-scroll.render_scroll[0], self.rect.y-scroll.render_scroll[1]])
        if self.mode == "melee":
            self.sword.draw(self.flip, self.dashing, self.rect, display, scroll, self.frame, self.action)
        elif self.mode == "ranged":
            self.pistol.draw(self, display, scroll)
        for bullet in self.pistol.bullets:
            bullet.render(display, scroll.render_scroll)
        self.sword.particles = [p for p in self.sword.particles if p.duration > 0]
        

    
    

    def dash(self):
        if not self.dashing and self.dash_cooldown <= 0:   
            self.dashing = True
            self.dash_timer = self.dash_duration
            self.dash_cooldown = self.max_dash_cd   

    def switch_mode(self):
        if self.mode == "melee":
            self.mode   = "ranged"
        elif self.mode == "ranged" and not self.pistol.reloading:
            self.mode = "melee"

    def update_mode_properties(self):
        if self.mode == "melee":
            self.velocity = 3
            self.dash_duration = 20
            self.dmg = 2
        elif self.mode == "ranged":
            self.velocity = 4
            self.dash_duration = 10
            self.dmg = 1


    def attack(self, enemy, logic_variables, sparks, dt):
        if self.dmg_cd <= 0 and self.dashing and self.mode == "melee":
            if self.rect.colliderect(enemy.rect):
                self.attack_on_hit(enemy, logic_variables, sparks)

                self.match_damage_cooldown()
                self.heal_on_stun(enemy, sparks)

    def attack_on_hit(self, enemy, logic_variables, sparks):
        enemy.take_dmg(self.dmg)
        self.activate_hitstop(logic_variables)
        sparks.append(Spark([enemy.rect.x, enemy.rect.y], random.randint(0, 360), random.randint(3, 6), (255,255,255), 2))

    def heal_on_stun(self, enemy, sparks):
        if enemy.stunned:
            sparks.append(Spark([enemy.rect.x, enemy.rect.y], random.randint(0, 360), random.randint(3, 6), (255,255,255), 2))
            self.heal(2)
        else:
            self.heal(1)

    def match_damage_cooldown(self):
        self.dmg_cd = self.dash_cooldown

    def manage_attack_cd(self, dt):
        if self.dmg_cd > 0:
            self.dmg_cd -= dt

    def take_dmg(self, scroll):
        self.hp -= 1
        scroll.shake_timer = 10
        scroll.shake_strength = 3
    
    def set_respawn_location(self):
        self.rect.x = self.spawn_point[0]
        self.rect.y = self.spawn_point[1]
    
    def revive(self, level):
        if self.respawn:
            self.hp = self.max_hp
            level.id = 1
            self.set_respawn_location()
            self.respawn = False
    
    def activate_hitstop(self, logic_variables):
        logic_variables.hitstop_timer = 3
    
    def heal(self, amount):
        if self.hp + amount < self.max_hp:
            self.hp += amount
        else:
            self.hp = self.max_hp
    
    def handle_movements(self, tile_rects, dt):
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

        self.rect, collisions = move_collisions(self.rect, self.movement, tile_rects, dt)

        self.handle_y_collisions(collisions, dt)

        # self.tail.update_points()
        # self.update_tail_points()

    def update_tail_points(self):
        for i in range(len(self.tail.points)):
            if self.tail.points[i].show:
                self.tail.points[i].dur -= i    
    
    def draw_tail_points(self, display, scroll):
        for i in range(len(self.tail.points)):
            if self.tail.points[i].show:
                self.tail.points[i].draw(display, scroll.render_scroll)

    def set_dash(self, dt):
        if self.dash_cooldown > 0:
            self.dash_cooldown -= dt
            

    def set_y_momentum(self, dt):
        self.y_momentum += 0.4 * dt
        if self.y_momentum > 7:
            self.y_momentum = 7

    def determine_action(self):
        if self.movement[0] > 0:
            self.change_action('run')
            self.flip = False
        if self.movement[0] < 0:
            self.change_action('run')
            self.flip = True
        if self.movement[0] == 0:
            self.change_action('idle')

    def move_right(self):
        if self.moving_right:
            self.movement[0] += self.velocity
            for point in self.tail.points:
                point.show = True
            self.tail.loc[0] = self.rect.x - 1 + self.movement[0]
            self.tail.dir = 'r'

    def move_left(self):
        if self.moving_left:
            self.movement[0] -= self.velocity
            self.tail.loc[0] = self.rect.x + 17 + self.movement[0]
            for point in self.tail.points:
                point.show = True
            self.tail.dir = 'l'

    def handle_dash(self, dt):
        self.y_momentum = 0
        self.movement[0] =  self.dash_speed * (-1 if self.flip else 1)
        self.dash_timer -= 1 * dt
        if self.dash_timer <= 0:
            self.dashing = False    
        
    def handle_y_collisions(self, collisions, dt):
        if collisions['bottom']:
            self.y_momentum = 0
            self.air_timer = 0
        else:
            self.air_timer += dt

        if collisions['top']:
            self.y_momentum = 0    

    def draw_dash_cd(self, display, scroll):
        if self.dash_cooldown > 0:
            self.cd_obj.frame = self.max_dash_cd -(self.dash_cooldown)
            self.cd_obj.img_id = self.cd_obj.animation_database[self.cd_obj.action][math.floor(self.cd_obj.frame)]
            self.cd_obj.img = self.cd_obj.animation_frames[self.cd_obj.img_id]
            display.blit(pygame.transform.flip(self.cd_obj.img,self.cd_obj.flip,False), [self.rect.x-scroll.render_scroll[0], self.rect.y-30-scroll.render_scroll[1]])           
            if self.cd_obj.frame >= len(self.cd_obj.animation_database[self.cd_obj.action]):
                self.cd_obj.frame = 0
        
    