import pytest

from entities.player.bow import Bow
from entities.player.sword import Sword
from main import Game


class FakeCleanupObject:
    def __init__(self, dies_during_update):
        self.alive = True
        self.dies_during_update = dies_during_update
        self.update_calls = 0

    def move(self, *_args):
        self.update_calls += 1
        if self.dies_during_update:
            self.alive = False

    def update(self, _dt):
        self.update_calls += 1
        if self.dies_during_update:
            self.alive = False


@pytest.fixture
def cleanup_objects():
    return [
        FakeCleanupObject(dies_during_update=True),
        FakeCleanupObject(dies_during_update=True),
        FakeCleanupObject(dies_during_update=False),
    ]


@pytest.fixture
def game():
    instance = Game.__new__(Game)
    instance.player = None
    instance.scroll = None
    instance.dt = 0.1
    instance.bullets = []
    instance.sparks = []
    return instance


def test_bullet_cleanup_updates_every_bullet_and_removes_dead_ones(
    game, cleanup_objects
):
    game.bullets = cleanup_objects

    game.move_bullets()

    assert [bullet.update_calls for bullet in cleanup_objects] == [1, 1, 1]
    assert game.bullets == [cleanup_objects[2]]


def test_spark_cleanup_updates_every_spark_and_removes_dead_ones(game, cleanup_objects):
    game.sparks = cleanup_objects

    game.move_sparks()

    assert [spark.update_calls for spark in cleanup_objects] == [1, 1, 1]
    assert game.sparks == [cleanup_objects[2]]


def test_arrow_cleanup_updates_every_arrow_and_removes_dead_ones(cleanup_objects):
    bow = Bow.__new__(Bow)
    bow.arrows = cleanup_objects

    bow.move_arrows([], 0.1)

    assert [arrow.update_calls for arrow in cleanup_objects] == [1, 1, 1]
    assert bow.arrows == [cleanup_objects[2]]


def test_particle_cleanup_updates_every_particle_and_removes_dead_ones(
    cleanup_objects,
):
    sword = Sword.__new__(Sword)
    sword.particles = cleanup_objects

    sword.update_particles(0.1)

    assert [particle.update_calls for particle in cleanup_objects] == [1, 1, 1]
    assert sword.particles == [cleanup_objects[2]]
