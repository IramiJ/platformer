from core.settings import TILE_SIZE


def tile_to_pixel(value: int) -> int:
    return value * TILE_SIZE


def pixel_to_tile(value: float) -> int:
    return int(value // TILE_SIZE)


def tile_position_to_pixel(position: list[int]) -> list[int]:
    x, y = position
    return [tile_to_pixel(x), tile_to_pixel(y)]
