from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ASSETS_DIR = PROJECT_ROOT / "assets"

def assets_path(relative_path: str) -> Path:
    return Path(ASSETS_DIR / relative_path)
