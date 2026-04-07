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

class Keyboard_event_handler():
    def __init__(self):
        self.keybinds = load_keybinds()
    def handle_keyboard_events(self, player, shop, pause_screen):    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if player.hp <= 0:
                    player.respawn = True
                else:
                    if event.key == self.keybinds["right"]:
                        player.moving_right = True
                    elif event.key == self.keybinds["left"]:
                        player.moving_left = True
                    elif event.key == self.keybinds["jump"]:
                        if player.air_timer < 6:
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
                    elif event.key == self.keybinds["reload"]:
                        if player.mode == "ranged":
                            player.bow.reload()

            elif event.type == pygame.KEYUP:
                if event.key == self.keybinds["right"]:
                    player.moving_right = False
                elif event.key == self.keybinds["left"]:
                    player.moving_left = False