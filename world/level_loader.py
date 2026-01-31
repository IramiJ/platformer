import json
from world.tilemap import read_csv

class Level_loader():
    def __init__(self):
        pass
    def load_level(self, json_file):
        with open(json_file, "r") as file:
            self.data = json.load(file)
        self.map = read_csv(self.data['map'])