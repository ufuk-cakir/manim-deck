"""Pipeline diagram animation module.

Draws a horizontal pipeline of labelled boxes connected by arrows, then
optionally pulses through them one-by-one to illustrate data flow.

Usage
-----
>>> from manim_deck.animations.pipeline import PipelineModule
>>> PipelineModule(slide, steps=["Data", "Model", "Train", "Evaluate"]).run()
"""

from __future__ import annotations

from manim import *


class PipelineModule:
    """Animated left-to-right pipeline."""

    def __init__(
        self,
        slide,
        *,
        steps: list[str],
        colors: list[str] | None = None,
        box_width: float = 1.8,
        box_height: float = 1.0,
        pulse: bool = True,
    ):
        self.slide = slide
        self.steps = steps
        self.colors = colors or [BLUE, GREEN, YELLOW, RED, TEAL, ORANGE][: len(steps)]
        self.box_width = box_width
        self.box_height = box_height
        self.pulse = pulse

    def run(self):
        s = self.slide
        boxes = VGroup()
        for label, col in zip(self.steps, self.colors):
            box = RoundedRectangle(
                width=self.box_width,
                height=self.box_height,
                corner_radius=0.15,
                fill_color=col,
                fill_opacity=0.2,
                stroke_color=col,
            )
            txt = Text(label, font_size=22, color=WHITE)
            boxes.add(VGroup(box, txt))
        boxes.arrange(RIGHT, buff=1.0)

        arrows = VGroup()
        for i in range(len(boxes) - 1):
            arr = Arrow(
                boxes[i][0].get_right(),
                boxes[i + 1][0].get_left(),
                color=WHITE,
                buff=0.1,
                stroke_width=2,
            )
            arrows.add(arr)

        s.play(
            LaggedStart(*[FadeIn(b, shift=UP * 0.3) for b in boxes], lag_ratio=0.15),
            run_time=1.0,
        )
        s.play(
            LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15),
            run_time=0.6,
        )

        if self.pulse:
            for box in boxes:
                s.play(
                    box[0].animate.set_fill(opacity=0.6).set_stroke(width=4),
                    run_time=0.25,
                )
                s.next_slide()
                s.play(
                    box[0].animate.set_fill(opacity=0.2).set_stroke(width=2),
                    run_time=0.25,
                )
