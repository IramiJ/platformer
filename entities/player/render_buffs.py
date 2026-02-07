from ui.Font_renderer import Font
import pygame
small_font = Font('assets/fonts/small_font.png')
large_font = Font('assets/fonts/large_font.png')

def render_buffs(buff_list, display: pygame.Surface, player):
    y_offset = 0
    for buff in buff_list:
        if buff in player.buffs:
            img = pygame.image.load(buff_list[buff]["asset_path"]).convert()
            img.set_colorkey((0,0,0))
            location = [320-img.get_width()-20, 20+y_offset]
            small_font.render(display, str(player.buffs[buff]//60), [320-10, 40+y_offset])
            display.blit(img, location)
            y_offset += img.get_height()
        