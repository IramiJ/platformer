from ui.Font_renderer import Font
small_font = Font('assets/fonts/small_font.png')
large_font = Font('assets/fonts/large_font.png')

def render_buffs(buff_list, display):
    counter = 0
    for buff in buff_list:
        location = [320-50]
        