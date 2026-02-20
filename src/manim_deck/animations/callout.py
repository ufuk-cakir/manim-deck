"""Highlight / callout animation module.

Creates a rounded panel with a title and body text — useful for
key takeaways, definitions, or theorems in a research talk.

Usage
-----
>>> from manim_deck.animations.callout import CalloutModule
>>> CalloutModule(slide, title="Key Result", body="We achieve 95% accuracy.").run()
"""

from __future__ import annotations

from manim import *


class CalloutModule:
    """Animated callout / highlight box."""

    def __init__(
        self,
        slide,
        *,
        title: str,
        body: str,
        accent: str = "#A4E786",
        width: float = 9.0,
        position=ORIGIN,
    ):
        self.slide = slide
        self.title = title
        self.body = body
        self.accent = accent
        self.width = width
        self.position = position

    def run(self):
        s = self.slide

        title = Text(self.title, font_size=30, color=self.accent, weight=BOLD)
        body = Text(self.body, font_size=24, color=WHITE, line_spacing=1.3)
        content = VGroup(title, body).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        bg = RoundedRectangle(
            width=self.width,
            height=content.height + 0.8,
            corner_radius=0.2,
            fill_color="#1E3A35",
            fill_opacity=0.9,
            stroke_color=self.accent,
            stroke_width=1.5,
        )
        content.move_to(bg)
        group = VGroup(bg, content).move_to(self.position)

        s.play(FadeIn(bg, scale=0.95), run_time=0.4)
        s.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.3)
        s.play(FadeIn(body, shift=DOWN * 0.1), run_time=0.3)

        self.mobject = group
