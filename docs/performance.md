# Performance measurements

Measurements were recorded on August 13, 2026, using Windows 10 (build
19045), an AMD64 Family 25 Model 80 CPU, Python 3.13.12, and pygame-ce 2.5.6.
The automated benchmarks use SDL's dummy video and audio drivers so that the
same workload can run without user input.

## Reproducing the measurements

Run the game with a rolling report every 300 frames:

```powershell
python main.py --profile
```

Run the fixed stress scenario:

```powershell
python performance_benchmark.py
```

Run the isolated before/after comparisons:

```powershell
python performance_comparison.py
```

Microbenchmarks should be rerun on the same machine with other applications
closed. Their absolute values vary between systems, so the comparison between
the two implementations is more useful than a single duration.

## Optimization comparisons

The comparison script reproduces the code pattern immediately before and after
each optimization. Each value is the median per operation over seven paired
rounds; the order of the before and after operation alternates between rounds.

| Optimization | Before | After | Reduction |
| --- | ---: | ---: | ---: |
| Shared asset cache (`924973a`) | 90.548 us | 0.130 us | 99.9% |
| Preloaded leaf surface (`a773cf0`) | 1.967 us | 1.918 us | 2.5% |
| Stored shop image (`a773cf0`) | 0.620 us | 0.572 us | 7.8% |
| Reused render surface (`a773cf0`) | 502.872 us | 191.172 us | 62.0% |

The leaf improvement is deliberately reported as modest. The shared cache was
already present by that point, so preloading removed a cached function lookup
per leaf rather than a disk read. Reusing the render destination produces the
largest recurring frame-time improvement and also avoids allocating a new
640x480 surface every frame.

## Startup and asset loading baseline

These are cold-start subsystem measurements from one profiled `Game`
construction. A subsystem duration includes asset decoding, surface conversion,
animation copies, and the small amount of object initialization surrounding
those operations.

| Startup section | Duration |
| --- | ---: |
| Tiles | 13.71 ms |
| Level data | 1.83 ms |
| Player and equipment | 12.49 ms |
| HUD and fonts | 3.30 ms |
| Overlays and shop | 1.84 ms |
| Enemies | 4.22 ms |
| Ammo UI | 1.04 ms |
| Text renderer | 0.01 ms |
| Buff renderer | 0.01 ms |
| Foliage | 1.47 ms |

## Stress benchmark

The benchmark warms up for 120 frames, then measures 600 frames at a fixed
simulation step of 1/60 second. It uses 50 active patroller enemies and 500
long-lived sword particles. `clock.tick()` is intentionally excluded because
its frame limiter sleeps to enforce the target FPS.

| Section | Average | P95 | Maximum |
| --- | ---: | ---: | ---: |
| Input | 0.02 ms | 0.02 ms | 0.18 ms |
| Enemy updates | 6.00 ms | 8.04 ms | 12.55 ms |
| Complete update | 7.43 ms | 9.62 ms | 13.92 ms |
| Rendering | 1.39 ms | 2.17 ms | 2.46 ms |
| Present | 0.29 ms | 0.46 ms | 0.72 ms |
| Complete CPU frame | 9.16 ms | 11.64 ms | 15.48 ms |

The 60 FPS CPU budget is 16.67 ms. The measured CPU-frame P95 is 11.64 ms,
so this scenario passes the defined P95 target with an uncapped throughput of
109.1 FPS. None of the 600 measured frames exceeded the CPU budget; the maximum
was 15.48 ms.

This headless result verifies the game's CPU-side update and software-rendering
workload. It does not measure a real display driver's presentation latency,
VSync, or monitor behavior. Use `python main.py --profile` for a final check on
the target gameplay machine.
