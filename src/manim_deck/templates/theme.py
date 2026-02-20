"""Themes for slide presentations.

A Theme is a simple dataclass holding all visual constants. Pass one to
TemplateSlide to change the look of your entire deck in one place.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class Theme:
    """Visual theme for a slide deck.

    Attributes:
        name:       Human-readable label (for debugging / logs).
        bg:         Background hex colour.
        panel:      Panel / card background hex colour.
        accent:     Accent colour used for headings, highlights, progress bar.
        text:       Default body-text colour.
        font:       Default font family (empty string = Manim default).
        title_size: Font size for title slides.
        heading_size: Font size for section / slide headings.
        body_size:  Font size for body text and bullets.
        code_font:  Font family for code blocks.
    """

    name: str = "custom"
    bg: str = "#0B1E1A"
    panel: str = "#1E3A35"
    accent: str = "#A4E786"
    text: str = "#FFFFFF"
    font: str = ""
    title_size: int = 80
    heading_size: int = 48
    body_size: int = 36
    code_font: str = "Monospace"


# ── Built-in themes

DARK_THEME = Theme(
    name="dark",
    bg="#0B1E1A",
    panel="#1E3A35",
    accent="#A4E786",
    text="#FFFFFF",
)

LIGHT_THEME = Theme(
    name="light",
    bg="#F5F5F0",
    panel="#E8E8E0",
    accent="#2D6A4F",
    text="#1A1A1A",
)
