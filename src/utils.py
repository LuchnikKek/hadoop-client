import logging
from pathlib import Path


def concat_path(path: str | Path, additional_path: str | Path) -> Path:
    """Concat Path or Path-like-string to new absolute path."""
    new_p = Path(path, additional_path).resolve()
    return new_p
