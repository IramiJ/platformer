import json

with open("shop.json", "r") as file:
    data = json.load(file)

for entry in data:
    print(data[entry]["price"])
    name = entry
    print(name)
    print(data[entry]["asset_path"])