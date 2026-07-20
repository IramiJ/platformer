from ui.Font_renderer import Font
from core.settings import TILE_SIZE
from world.coordinates import tile_to_pixel

class Texts:
    def __init__(self):
        self.strings = {}
        self.large_font = Font("assets/fonts/large_font.png")

    def load_texts(self, data):
        self.strings = data

    def render_texts(self, display, scroll):
        for text in self.strings:
            self.large_font.render(
                display,
                text,
                [
                    tile_to_pixel(self.strings[text][0]) - scroll.render_scroll[0],
                    tile_to_pixel(self.strings[text][1]) - scroll.render_scroll[1],
                ],
            )
