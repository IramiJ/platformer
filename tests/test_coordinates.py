import pytest

from world.coordinates import pixel_to_tile, tile_position_to_pixel, tile_to_pixel


@pytest.mark.parametrize(
    ("tile_position", "pixel_position"),
    [([0, 0], [0, 0]), ([20, 0], [480, 0]), ([5, 5], [120, 120])],
)
def test_tile_position_to_pixel(tile_position, pixel_position):
    assert tile_position_to_pixel(tile_position) == pixel_position


@pytest.mark.parametrize(("tile", "pixel"), [(0, 0), (3, 72), (10, 240)])
def test_tile_to_pixel(tile, pixel):
    assert tile_to_pixel(tile) == pixel


@pytest.mark.parametrize(
    ("pixel", "tile"), [(0, 0), (23, 0), (24, 1), (36, 1), (48, 2)]
)
def test_pixel_to_tile(pixel, tile):
    assert pixel_to_tile(pixel) == tile
