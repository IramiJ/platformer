from ui.Font_renderer import Font
from core.paths import assets_path

class Pause_screen:
    def __init__(self):
        self.small_font = Font(assets_path("fonts/small_font.png"))
        self.large_font = Font(assets_path("fonts/large_font.png"))
        self.displaying = False

    def render(self, surf):
        surf.fill((0, 0, 0))
        self.large_font.render(surf, "PAUSE", (144, 0))

    def change_displaying(self):
        self.displaying = not self.displaying
