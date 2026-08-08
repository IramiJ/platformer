from __future__ import annotations

import json
import sys
from typing import TYPE_CHECKING

import pygame

from core.paths import PROJECT_ROOT

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

    from entities.player.player import Player
    from ui.pause_screen import PauseScreen
    from ui.shopping import Shop
    from ui.win_screen import WinScreen


def load_keybinds(
    path: str | Path = PROJECT_ROOT / "core/keybinds.json",
) -> dict[str, int]:
    """
    Takes the keybinds.json file from this directory and returns valid pygame keybinds.
    """
    with open(path, "r") as f:
        raw = json.load(f)
    validate_keybinds(raw)
    binds: dict[str, int] = {}
    for action, key_name in raw.items():
        try:
            binds[action] = getattr(pygame, key_name)
        except AttributeError:
            raise ValueError(f"Invalid key name in JSON: {key_name} (action: {action})")

    return binds


def validate_keybinds(data: Mapping[str, object]) -> None:
    """
    Makes sure all necessary keybinds are there and all keys are syntactically correct
    """
    errors: list[str] = []

    required_keys = [
        "right",
        "left",
        "jump",
        "shop",
        "dash",
        "pause",
        "switch_mode",
        "shoot",
        "reload",
    ]
    for key in required_keys:
        if key not in data:
            errors.append(f"required key {key} is missing")
    for action, key_name in data.items():
        if not (
            isinstance(key_name, str)
            and key_name.startswith("K_")
            and hasattr(pygame, key_name)
        ):
            errors.append(f"invalid pygame key for {action}: {key_name}")

    if errors:
        raise ValueError("\n".join(errors))


class KeyboardEventHandler:
    """
    Takes care of all everything regarding actual clicks on the keyboard, such as jumps or attacks.
    Uses the Keybinds in the keybinds.json file of the same directory.
    """

    def __init__(self) -> None:
        self.keybinds = load_keybinds()

    def handle_keyboard_events(
        self,
        player: Player,
        shop: Shop,
        pause_screen: PauseScreen,
        win_screen: WinScreen,
    ) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if player.hp <= 0:
                    player.respawn = True
                    continue
                if win_screen.displaying:
                    continue
                if pause_screen.displaying:
                    if event.key == self.keybinds["pause"]:
                        pause_screen.change_displaying()
                    continue

                if shop.displaying:
                    if event.key == self.keybinds["shop"]:
                        shop.change_displaying()
                    continue
                else:
                    if event.key == self.keybinds["right"]:
                        player.moving_right = True
                    elif event.key == self.keybinds["left"]:
                        player.moving_left = True
                    elif event.key == self.keybinds["jump"]:
                        if player.air_timer < 0.1:
                            player.y_momentum = player.jump_momentum
                    elif event.key == self.keybinds["shop"]:
                        shop.change_displaying()
                    elif event.key == self.keybinds["dash"]:
                        player.dash()
                    elif event.key == self.keybinds["pause"]:
                        pause_screen.change_displaying()
                    elif event.key == self.keybinds["switch_mode"]:
                        player.switch_mode()
                    elif event.key == self.keybinds["shoot"]:
                        if player.mode == "ranged":
                            player.bow.add_arrow()
                    elif (
                        event.key == self.keybinds["reload"] and player.mode == "ranged"
                    ):
                        player.bow.reload()

            elif event.type == pygame.KEYUP:
                if event.key == self.keybinds["right"]:
                    player.moving_right = False
                elif event.key == self.keybinds["left"]:
                    player.moving_left = False
