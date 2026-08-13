# TODO

## 1. Stabilize the complete game flow

- [x] Define one central `TILE_SIZE = 24` constant.
- [x] Replace every hard-coded 16/24 tile conversion with `TILE_SIZE`.
- [x] Use one coordinate convention for player spawns, enemies, checkpoints, texts, torches, camera limits, minimap data, and level exits.
- [x] Migrate all level JSON files to the unified coordinate convention.
- [x] Replace single-point level exits with rectangular trigger zones.
- [x] Add a validated level schema with required fields and useful error messages.
- [x] Add the missing `texts` field to level 3.
- [x] Make all level files use the same fields and data types.
- [x] Replace the bare `except` in the level transition logic with specific exception handling.
- [x] Clamp minimap reads to the map boundaries and render out-of-bounds cells as empty tiles.
- [x] Reset bullets, arrows, sparks, movement, momentum, cooldowns, and temporary state on level reload and transition.
- [x] Load and render torches and chandeliers correctly on the first level and after transitions, or remove the unused system.
- [x] Fix the double-coin buff and reward multiple enemy deaths correctly.
- [x] Manually complete all levels from start to finish without errors.

## 2. Make the game loop deterministic and testable

- [x] Add an `if __name__ == __main__:` entry-point guard.
- [x] Make every production module importable without starting the game or opening a window.
- [x] Separate state updates from rendering.
- [x] Move animation, cooldown, damage-flash, particle, and cleanup updates out of render methods.
- [x] Use seconds consistently for delta time, cooldowns, stun durations, buffs, and animations.
- [x] Stop removing bullets, arrows, coins, and particles while iterating over their lists.
- [x] Introduce an explicit alive/dead lifecycle and filter collections after updates.
- [x] Add a central level/session reset method.
- [x] Ensure pause, shop, death, and win overlays stop only the intended systems.

## 3. Fix broken and fragile modules

- [x] Import `Patroller` directly in `heavy_patroller.py` and remove the circular import.
- [x] Remove or repair the broken `player_movements.py` module.
- [x] Remove or convert `ui/test.py` into an automated test.
- [x] Move the interactive tree prototype from `tests/` to `experiments/` or remove it.
- [x] Move foliage images from `tests/tree_test/` to `assets/foliage/`.
- [x] Resolve asset and configuration paths relative to the project instead of the current working directory.
- [x] Validate enemy names, keybinds, shop entries, maps, and referenced asset paths when loading data.

## 4. Add automated quality checks

- [x] Create a `pyproject.toml` with runtime and development dependencies.
- [x] Configure pytest.
- [x] Configure Ruff for linting and formatting.
- [x] Add tests for tile-coordinate conversion.
- [x] Add tests for level schema validation and loading.
- [x] Add tests for all level transitions and the final win state.
- [x] Add tests for collision resolution.
- [x] Add minimap boundary tests.
- [x] Add tests for projectile and particle cleanup.
- [x] Add tests for shop purchases, buff duration, and double-coin rewards.
- [x] Add tests for level/session resets.
- [x] Add a headless game-start smoke test.
- [x] Add a GitHub Actions workflow that runs formatting checks, linting, and tests.
- [x] Keep the test suite green on the supported Python versions.

## 5. Clean up the codebase

- [x] Rename classes, files, methods, and constants consistently according to PEP 8.
- [x] Replace wildcard imports with explicit imports.
- [x] Split combined imports into individual lines.
- [x] Stop shadowing built-ins such as `map` and `dict`.
- [x] Remove commented-out implementations and dead code.
- [x] Remove unused systems or integrate them completely.
- [x] Remove or archive `*_old` assets, old maps, sketches, and unused editor-session files.
- [x] Add type hints to core data structures and public methods.
- [x] Add short docstrings to the main game, level, entity, collision, and rendering systems.
- [x] Normalize Git author information and add a `.mailmap` if needed.

## 6. Measure and improve performance

- [x] Add a shared asset cache for images, fonts, and animations.
- [x] Preload leaf surfaces instead of loading an image for every spawned leaf.
- [x] Load shop and HUD images once instead of during rendering.
- [x] Reuse render surfaces where possible instead of allocating them every frame.
- [x] Profile frame time, rendering, entity updates, and asset loading.
- [x] Record before/after measurements for every claimed optimization.
- [x] Verify stable gameplay at the target frame rate with multiple enemies and particles active.

## 7. Prepare the repository for applications

- [ ] Choose a distinctive project name and one-sentence pitch.
- [ ] Update the README feature list to match the implemented game.
- [ ] Remove completed features from the planned-improvements section.
- [ ] Add a controls table for keyboard and mouse input.
- [ ] Document installation with a virtual environment and `requirements.txt` or `pyproject.toml`.
- [ ] Document the supported Python version and tested operating systems.
- [ ] Place a short polished gameplay GIF directly below the README introduction.
- [ ] Capture clean screenshots of movement, combat, the shop, and a level transition.
- [ ] Add a small architecture diagram.
- [ ] Add a section describing important design decisions and trade-offs.
- [ ] Link to representative code for the game loop, level system, enemy registry, collisions, and tile culling.
- [ ] Replace unverified performance claims with measured results.
- [ ] Add project status, development period, personal responsibilities, and key learnings.
- [ ] Add a license for the source code.
- [ ] Verify and document the ownership and license of every included asset.
- [ ] Remove any asset whose origin or usage rights are unclear.
- [ ] Add test and CI badges after the workflow is passing.
- [ ] Create a downloadable release and verify it on a clean machine.
- [ ] Publish the build on GitHub Releases or itch.io.
- [x] Merge the stabilized `feature/rework` branch into the default `main` branch.
- [ ] Tag the recruiter-ready version as the first public release.
