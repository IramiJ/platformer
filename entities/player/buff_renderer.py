from ui.Font_renderer import Font
import pygame


class Buff_renderer():
    def __init__(self ,font: Font, buff_list):
        self.font = font
        self.buff_list = buff_list
        self.imgs = {}
        for buff in buff_list:
            self.imgs[buff] = pygame.image.load(buff_list[buff]["asset_path"]).convert()
            self.imgs[buff].set_colorkey((0,0,0))
    def render_buffs(self, display: pygame.Surface, player):
        y_offset = 0
        for buff in self.buff_list:
            if buff in player.buffs:
                location = [320-self.imgs[buff].get_width()-20, 20+y_offset]
                self.font.render(display, str(player.buffs[buff]//60), [320-10, 40+y_offset])
                display.blit(self.imgs[buff], location)
                y_offset += self.imgs[buff].get_height()
        