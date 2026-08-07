import pygame

from world.collisions import collision_test, move_collisions


def test_collision_test_with_no_tile():
    rect = pygame.Rect(0, 0, 24, 24)
    tiles = [
        pygame.Rect(50, 50, 24, 24),
        pygame.Rect(100, 100, 24, 24),
        pygame.Rect(200, 200, 24, 24),
    ]
    assert collision_test(rect, tiles) == []


def test_collision_test_with_overlap():
    rect = pygame.Rect(0, 0, 24, 24)
    tiles = [pygame.Rect(0, 0, 24, 24), pygame.Rect(100, 100, 24, 24)]
    assert collision_test(rect, tiles) == [tiles[0]]


def test_collision_test_with_multiple_overlaps():
    rect = pygame.Rect(0, 0, 100, 100)
    tiles = [
        pygame.Rect(0, 0, 24, 24),
        pygame.Rect(24, 24, 24, 24),
        pygame.Rect(50, 50, 24, 24),
        pygame.Rect(200, 200, 24, 24),
        pygame.Rect(300, 300, 24, 24),
    ]
    assert collision_test(rect, tiles) == [tiles[i] for i in range(3)]


def test_move_collisions_horizontally():
    rect = pygame.Rect(0, 0, 24, 24)
    movement = [500, 0]
    tiles = [pygame.Rect(48, 0, 24, 24), pygame.Rect(48, 24, 24, 24)]
    dt = 0.1
    moved_rect, collisions = move_collisions(rect, movement, tiles, dt)

    assert moved_rect.right == tiles[0].left
    assert collisions == {"top": False, "bottom": False, "left": False, "right": True}


def test_move_collisions_vertically():
    rect = pygame.Rect(0, 0, 24, 24)
    movement = [0, 500]
    tiles = [pygame.Rect(0, 48, 24, 24), pygame.Rect(24, 48, 24, 24)]
    dt = 0.1
    moved_rect, collisions = move_collisions(rect, movement, tiles, dt)

    assert moved_rect.bottom == tiles[0].top
    assert collisions == {"top": False, "bottom": True, "left": False, "right": False}
