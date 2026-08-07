import pytest

from core.paths import PROJECT_ROOT
from core.settings import TILE_SIZE
from world.level_loader import Level_loader, LevelValidationError, validate_level


def make_valid_level():
    return {
        "id": 1,
        "map": "maps/map1.csv",
        "spawn": [0, 14],
        "max_y": 28,
        "enemies": {
            "Patroller": [[51, 8]],
            "Heavy_Patroller": [],
            "Chaser": [],
            "Shooter": [[70, 13]],
        },
        "checkpoints": [[10, 12]],
        "end_coordinates": [99, 6],
        "texts": {
            "press SPACE to jump": [5, 11],
            "gate to the next level": [94, 3],
        },
    }


def assert_invalid_level(level_data, *expected_messages):
    with pytest.raises(LevelValidationError) as error:
        validate_level(level_data, "test-level.json")

    error_message = str(error.value)
    assert "Invalid Leveldata: test-level.json" in error_message
    for expected_message in expected_messages:
        assert expected_message in error_message


def test_validate_level_accepts_valid_level_data():
    validate_level(make_valid_level(), "test-level.json")


@pytest.mark.parametrize(
    ("field", "expected_message"),
    [
        ("id", "Required field 'id"),
        ("map", "Required field 'map"),
        ("spawn", "Required field 'spawn"),
        ("max_y", "Required field 'max_y"),
        ("enemies", "Required field 'enemies"),
        ("checkpoints", "Required field 'checkpoints"),
        ("end_coordinates", "Required field 'end_coordinates"),
        ("texts", "Required field 'texts"),
    ],
)
def test_validate_level_rejects_missing_required_fields(field, expected_message):
    level_data = make_valid_level()
    del level_data[field]

    assert_invalid_level(level_data, expected_message)


@pytest.mark.parametrize(
    ("field", "value", "expected_message"),
    [
        ("id", "1", "'id' must be int"),
        ("map", ["maps/map1.csv"], "'map' must be str"),
        ("spawn", "0,14", "'spawn' must be list"),
        ("max_y", "28", "'max_y' must be int"),
        ("enemies", [], "'enemies' must be dict"),
        ("checkpoints", {}, "'checkpoints' must be list"),
        ("end_coordinates", "99,6", "'end_coordinates' must be list"),
        ("texts", [], "'texts' must be dict"),
    ],
)
def test_validate_level_rejects_wrong_required_field_types(
    field, value, expected_message
):
    level_data = make_valid_level()
    level_data[field] = value

    assert_invalid_level(level_data, expected_message)


@pytest.mark.parametrize(
    ("field", "value", "expected_message"),
    [
        ("spawn", [0], "'spawn' must be a position like [1, 1]"),
        ("spawn", [0, "14"], "'spawn' must be a position like [1, 1]"),
        ("spawn", [0, 14.0], "'spawn' must be a position like [1, 1]"),
        (
            "end_coordinates",
            [99, "6"],
            "'end_coordinates' must be a position like [1, 1]",
        ),
    ],
)
def test_validate_level_rejects_invalid_positions(field, value, expected_message):
    level_data = make_valid_level()
    level_data[field] = value

    assert_invalid_level(level_data, expected_message)


def test_validate_level_rejects_invalid_checkpoint_positions():
    level_data = make_valid_level()
    level_data["checkpoints"] = [[10, 12], [1], [2, "3"]]

    assert_invalid_level(
        level_data,
        "'checkpoints[1] must be a position like [1, 1]",
        "'checkpoints[2] must be a position like [1, 1]",
    )


def test_validate_level_rejects_missing_map_file():
    level_data = make_valid_level()
    level_data["map"] = "maps/does-not-exist.csv"

    assert_invalid_level(level_data, "Map-file doesn't exist: maps/does-not-exist.csv")


def test_validate_level_rejects_unknown_enemy_type():
    level_data = make_valid_level()
    level_data["enemies"]["Boss"] = [[4, 5]]

    assert_invalid_level(level_data, "Unknown enemy type: 'Boss'")


def test_validate_level_rejects_enemy_positions_that_are_not_lists():
    level_data = make_valid_level()
    level_data["enemies"]["Patroller"] = {"x": 51, "y": 8}

    assert_invalid_level(level_data, "'enemies.Patroller' musst be a list")


def test_validate_level_rejects_invalid_enemy_positions():
    level_data = make_valid_level()
    level_data["enemies"]["Shooter"] = [[70, 13], [2], [3, "4"]]

    assert_invalid_level(
        level_data,
        "'enemies.Shooter[1] musst be [x, y]",
        "'enemies.Shooter[2] musst be [x, y]",
    )


def test_validate_level_rejects_non_dictionary_texts():
    level_data = make_valid_level()
    level_data["texts"] = []

    assert_invalid_level(
        level_data,
        "'texts' must be dict",
        "field 'texts' is not a dictionary",
    )


def test_validate_level_rejects_invalid_text_entries():
    level_data = make_valid_level()
    level_data["texts"] = {
        "valid text": [5, 11],
        123: [6, 11],
        "invalid position": [7],
    }

    assert_invalid_level(
        level_data,
        "Every text key must be a string",
        "Position of text 'invalid position' must be [x, y]",
    )


@pytest.mark.parametrize("level_id", [1, 2, 3])
def test_project_level_files_pass_validation(level_id):
    loader = Level_loader()
    loader.load_level(PROJECT_ROOT / f"world/levels/level{level_id}.json")

    assert loader.data["id"] == level_id
    assert loader.map
    assert loader.max_y_px == loader.data["max_y"] * TILE_SIZE
    assert loader.end_rect.topleft == (
        loader.data["end_coordinates"][0] * TILE_SIZE,
        loader.data["end_coordinates"][1] * TILE_SIZE,
    )
