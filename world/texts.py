from ui.Font_renderer import Font



class Texts:
    def __init__(self):
        self.strings = {}
        self.large_font = Font('assets/fonts/large_font.png')

    def load_texts(self, data):
        self.strings = data
    
    def render_texts(self, display, scroll):
        for text in self.strings:
            self.large_font.render(display, text, [self.strings[text][0] * 16 - scroll.render_scroll[0], self.strings[text][1] * 16 - scroll.render_scroll[1]])