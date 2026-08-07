import json

import pygame

from core.paths import PROJECT_ROOT, require_asset_file, validate_asset_path
from entities.animations import draw_constants
from ui.font_renderer import Font


class Shop:
    def __init__(self):
        self.small_font = Font(require_asset_file("fonts/small_font.png"))
        self.large_font = Font(require_asset_file("fonts/large_font.png"))
        with open(PROJECT_ROOT / "ui/shop.json", "r") as file:
            self.data = json.load(file)
        validate_shop_file(self.data)
        self.buy_cooldown = 0
        counter = 1
        self.item_boxes = {}
        self.displaying = False
        self.imgs = {}
        self.prices = {}
        for entry in self.data:
            self.prices[entry] = str(self.data[entry]["price"])
            self.imgs[entry] = (
                pygame.image.load(
                    require_asset_file(self.data[entry]["asset_path"])
                ).convert(),
                [0, 32 * counter],
            )
            self.item_boxes[entry] = pygame.Rect(
                self.imgs[entry][1][0],
                self.imgs[entry][1][1],
                self.imgs[entry][0].get_width(),
                self.imgs[entry][0].get_height(),
            )
            counter += 1

    def render(self, surf, player_coin_amount):
        surf.fill((0, 0, 0))
        self.large_font.render(surf, "SHOP", (150, 0))
        draw_constants(surf)
        self.draw_items(surf)
        self.large_font.render(surf, str(player_coin_amount), (16, 0))

    def draw_items(self, surf):
        for item in self.imgs:
            self.small_font.render(surf, item, (0, self.imgs[item][1][1] - 8))
            self.large_font.render(
                surf, self.prices[item], [36, self.imgs[item][1][1] + 2]
            )
            (
                self.small_font.render(
                    surf,
                    "duration: " + str(self.data[item]["duration"]),
                    [60, self.imgs[item][1][1] + 2],
                ),
            )
            surf.blit(
                self.imgs[item][0], (self.item_boxes[item].x, self.item_boxes[item].y)
            )

    def buy(self, player, buff_list):
        for item in self.imgs:
            if pygame.mouse.get_pressed()[0]:
                mouse_rect = pygame.Rect(
                    pygame.mouse.get_pos()[0] / 2, pygame.mouse.get_pos()[1] / 2, 1, 1
                )
                self.buy_on_press(mouse_rect, item, player, buff_list)

    def buy_on_press(self, mouse_rect, item, player, buff_list):
        if mouse_rect.colliderect(self.item_boxes[item]) and (
            player.coin_amount >= int(self.prices[item])
            and self.buy_cooldown == 0
            and item not in buff_list
        ):
            player.coin_amount -= int(self.prices[item])
            self.buy_cooldown = 0
            buff_list[item] = int(self.data[item]["duration"])

    def change_displaying(self):
        self.displaying = not self.displaying
        return self.displaying

    def show(self, display, player):
        if self.displaying:
            self.render(display, player.coin_amount)

    def update(self, player):
        if not self.displaying:
            return

        player.moving_right = False
        player.moving_left = False
        self.buy(player, player.buffs)


def validate_shop_file(data):
    errors = []

    required_fields = {
        "price": str,
        "duration": str,
        "description": str,
        "asset_path": str,
    }

    supported_buffs = ["double coin", "speed boost", "jump boost"]

    if not isinstance(data, dict):
        raise TypeError("shop file must contain a JSON object")
    for item, item_data in data.items():
        if item not in supported_buffs:
            errors.append(f"{item} is not a valid buff")
            continue
        if not isinstance(item_data, dict):
            errors.append(f"{item} must be a JSON object")
            continue
        for field, expected_type in required_fields.items():
            if field not in item_data:
                errors.append(f"{item} is missing field: {field}")
                continue
            if not isinstance(item_data[field], expected_type):
                errors.append(
                    f"the field {field} of item {item} is not of type {expected_type.__name__}"
                )

        if isinstance(item_data.get("price"), str) and not is_positive_int(
            item_data["price"]
        ):
            errors.append(f"in field {item}, 'price' is not a positive integer")
        if isinstance(item_data.get("duration"), str) and not is_positive_int(
            item_data["duration"]
        ):
            errors.append(f"in field {item}, 'duration' is not a positive integer")
        if isinstance(item_data.get("asset_path"), str):
            asset_path = item_data["asset_path"]
            if not validate_asset_path(asset_path):
                errors.append(
                    f"in field {item}, asset does not exist: {item_data['asset_path']}"
                )
    if errors:
        raise ValueError("\n".join(errors))


def is_positive_int(value: str) -> bool:
    try:
        number = int(value)
    except ValueError:
        return False
    return number > 0
