import pygame

class Minimap:
    def __init__(self):
        self.size = [40, 30]
        self.pos = [280, 0]
        self.map_array = []
        self.minimap_surface = pygame.Surface(self.size)
        self.border_color = (200, 200, 200)
        self.border = pygame.Rect(0, 0, self.size[0], self.size[1])
    def load_map(self, map):
        self.map_array = map
    def to_show(self):    
        pygame.draw.rect(self.minimap_surface, self.border_color, self.border, 1)
    def closest_to_player(self):
        pass
    def render(self, display):
        display.blit(self.minimap_surface, self.pos)