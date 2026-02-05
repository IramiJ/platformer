import pygame, sys, json

def load_keybinds(path="core/keybinds.json"):
    with open(path, "r") as f:
        raw = json.load(f)

    binds = {}
    for action, key_name in raw.items():
        try:
            binds[action] = getattr(pygame, key_name)
        except AttributeError:
            raise ValueError(f"Invalid key name in JSON: {key_name} (action: {action})")

    return binds


def kb_events(player, shop, pause_screen):
    keybinds = load_keybinds()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == keybinds["right"]:
                player.moving_right = True
            elif event.key == keybinds["left"]:
                player.moving_left = True
            elif event.key == keybinds["jump"]:
                if player.air_timer < 6:
                    player.y_momentum = player.jump_momentum
            elif event.key == keybinds["shop"]:
                shop.change_displaying()
            elif event.key == keybinds["dash"]:
                player.dash()
            elif event.key == keybinds["pause"]:
                pause_screen.change_displaying()
            elif event.key == keybinds["switch_mode"]:
                player.switch_mode()

        elif event.type == pygame.KEYUP:
            if event.key == keybinds["right"]:
                player.moving_right = False
            elif event.key == keybinds["left"]:
                player.moving_left = False