"""Feedforward network animation module.

Draws a layered network (neurons as circles, weights as lines), then sends
a pulse through it layer by layer to illustrate a forward pass.

Usage
-----
>>> from manim_deck.animations.neural_net import NeuralNetModule
>>> NeuralNetModule(slide, layers=(3, 8, 8, 1)).run()
"""

from __future__ import annotations

from manim import *


class NeuralNetModule:
    """Draws and animates a simple feedforward network."""

    def __init__(
        self,
        slide,
        *,
        layers: tuple[int, ...] = (4, 6, 6, 2),
        labels: tuple[str, ...] | None = None,
        accent: str = "#A4E786",
        layer_gap: float = 2.8,
        neuron_gap: float = 0.68,
        radius: float = 0.19,
        forward_pass: bool = True,
    ):
        self.slide = slide
        self.layers = layers
        self.labels = labels
        self.accent = accent
        self.layer_gap = layer_gap
        self.neuron_gap = neuron_gap
        self.radius = radius
        self.forward_pass = forward_pass

    def run(self):
        s = self.slide
        text_color = getattr(getattr(s, "theme", None), "text", WHITE)

        columns = VGroup()
        for n in self.layers:
            col = VGroup(
                *[
                    Circle(
                        radius=self.radius,
                        stroke_color=text_color,
                        stroke_width=2,
                        fill_color=text_color,
                        fill_opacity=0.0,
                    )
                    for _ in range(n)
                ]
            ).arrange(DOWN, buff=self.neuron_gap - 2 * self.radius)
            columns.add(col)
        columns.arrange(RIGHT, buff=self.layer_gap - 2 * self.radius).move_to(ORIGIN)

        edges = VGroup()
        for left, right in zip(columns[:-1], columns[1:]):
            group = VGroup(
                *[
                    Line(
                        a.get_right(),
                        b.get_left(),
                        stroke_color=text_color,
                        stroke_width=1,
                        stroke_opacity=0.35,
                    )
                    for a in left
                    for b in right
                ]
            )
            edges.add(group)

        s.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in columns], lag_ratio=0.2),
            run_time=1.0,
        )
        s.play(
            LaggedStart(*[Create(e) for e in edges], lag_ratio=0.3),
            run_time=1.2,
        )

        if self.labels:
            names = VGroup(
                *[
                    Text(lbl, font_size=22, color=text_color).next_to(col, DOWN, buff=0.35)
                    for lbl, col in zip(self.labels, columns)
                ]
            )
            s.play(FadeIn(names), run_time=0.5)

        if self.forward_pass:
            s.next_slide()
            s.play(columns[0].animate.set_fill(self.accent, opacity=1.0), run_time=0.3)
            for group, col in zip(edges, columns[1:]):
                s.play(
                    ShowPassingFlash(
                        group.copy().set_stroke(self.accent, width=3, opacity=1.0),
                        time_width=0.6,
                    ),
                    run_time=0.6,
                )
                s.play(col.animate.set_fill(self.accent, opacity=1.0), run_time=0.25)

        self.mobject = VGroup(columns, edges)
