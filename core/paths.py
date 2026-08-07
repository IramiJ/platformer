from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ASSETS_DIR = PROJECT_ROOT / "assets"


def normalize_asset_path(relative_path: str | Path) -> Path:
    path = Path(relative_path)

    if path.parts and path.parts[0] == "assets":
        return Path(*path.parts[1:])

    return path


def assets_path(relative_path: str | Path) -> Path:
    return ASSETS_DIR / normalize_asset_path(relative_path)


def validate_asset_path(relative_path: str | Path) -> bool:
    return assets_path(relative_path).exists()


def require_asset_file(relative_path: str | Path) -> Path:
    path = assets_path(relative_path)

    if not path.is_file():
        raise FileNotFoundError(f"Missing asset file: {path}")

    return path


def require_asset_dir(relative_path: str | Path) -> Path:
    path = assets_path(relative_path)

    if not path.is_dir():
        raise FileNotFoundError(f"Missing asset directory: {path}")

    return path
