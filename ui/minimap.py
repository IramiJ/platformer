import pygame, math
from core.settings import TILE_SIZE
from world.coordinates import pixel_to_tile

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

    def update_map(self, player_pos: list[int], tilemap: list[list[str]]) -> None:
        self.center = [
        pixel_to_tile(player_pos[0]),
        pixel_to_tile(player_pos[1]),
    ]

        minimap_x = self.center[0] - self.size[0] // 2
        minimap_y = self.center[1] - self.size[1] // 2

        for local_y in range(self.size[1]):
            map_y = minimap_y + local_y

            for local_x in range(self.size[0]):
                map_x = minimap_x + local_x

                if (
                    0 <= map_y < len(tilemap)
                    and 0 <= map_x < len(tilemap[map_y])
                ):
                    tile = tilemap[map_y][map_x]
                else:
                    tile = "-1"

                self.map_array[local_y][local_x] = tile


    def to_show(self):
        for i, row in enumerate(self.map_array):
            for j, tile in enumerate(row):
                if tile == "-1":
                    self.minimap_surface.set_at([j, i], (1, 1, 1))
                else:
                    self.minimap_surface.set_at([j, i], (100, 100, 100))
        self.minimap_surface.set_at((20, 15), (0, 255, 0))
        pygame.draw.rect(self.minimap_surface, self.border_color, self.border, 1)

    def render(self, display):
        self.minimap_surface.fill((0, 0, 0))
        self.to_show()
        display.blit(self.minimap_surface, self.pos)
