from unittest.mock import patch

import pytest

from core.profiler import Profiler


def test_disabled_profiler_does_not_collect_samples():
    profiler = Profiler(enabled=False)

    with profiler.measure("update"):
        pass

    assert profiler.samples == {}


def test_enabled_profiler_records_duration_in_milliseconds():
    profiler = Profiler(enabled=True)

    with (
        patch("core.profiler.time.perf_counter", side_effect=[10.0, 10.005]),
        profiler.measure("update"),
    ):
        pass

    assert list(profiler.samples["update"]) == pytest.approx([5.0])


def test_profiler_keeps_only_the_latest_samples():
    profiler = Profiler(enabled=True, sample_count=2)

    with patch(
        "core.profiler.time.perf_counter",
        side_effect=[1.0, 1.001, 2.0, 2.002, 3.0, 3.003],
    ):
        for _ in range(3):
            with profiler.measure("render"):
                pass

    assert list(profiler.samples["render"]) == pytest.approx([2.0, 3.0])


def test_profiler_calculates_summary_statistics():
    profiler = Profiler(enabled=True)
    profiler.samples["frame"].extend([1.0, 2.0, 3.0, 4.0, 10.0])

    stats = profiler.results()["frame"]

    assert stats.sample_count == 5
    assert stats.average_ms == 4.0
    assert stats.p95_ms == 4.0
    assert stats.maximum_ms == 10.0
