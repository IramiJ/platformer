import os
import subprocess
import sys

from core.paths import PROJECT_ROOT


def test_game_starts_and_completes_one_headless_frame():
    environment = os.environ.copy()
    environment["SDL_VIDEODRIVER"] = "dummy"
    environment["SDL_AUDIODRIVER"] = "dummy"
    environment["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

    result = subprocess.run(
        [
            sys.executable,
            "-c",
            """
import pygame

pygame.init()

try:
    from main import Game

    game = Game()
    game.update_dt()
    game.run_frame()

    assert pygame.display.get_driver() == 'dummy'
    assert game.level.id == 1
    assert game.player is not None
finally:
    pygame.quit()
""",
        ],
        cwd=PROJECT_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )

    assert result.returncode == 0, (
        f"Headless game startup failed.\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )
