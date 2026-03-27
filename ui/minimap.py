import pygame, math

class Minimap:
    def __init__(self):
        self.size = [40, 30]
        self.pos = [280, 0]
        self.map_array = [[0 for _ in range(self.size[0])] for _ in range(self.size[1])]
        self.minimap_surface = pygame.Surface(self.size)
        self.border_color = (200, 200, 200)
        self.border = pygame.Rect(0, 0, self.size[0], self.size[1])
        self.NON_RENDER_TILES = {"-1"}
        self.center = [0, 0]
    def update_map(self, player_pos, tilemap):
        self.center = [round(player_pos[0]/16), round(player_pos[1]/16)]
        minimap_x = self.center[0] - self.size[0] // 2
        minimap_y = self.center[1] - self.size[1] // 2
        for y in range(minimap_y, minimap_y + self.size[1]):
            row = tilemap[y]
            for x in range(minimap_x, minimap_x + self.size[0]):
                tile = row[x]
                self.map_array[y-minimap_y][x-minimap_x] = tile

    def to_show(self):
        for i, row in enumerate(self.map_array):
            for j, tile in enumerate(row):
                if tile == "-1":
                    self.minimap_surface.set_at([j, i], (1,1,1))
                else:
                   self.minimap_surface.set_at([j, i], (100,100,100))
        self.minimap_surface.set_at((20, 15), (0,255,0))
        pygame.draw.rect(self.minimap_surface, self.border_color, self.border, 1)
    def render(self, display):
        self.minimap_surface.fill((0, 0, 0))
        self.to_show()
        display.blit(self.minimap_surface, self.pos)