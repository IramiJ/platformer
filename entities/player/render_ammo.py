import pygame

from ui.Font_renderer import Font
small_font = Font('assets/fonts/small_font.png')
def render_ammo(display, player):
    img = pygame.image.load("assets/constants/cd_pistol.png").convert()
    img.set_colorkey((0,0,0))
    display.blit(img, [320-img.get_width()-20, 15])
    small_font.render(display, str(player.pistol.ammo), (320-10, 15))
