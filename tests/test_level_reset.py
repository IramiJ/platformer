from types import SimpleNamespace
from unittest.mock import Mock

import pytest

import main


@pytest.fixture
def dirty_game():
    instance = main.Game.__new__(main.Game)
    instance.bullets = [object()]
    instance.sparks = [object()]
    instance.player = SimpleNamespace(
        bow=SimpleNamespace(
            arrows=[object()],
            shoot_cd=1.0,
            reload_cd=2.0,
            reloading=True,
            add_ammo=True,
        ),
        sword=SimpleNamespace(particles=[object()]),
        movement=[100, -100],
        y_momentum=200,
        air_timer=3.0,
        moving_left=True,
        moving_right=True,
        dashing=True,
        dash_timer=0.2,
        dash_cooldown=0.8,
        dmg_cd=0.5,
        hp=1,
        max_hp=5,
        buffs={"double coin": 10.0},
        respawn=True,
    )
    instance.leafSystem = SimpleNamespace(leaves=[object()])
    instance.logic_variables = SimpleNamespace(hitstop_timer=0.5)
    instance.scroll = SimpleNamespace(
        shake_timer=0.5,
        shake_strength=10,
        shake_offset=[4, -3],
        shake_sample_timer=0.1,
    )
    instance.level = SimpleNamespace(
        id=3,
        data={"texts": ["level text"]},
        reload_level=Mock(),
    )
    instance.shop = SimpleNamespace(displaying=True)
    instance.pause_screen = SimpleNamespace(displaying=True)
    instance.win_screen = SimpleNamespace(displaying=True)
    return instance


def test_transient_reset_clears_temporary_collections(dirty_game):
    dirty_game.reset_transient_state()

    assert dirty_game.bullets == []
    assert dirty_game.player.bow.arrows == []
    assert dirty_game.sparks == []
    assert dirty_game.player.sword.particles == []
    assert dirty_game.leafSystem.leaves == []


def test_transient_reset_clears_movement_cooldowns_and_effects(dirty_game):
    dirty_game.reset_transient_state()

    assert dirty_game.player.movement == [0, 0]
    assert dirty_game.player.y_momentum == 0
    assert dirty_game.player.air_timer == 0
    assert dirty_game.player.moving_left is False
    assert dirty_game.player.moving_right is False
    assert dirty_game.player.dashing is False
    assert dirty_game.player.dash_timer == 0
    assert dirty_game.player.dash_cooldown == 0
    assert dirty_game.player.dmg_cd == 0

    assert dirty_game.player.bow.shoot_cd == 0
    assert dirty_game.player.bow.reload_cd == 0
    assert dirty_game.player.bow.reloading is False
    assert dirty_game.player.bow.add_ammo is False

    assert dirty_game.logic_variables.hitstop_timer == 0
    assert dirty_game.scroll.shake_timer == 0
    assert dirty_game.scroll.shake_strength == 0
    assert dirty_game.scroll.shake_offset == [0, 0]
    assert dirty_game.scroll.shake_sample_timer == 0


def test_session_reset_restores_session_state_and_reloads_level(dirty_game):
    dirty_game.initialize_loaded_level = Mock()

    dirty_game.reset_session()

    assert dirty_game.level.id == 1
    assert dirty_game.player.hp == dirty_game.player.max_hp
    assert dirty_game.player.buffs == {}
    assert dirty_game.player.respawn is False
    assert dirty_game.shop.displaying is False
    assert dirty_game.pause_screen.displaying is False
    assert dirty_game.win_screen.displaying is False
    dirty_game.level.reload_level.assert_called_once_with()
    dirty_game.initialize_loaded_level.assert_called_once_with()


def test_loaded_level_initialization_refreshes_level_systems(dirty_game, monkeypatch):
    dirty_game.enemies = SimpleNamespace(load_enemies=Mock())
    dirty_game.texts = SimpleNamespace(load_texts=Mock())
    dirty_game.reset_transient_state = Mock()
    dirty_game.update_tile_rects = Mock()
    initialize_player = Mock()
    monkeypatch.setattr(main, "initialize_player", initialize_player)

    dirty_game.initialize_loaded_level()

    dirty_game.enemies.load_enemies.assert_called_once_with(dirty_game.level)
    dirty_game.texts.load_texts.assert_called_once_with(dirty_game.level.data["texts"])
    initialize_player.assert_called_once_with(dirty_game.player, dirty_game.level)
    dirty_game.reset_transient_state.assert_called_once_with()
    dirty_game.update_tile_rects.assert_called_once_with()
