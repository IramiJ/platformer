from __future__ import annotations

import os
import statistics
import time
from collections.abc import Callable
from dataclasses import dataclass

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from core.asset_cache import load_image, load_image_file
from core.paths import require_asset_dir, require_asset_file
from core.settings import Settings
from entities.animations import draw_constants
from world.foliage.leaf import Leaf


@dataclass(frozen=True)
class Comparison:
    name: str
    before_us: float
    after_us: float

    @property
    def reduction_percent(self) -> float:
        return (self.before_us - self.after_us) / self.before_us * 100


def time_operation_us(operation: Callable[[], object], iterations: int) -> float:
    start = time.perf_counter()
    for _ in range(iterations):
        operation()
    return (time.perf_counter() - start) * 1_000_000 / iterations


def compare_operations(
    name: str,
    before: Callable[[], object],
    after: Callable[[], object],
    iterations: int,
    rounds: int = 7,
) -> Comparison:
    """Compare paired operations, alternating their order between rounds."""
    before_timings = []
    after_timings = []

    for round_number in range(rounds):
        if round_number % 2 == 0:
            before_timings.append(time_operation_us(before, iterations))
            after_timings.append(time_operation_us(after, iterations))
        else:
            after_timings.append(time_operation_us(after, iterations))
            before_timings.append(time_operation_us(before, iterations))

    return Comparison(
        name,
        statistics.median(before_timings),
        statistics.median(after_timings),
    )


def compare_asset_cache() -> Comparison:
    image_path = require_asset_file("particles/sword_particle.png")

    def load_without_cache() -> pygame.Surface:
        image = pygame.image.load(image_path).convert()
        image.set_colorkey((0, 0, 0))
        return image

    load_image(image_path)
    return compare_operations(
        "Shared asset cache",
        load_without_cache,
        lambda: load_image(image_path),
        iterations=1_000,
    )


def compare_leaf_preloading() -> Comparison:
    leaf_path = next(require_asset_dir("foliage/leaves").glob("*.png"))
    leaf_surface = load_image_file(leaf_path)
    load_image(leaf_path)

    return compare_operations(
        "Preloaded leaf surface",
        lambda: Leaf(load_image(leaf_path), [0, 0], 2.0),
        lambda: Leaf(leaf_surface, [0, 0], 2.0),
        iterations=20_000,
    )


def compare_shop_image_reuse() -> Comparison:
    display = pygame.Surface((320, 240))
    coin_image = load_image("constants/coins.png")

    return compare_operations(
        "Stored shop image",
        lambda: draw_constants(display),
        lambda: display.blit(coin_image, (0, 0)),
        iterations=20_000,
    )


def compare_render_surface_reuse() -> Comparison:
    display = pygame.Surface((320, 240))
    destination = pygame.Surface(Settings.window_size)

    return compare_operations(
        "Reused render surface",
        lambda: pygame.transform.scale(display, Settings.window_size),
        lambda: pygame.transform.scale(display, Settings.window_size, destination),
        iterations=2_000,
    )


def main() -> None:
    pygame.init()
    pygame.display.set_mode((1, 1))

    try:
        comparisons = [
            compare_asset_cache(),
            compare_leaf_preloading(),
            compare_shop_image_reuse(),
            compare_render_surface_reuse(),
        ]

        print("Optimization microbenchmarks (median of 7 rounds)")
        for result in comparisons:
            print(
                f"{result.name:25} "
                f"before={result.before_us:8.3f} us "
                f"after={result.after_us:8.3f} us "
                f"reduction={result.reduction_percent:6.1f}%"
            )
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
