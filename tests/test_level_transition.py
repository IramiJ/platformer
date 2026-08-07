import pygame

from world.level_loader import update_level


class FakePlayer:
    def __init__(self, rect):
        self.rect = rect


class FakeLevel:
    def __init__(self, end_rect):
        self.end_rect = end_rect
        self.next_level_calls = 0

    def next_level(self):
        self.next_level_calls += 1


class FinalLevel(FakeLevel):
    def next_level(self):
        self.next_level_calls += 1
        raise FileNotFoundError("No next level")


class FakeWinScreen:
    def __init__(self):
        self.displaying = False


def test_update_level_does_not_change_level_when_player_is_not_at_exit():
    player = FakePlayer(pygame.Rect(0, 0, 24, 24))
    level = FakeLevel(pygame.Rect(100, 100, 24, 24))
    win_screen = FakeWinScreen()

    changed_level = update_level(player, level, None, None, win_screen)

    assert changed_level is False
    assert level.next_level_calls == 0
    assert win_screen.displaying is False


def test_update_level_changes_level_when_player_reaches_exit():
    player = FakePlayer(pygame.Rect(100, 100, 24, 24))
    level = FakeLevel(pygame.Rect(100, 100, 24, 24))
    win_screen = FakeWinScreen()

    changed_level = update_level(player, level, None, None, win_screen)

    assert changed_level is True
    assert level.next_level_calls == 1
    assert win_screen.displaying is False


def test_update_level_shows_win_screen_when_final_level_has_no_next_level():
    player = FakePlayer(pygame.Rect(100, 100, 24, 24))
    level = FinalLevel(pygame.Rect(100, 100, 24, 24))
    win_screen = FakeWinScreen()

    changed_level = update_level(player, level, None, None, win_screen)

    assert changed_level is False
    assert level.next_level_calls == 1
    assert win_screen.displaying is True
