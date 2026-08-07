from ui.minimap import Minimap
from world.coordinates import tile_position_to_pixel


def test_minimap_at_top_left_boundary():
    tilemap = [
        ["top-left", "top-middle", "top-right"],
        ["middle-left", "center", "middle-right"],
        ["bottom-left", "bottom-middle", "bottom-right"],
    ]
    minimap = Minimap()

    minimap.update_map(tile_position_to_pixel([0, 0]), tilemap)

    center_x = minimap.size[0] // 2
    center_y = minimap.size[1] // 2
    assert minimap.map_array[center_y][center_x] == "top-left"
    assert minimap.map_array[center_y][center_x - 1] == "-1"
    assert minimap.map_array[center_y - 1][center_x] == "-1"
    assert minimap.map_array[center_y + 2][center_x + 2] == "bottom-right"


def test_minimap_at_bottom_right_boundary():
    tilemap = [
        ["top-left", "top-middle", "top-right"],
        ["middle-left", "center", "middle-right"],
        ["bottom-left", "bottom-middle", "bottom-right"],
    ]
    minimap = Minimap()

    minimap.update_map(tile_position_to_pixel([2, 2]), tilemap)

    center_x = minimap.size[0] // 2
    center_y = minimap.size[1] // 2
    assert minimap.map_array[center_y][center_x] == "bottom-right"
    assert minimap.map_array[center_y][center_x + 1] == "-1"
    assert minimap.map_array[center_y + 1][center_x] == "-1"
    assert minimap.map_array[center_y - 2][center_x - 2] == "top-left"
