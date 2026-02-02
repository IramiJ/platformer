import pygame

class Hp_bar():
    def __init__(self, bg, frame, x, y):
        self.bg = pygame.image.load(bg).convert()
        self.bg.set_colorkey((0,0,0))
        self.frame = pygame.image.load(frame).convert()
        self.frame.set_colorkey((0,0,0))
        self.x = x
        self.y = y
        self.width = self.frame.get_width()
        self.height = self.frame.get_height()
        
    def draw(self, display, max_hp, current_hp):
        display.blit(self.frame, (self.x, self.y))
        fill_width = int(self.width * (current_hp / max_hp))
        fill_rect = pygame.Rect(0, 0, fill_width, self.height)
        display.blit(self.bg, (self.x, self.y), fill_rect)
        
