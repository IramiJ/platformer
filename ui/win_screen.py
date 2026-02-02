from ui.Font_renderer import Font
small_font = Font('assets/fonts/small_font.png')
large_font = Font('assets/fonts/large_font.png')

class Win_screen:
    def __init__(self):
        self.displaying = False
    
    def render(self, surf):
        surf.fill((0,0,0))
        large_font.render(surf, "YOU WON", (130, 0))
    def change_displaying(self):
        self.displaying = not self.displaying