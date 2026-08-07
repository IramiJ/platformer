import pygame
import pytest

from entities.coins import Coins
from entities.enemies.enemies import Enemies
from entities.player.player import Player
from ui.shopping import Shop


class FakePlayer:
    def __init__(self, coin_amount=0, double_coin_buff=False):
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.coin_amount = coin_amount
        self.buffs = {}
        self.double_coin_buff = double_coin_buff


class FakeCoin:
    def __init__(self):
        self.alive = True

    def collision_test(self, _player_rect):
        return True


class FakeDeadEnemy:
    def __init__(self):
        self.rect = pygame.Rect(10000, 10000, 16, 16)
        self.alive = False

    def update_dmg_timer(self, _dt):
        pass

    def update_frames(self, _dt):
        pass


@pytest.fixture
def shop():
    instance = Shop.__new__(Shop)
    instance.data = {"double coin": {"duration": "30"}}
    instance.prices = {"double coin": "10"}
    instance.item_boxes = {"double coin": pygame.Rect(0, 0, 16, 16)}
    instance.buy_cooldown = 0
    return instance


def test_shop_purchase_deducts_coins_and_adds_buff(shop):
    player = FakePlayer(coin_amount=15)

    shop.buy_on_press(pygame.Rect(1, 1, 1, 1), "double coin", player, player.buffs)

    assert player.coin_amount == 5
    assert player.buffs == {"double coin": 30}


@pytest.mark.parametrize(
    ("coin_amount", "active_buffs"),
    [(9, {}), (20, {"double coin": 5})],
)
def test_shop_rejects_invalid_purchase(shop, coin_amount, active_buffs):
    player = FakePlayer(coin_amount=coin_amount)
    player.buffs = active_buffs.copy()

    shop.buy_on_press(pygame.Rect(1, 1, 1, 1), "double coin", player, player.buffs)

    assert player.coin_amount == coin_amount
    assert player.buffs == active_buffs


def test_double_coin_buff_duration_counts_down_and_expires():
    player = Player.__new__(Player)
    player.buffs = {"double coin": 1.0}
    player.double_coin_buff = False

    player.apply_buffs(0.25)

    assert player.double_coin_buff is True
    assert player.buffs["double coin"] == pytest.approx(0.75)

    player.apply_buffs(0.75)
    player.apply_buffs(0.01)
    player.remove_buffs(["double coin"])

    assert "double coin" not in player.buffs
    assert player.double_coin_buff is False


@pytest.mark.parametrize(
    ("double_coin_buff", "expected_reward"),
    [(False, 1), (True, 2)],
)
def test_coin_collection_reward(double_coin_buff, expected_reward):
    coins = Coins()
    coin = FakeCoin()
    coins.objects = [coin]
    player = FakePlayer(double_coin_buff=double_coin_buff)

    coins.coin_collisions(player)

    assert player.coin_amount == expected_reward
    assert coin.alive is False
    assert coins.objects == []


@pytest.mark.parametrize(
    ("double_coin_buff", "expected_reward"),
    [(False, 4), (True, 8)],
)
def test_multiple_enemy_death_reward(double_coin_buff, expected_reward):
    enemies = Enemies()
    enemies.enemies = [FakeDeadEnemy(), FakeDeadEnemy()]
    player = FakePlayer(double_coin_buff=double_coin_buff)

    enemies.update_enemies(player, [], None, [], None, [], 0.1)

    assert player.coin_amount == expected_reward
    assert enemies.enemies == []
    assert enemies.current_enemy_amount == 0
