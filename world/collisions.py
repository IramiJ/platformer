import pygame


def collision_test(
    rect: pygame.Rect | pygame.FRect, tiles: list[pygame.Rect]
) -> list[pygame.Rect]:
    """
    Takes a rect and checks the collision with all tiles that are being given.
    """
    hit_list: list[pygame.Rect] = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move_collisions(
    rect: pygame.FRect, movement: list[float], tiles: list[pygame.Rect], dt: float
) -> tuple[pygame.FRect, dict[str, bool]]:
    """
    Moves a rect in both the x and y direction seperately, while also making sure that collisions are being resolved
    """
    collision_types = {"top": False, "bottom": False, "left": False, "right": False}
    x_movement(rect, movement, dt, tiles, collision_types)
    y_movement(rect, movement, dt, tiles, collision_types)
    return rect, collision_types


def x_movement(
    rect: pygame.FRect,
    movement: list[float],
    dt: float,
    tiles: list[pygame.Rect],
    collision_types: dict[str, bool],
) -> None:
    rect.x += movement[0] * dt
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types["right"] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types["left"] = True


def y_movement(
    rect: pygame.FRect,
    movement: list[float],
    dt: float,
    tiles: list[pygame.Rect],
    collision_types: dict[str, bool],
) -> None:
    rect.y += movement[1] * dt
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types["bottom"] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types["top"] = True
