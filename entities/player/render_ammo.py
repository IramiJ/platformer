import pygame
from entities.entity import entity
from entities.animations import load_animation
from ui.Font_renderer import Font
from core.paths import require_asset_file, require_asset_dir

class Ammo:
    def __init__(self):
        self.small_font = Font(require_asset_file("fonts/small_font.png"))
        self.pistol_img = pygame.image.load(require_asset_file("weapons/cd_pistol.png")).convert()
        self.pistol_img.set_colorkey((0, 0, 0))
        self.amount_padding = self.pistol_img.get_width() + 5
        self.cd_obj = entity(self.amount_padding, 9, 16, 16)
        self.cd_obj.animation_database["idle"] = load_animation(
            require_asset_dir("cooldown/idle"), [8 for x in range(15)], self.cd_obj
        )

    def render_ammo(self, display, player):
        self.render_pistol(display)
        if not player.bow.reloading:
            self.render_ammo_amount(display, player)
        else:
            self.draw_reload_img(display, player)

    def draw_reload_img(self, display, player):
        animation = self.cd_obj.animation_database[self.cd_obj.action]
        progress = 1.0 - player.bow.reload_cd / player.bow.max_reload_cd
        progress = max(0.0, min(progress, 1.0))
        frame = min(int(progress * len(animation)), len(animation) - 1)
        img_id = animation[frame]
        img = self.cd_obj.animation_frames[img_id]
        display.blit(img, (self.cd_obj.x, self.cd_obj.y))

    def render_ammo_amount(self, display, player):
        self.small_font.render(display, str(player.bow.ammo), (self.amount_padding, 15))

    def render_pistol(self, display):
        display.blit(self.pistol_img, [0, 15])
