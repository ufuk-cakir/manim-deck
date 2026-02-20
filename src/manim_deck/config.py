"""Configuration loader for manim_deck defaults."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib


@dataclass(frozen=True)
class SlideDeckDefaults:
    """Default values loaded from manim_deck.toml."""

    author: str = ""
    email: str = ""


def load_defaults(config_path: Path | None = None) -> SlideDeckDefaults:
    """Load defaults from manim_deck.toml in the current working directory."""

    if config_path is None:
        config_path = Path.cwd() / "manim_deck.toml"

    if not config_path.is_file():
        return SlideDeckDefaults()

    try:
        data = tomllib.loads(config_path.read_text(encoding="utf-8"))
    except Exception:
        return SlideDeckDefaults()

    if not isinstance(data, dict):
        return SlideDeckDefaults()

    defaults = data.get("defaults", {})
    if not isinstance(defaults, dict):
        return SlideDeckDefaults()

    author = defaults.get("author")
    email = defaults.get("email")

    return SlideDeckDefaults(
        author=str(author) if author is not None else "",
        email=str(email) if email is not None else "",
    )
