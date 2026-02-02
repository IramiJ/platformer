import json, pygame
from world.tilemap import read_csv

class Level_loader():
    def __init__(self):
        pass
    def load_level(self, json_file):
        with open(json_file, "r") as file:
            self.data = json.load(file)
        self.map = read_csv(self.data['map'])
    def next_level(self):
        id = self.data["id"] + 1
        self.load_level(f"world/levels/level{id}.json")

def update_level(player, level, enemies, win_screen):
    if player.rect.x >= level.data["end_coordinates"][0] and player.rect.y == level.data["end_coordinates"][1]:
        try:
            level.next_level()
        except:
            win_screen.displaying = True
        enemies.load_enemies(level)
        player.spawn_point[0]= level.data["spawn"][0]
        player.spawn_point[1] = level.data["spawn"][1]
        player.rect.x = level.data["spawn"][0]
        player.rect.y = level.data["spawn"][1]
        player.movement = [0, 0]

def reach_checkpoint(player, level):
    for checkpoint in level.data["checkpoints"]:
        if player.rect.collidepoint((checkpoint[0]*16, checkpoint[1]*16)):
            player.spawn_point = [checkpoint[0]*16, checkpoint[1]*16]
            return