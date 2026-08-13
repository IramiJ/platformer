from __future__ import annotations

import time
from collections import defaultdict, deque
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass


@dataclass(frozen=True)
class ProfileStats:
    """Summary statistics for one measured code section."""

    sample_count: int
    average_ms: float
    p95_ms: float
    maximum_ms: float


class Profiler:
    """Collect and periodically report timing samples for named code sections."""

    def __init__(self, enabled: bool = False, sample_count: int = 300) -> None:
        self.enabled = enabled
        self.samples: dict[str, deque[float]] = defaultdict(
            lambda: deque(maxlen=sample_count)
        )
        self.frames_since_report = 0
        self.report_interval = sample_count

    @contextmanager
    def measure(self, name: str) -> Iterator[None]:
        """Measure a code section and store its duration in milliseconds."""
        if not self.enabled:
            yield
            return

        start = time.perf_counter()

        try:
            yield
        finally:
            duration_ms = (time.perf_counter() - start) * 1000
            self.samples[name].append(duration_ms)

    def finish_frame(self) -> None:
        """Print the latest sample window after the configured frame interval."""
        if not self.enabled:
            return

        self.frames_since_report += 1
        if self.frames_since_report >= self.report_interval:
            self.print_results()
            self.frames_since_report = 0

    def print_results(self) -> None:
        """Print average, 95th percentile, and maximum section durations."""
        print("\n--- Profiling results ---")

        for name, stats in self.results().items():
            print(
                f"{name:12} "
                f"avg={stats.average_ms:6.2f} ms "
                f"p95={stats.p95_ms:6.2f} ms "
                f"max={stats.maximum_ms:6.2f} ms "
                f"n={stats.sample_count}"
            )

    def results(self) -> dict[str, ProfileStats]:
        """Return summary statistics for all sections that have samples."""
        results: dict[str, ProfileStats] = {}

        for name, values in self.samples.items():
            if not values:
                continue

            sorted_values = sorted(values)
            p95_index = int((len(sorted_values) - 1) * 0.95)
            results[name] = ProfileStats(
                sample_count=len(values),
                average_ms=sum(values) / len(values),
                p95_ms=sorted_values[p95_index],
                maximum_ms=max(values),
            )

        return results
