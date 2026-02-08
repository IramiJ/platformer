import pygame
from entities.entity import entity
from entities.animations import load_animation
from ui.Font_renderer import Font

class Ammo():
    def __init__(self):
        self.small_font = Font('assets/fonts/small_font.png')
        self.cd_obj = entity(300, 15, 16, 16)
        self.cd_obj.animation_database['idle'] = load_animation('assets/cooldown/idle', [8 for x in range(15)], self.cd_obj)
        self.pistol_img = pygame.image.load("assets/constants/cd_pistol.png").convert()
        self.pistol_img.set_colorkey((0,0,0))
    def render_ammo(self, display, player):
        self.render_pistol(display)
        if player.pistol.ammo > 0:
            self.render_ammo_amount(display, player)
        else:
            self.dash_cd(display)

    def dash_cd(self, display):
        self.cd_obj.img_id = self.cd_obj.animation_database[self.cd_obj.action][self.cd_obj.frame]
        self.cd_obj.img = self.cd_obj.animation_frames[self.cd_obj.img_id]
        display.blit(self.cd_obj.img,  (self.cd_obj.x, self.cd_obj.y))
        self.cd_obj.frame += 1
        if self.cd_obj.frame >= len(self.cd_obj.animation_database[self.cd_obj.action]):
            self.cd_obj.frame = 0    

    def render_ammo_amount(self, display, player):
        self.small_font.render(display, str(player.pistol.ammo), (320-10, 15))

    def render_pistol(self, display):
        display.blit(self.pistol_img, [320-self.pistol_img.get_width()-20, 15])
