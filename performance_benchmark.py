from __future__ import annotations

import argparse
import os
import platform
import time

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from core.paths import require_asset_file
from core.profiler import Profiler
from core.settings import Settings
from entities.enemies.patroller import Patroller
from entities.particles import Particle
from main import Game

DEFAULT_FRAMES = 600
DEFAULT_WARMUP_FRAMES = 120
DEFAULT_ENEMIES = 50
DEFAULT_PARTICLES = 500


def populate_stress_scenario(game: Game, enemy_count: int, particle_count: int) -> None:
    """Populate the current level with active enemies and long-lived particles."""
    player_x = game.player.rect.x
    player_y = game.player.rect.y

    enemies = []
    for index in range(enemy_count):
        column = index % 15
        row = (index // 15) % 4
        enemy = Patroller(
            player_x + 72 + column * 24,
            player_y - row * 24,
            16,
            16,
        )
        enemy.update_frames(0)
        enemies.append(enemy)

    game.enemies.enemies = enemies
    game.enemies.max_enemy_amount = len(enemies)
    game.enemies.current_enemy_amount = len(enemies)

    particle_image = require_asset_file("particles/sword_particle.png")
    game.player.sword.particles = [
        Particle(
            particle_image,
            [player_x + index % 40, player_y - (index // 40) % 10],
            duration=60.0,
        )
        for index in range(particle_count)
    ]

    game.player.max_hp = 100_000
    game.player.hp = game.player.max_hp


def run_fixed_frames(game: Game, frame_count: int) -> float:
    """Run frames with a fixed simulation step and return elapsed wall time."""
    fixed_dt = 1.0 / Settings.fps
    start = time.perf_counter()

    for _ in range(frame_count):
        game.dt = fixed_dt
        game.run_frame()

    return time.perf_counter() - start


def run_benchmark(
    frame_count: int,
    warmup_frames: int,
    enemy_count: int,
    particle_count: int,
) -> bool:
    """Run the reproducible stress benchmark and report the 60 FPS verdict."""
    pygame.init()

    try:
        game = Game(profiling=True)
        print("Startup and asset loading:")
        game.profiler.print_results()

        populate_stress_scenario(game, enemy_count, particle_count)

        game.profiler = Profiler(enabled=False)
        run_fixed_frames(game, warmup_frames)

        game.profiler = Profiler(enabled=True, sample_count=frame_count)
        elapsed_seconds = run_fixed_frames(game, frame_count)

        print(
            f"\nStress load: {enemy_count} enemies, "
            f"{particle_count} particles, {frame_count} measured frames"
        )
        print(
            f"Environment: {platform.system()} {platform.release()}, "
            f"Python {platform.python_version()}, pygame-ce {pygame.version.ver}"
        )
        game.profiler.print_results()

        frame_stats = game.profiler.results()["cpu_frame"]
        frame_budget_ms = 1000.0 / Settings.fps
        throughput_fps = frame_count / elapsed_seconds
        over_budget_count = sum(
            duration > frame_budget_ms
            for duration in game.profiler.samples["cpu_frame"]
        )
        over_budget_percent = over_budget_count / frame_count * 100
        meets_target = frame_stats.p95_ms <= frame_budget_ms
        verdict = "PASS" if meets_target else "FAIL"

        print(f"\nUncapped throughput: {throughput_fps:.1f} FPS")
        print(
            f"Frames over budget: {over_budget_count}/{frame_count} "
            f"({over_budget_percent:.2f}%)"
        )
        print(
            f"Target: {Settings.fps} FPS ({frame_budget_ms:.2f} ms budget), "
            f"CPU-frame P95: {frame_stats.p95_ms:.2f} ms -> {verdict}"
        )
        return meets_target
    finally:
        pygame.quit()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the platformer stress benchmark")
    parser.add_argument("--frames", type=int, default=DEFAULT_FRAMES)
    parser.add_argument("--warmup-frames", type=int, default=DEFAULT_WARMUP_FRAMES)
    parser.add_argument("--enemies", type=int, default=DEFAULT_ENEMIES)
    parser.add_argument("--particles", type=int, default=DEFAULT_PARTICLES)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    passed = run_benchmark(
        frame_count=arguments.frames,
        warmup_frames=arguments.warmup_frames,
        enemy_count=arguments.enemies,
        particle_count=arguments.particles,
    )
    raise SystemExit(0 if passed else 1)
