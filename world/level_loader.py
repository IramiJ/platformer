import json
from world.tilemap import read_csv

from .tilemap import load_torches

class Level_loader():
    def __init__(self):
        self.id = 1
    def load_level(self, json_file):
        with open(json_file, "r") as file:
            self.data = json.load(file)
        self.map = read_csv(self.data['map'])
    def reload_level(self):
        self.load_level(f"world/levels/level{self.id}.json")
    def next_level(self):
        self.id += 1
        self.load_level(f"world/levels/level{self.id}.json")

def update_level(player, level, enemies, torches, texts, win_screen):
    if player.rect.x >= level.data["end_coordinates"][0] and player.rect.y == level.data["end_coordinates"][1]:
        try:
            level.next_level()
        except:
            win_screen.displaying = True
        enemies.load_enemies(level)
        load_torches(level.map, torches)
        texts.load_texts(level.data["texts"])
        player.spawn_point[0]= level.data["spawn"][0]
        player.spawn_point[1] = level.data["spawn"][1]
        player.rect.x = level.data["spawn"][0]
        player.rect.y = level.data["spawn"][1]
        player.movement = [0, 0]
def reload_level(enemies, level, torches, player, texts):
    level.reload_level()
    enemies.load_enemies(level)
    texts.load_texts(level.data["texts"])
    load_torches(level.map, torches)
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