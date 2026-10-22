"""Scenes behind the animations in the README.

The crash-course scenes (Mobjects, Animations, Positioning, MyScene) and
MyPresentation are printed in full in README.md: change a scene here and its
copy there together. `docs/make_clips.py` renders the scenes and writes
`docs/assets/<name>.webp`.

Render one by hand:  uv run manim render -ql docs/readme_clips.py Animations
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

from manim import *
from manim_slides import Slide

from manim_deck import TemplateSlide
from manim_deck.templates import DARK_THEME, LIGHT_THEME, Theme
from manim_deck.animations.pipeline import PipelineModule
from manim_deck.animations.callout import CalloutModule
from manim_deck.animations.neural_net import NeuralNetModule
from manim_deck.animations.custom.cellular_automata import WildfireCAExplanationModule

MONO = "Menlo"


class Clip:
    """Mixin for README clips.

    A clip has no clicks, so every `next_slide()` becomes a hold. With
    `show_key = True` the hold shows a small "→ next_slide()" key that is
    pressed when the slide would advance.
    """

    hold = 1.0
    end_hold = 1.5
    show_key = False

    def next_slide(self, *args, **kwargs):
        if self.mobjects:
            if self.show_key:
                self._press_key()
            else:
                self.wait(self.hold)
        super().next_slide(*args, **kwargs)

    def tear_down(self):
        self.wait(self.end_hold)
        super().tear_down()

    def _press_key(self):
        color = getattr(getattr(self, "theme", None), "text", WHITE)
        cap = RoundedRectangle(
            width=0.62,
            height=0.5,
            corner_radius=0.1,
            stroke_color=color,
            stroke_width=2,
            stroke_opacity=0.6,
        )
        arrow = Text("→", font_size=24, color=color, fill_opacity=0.6).move_to(cap)
        key = VGroup(cap, arrow)
        label = Text("next_slide()", font=MONO, font_size=18, color=color, fill_opacity=0.6)
        badge = VGroup(key, label).arrange(LEFT, buff=0.2).to_corner(UR, buff=0.35)
        self.play(FadeIn(badge), run_time=0.2)
        self.wait(max(self.hold - 0.55, 0.1))
        self.play(key.animate.scale(0.82), rate_func=there_and_back, run_time=0.25)
        self.remove(badge)


# ── Core Manim concepts ─────────────────────────────────────────


class Mobjects(Scene):
    def construct(self):
        circle = Circle(radius=1, color=BLUE)
        label = Text("Hello", font_size=36)
        eq = MathTex(r"E = mc^2")
        arrow = Arrow(LEFT, RIGHT)

        row = VGroup(circle, label, eq, arrow)
        row.arrange(RIGHT, buff=1)
        for mob in row:
            self.play(FadeIn(mob, shift=UP))
        self.wait()


class Animations(Scene):
    def construct(self):
        circle = Circle(color=BLUE, fill_opacity=0.3)
        circle.shift(LEFT * 1.5)
        square = Square(side_length=2, color=GREEN)
        square.set_fill(GREEN, opacity=0.3)
        square.shift(RIGHT * 1.5)

        self.play(Create(circle))
        self.play(circle.animate.shift(RIGHT * 3))
        self.play(Transform(circle, square))
        self.play(FadeOut(circle))
        self.wait()


class Positioning(Scene):
    def construct(self):
        other = Square(color=GRAY).shift(LEFT * 4)
        mob = Square(side_length=0.8, color=YELLOW)
        mob.shift(UP + LEFT)
        self.add(other, mob)

        self.play(mob.animate.move_to(ORIGIN))
        self.play(mob.animate.to_edge(UP))
        self.play(mob.animate.to_corner(UR))
        self.play(mob.animate.shift(LEFT * 2))
        self.play(mob.animate.next_to(other, RIGHT))
        self.wait()


class MyScene(Scene):
    def construct(self):
        sq = Square(color=GREEN)
        self.play(Create(sq))
        self.play(sq.animate.rotate(PI / 4))
        self.wait()


# ── Manim Slides ────────────────────────────────────────────────


class MyPresentation(Clip, Slide):
    show_key = True
    hold = 1.4

    def construct(self):
        title = Text("Hello!")
        self.play(Write(title))

        self.next_slide()  # pause here

        self.play(FadeOut(title))
        conclusion = Text("Thanks!")
        self.play(FadeIn(conclusion))


# ── manim_deck ──────────────────────────────────────────────────


class MyConferenceTalk(Clip, TemplateSlide):
    show_key = True
    section_titles = ["Motivation", "Method", "Experiments", "Conclusion"]
    author = "Your Name"
    theme = DARK_THEME

    def construct(self):
        self.title_slide("My Paper Title", occasion="ICML 2026")

        self.section_slide(1, "Motivation")
        self.statement_slide("Current methods struggle with X.")
        self.list_slide(
            "Challenges",
            [
                "Challenge A is hard because ...",
                "Challenge B remains unsolved",
                "We need a new approach",
            ],
        )

        self.section_slide(2, "Method")
        # ... your content here ...

        self.section_slide(4, "Conclusion")
        self.statement_slide("Questions?")


def _demo_image(path: str) -> str:
    """A small burn map as a PNG, standing in for a figure from a paper."""
    rng = np.random.default_rng(3)
    h, w = 24, 36
    y, x = np.mgrid[0:h, 0:w]
    fuel = rng.random((h, w)) < 0.8
    dist = np.hypot((x - 13) / 1.6, y - 12)          # an elongated burn scar
    colors = np.array([[22, 68, 40], [48, 120, 62], [62, 62, 62], [213, 94, 0]], np.uint8)
    cells = np.where(fuel, 1, 0)
    cells[dist < 8] = 2
    cells[(dist >= 7) & (dist < 8.2) & fuel] = 3
    rgb = colors[cells].repeat(12, axis=0).repeat(12, axis=1)
    Image.fromarray(rgb).save(path)
    return path


class SlideTypes(Clip, TemplateSlide):
    section_titles = ["Intro", "Method", "Results", "End"]
    author = "Your Name"
    hold = 1.1

    def construct(self):
        t = self.theme
        self.title_slide("title_slide", occasion="occasion")
        self.section_slide(1, "section_slide")
        self.statement_slide("statement_slide: one centred sentence", add_footer=True)
        self.list_slide("list_slide", ["One bullet per click", "Built from a list of strings"])
        self.text_slide(
            "text_slide",
            ["A heading and a paragraph.", "Each string is one line."],
            add_footer=True,
        )
        self.code_slide(
            "code_slide",
            code='def policy(params, obs):\n    x = jnp.tanh(obs @ params["w1"])\n    return jax.nn.softmax(x @ params["w2"])',
        )
        image = _demo_image(str(Path(config.media_dir) / "demo_field.png"))
        self.image_slide("image_slide", image, image_height=4.0, caption="any PNG or JPG")
        left = VGroup(
            Circle(radius=1.1, color=t.accent),
            Text("left", font_size=28, color=t.text),
        )
        right = VGroup(
            Square(side_length=2.2, color=t.accent),
            Text("right", font_size=28, color=t.text),
        )
        self.two_column_slide("two_column_slide", left, right, add_footer=True)


OXFORD_THEME = Theme(
    name="oxford",
    bg="#002147",
    panel="#0A3060",
    accent="#F0C808",
    text="#FFFFFF",
    heading_size=52,
    body_size=34,
)


class Themes(Clip, TemplateSlide):
    section_titles = ["Intro", "Method", "Results", "End"]
    hold = 1.6

    def construct(self):
        themes = [
            ("DARK_THEME", DARK_THEME),
            ("LIGHT_THEME", LIGHT_THEME),
            ('Theme(name="oxford", ...)', OXFORD_THEME),
        ]
        for i, (name, theme) in enumerate(themes):
            if i:
                self.next_slide()
                self.clear()
            self.theme = theme
            self.camera.background_color = ManimColor(theme.bg)
            self.current_section = 2
            self.list_slide(
                name,
                ["Same slide code", "Different theme"],
                lagged_start=False,
                add_footer=True,
            )


# ── Animation modules ───────────────────────────────────────────


class Pipeline(Clip, TemplateSlide):
    hold = 0.5

    def construct(self):
        self.update_canvas(show_slide_count=False)
        PipelineModule(self, steps=["Data", "Model", "Train", "Evaluate"]).run()


class Callout(Clip, TemplateSlide):
    end_hold = 2.5

    def construct(self):
        self.update_canvas(show_slide_count=False)
        CalloutModule(
            self,
            title="Key Finding",
            body="Our approach achieves 2x faster convergence\nwith 30% fewer parameters.",
        ).run()


class NeuralNet(Clip, TemplateSlide):
    hold = 0.6

    def construct(self):
        self.update_canvas(show_slide_count=False)
        NeuralNetModule(self, layers=(3, 8, 8, 1)).run()


class CellularAutomata(Clip, TemplateSlide):
    hold = 0.8

    def construct(self):
        self.update_canvas(show_slide_count=False)
        WildfireCAExplanationModule(self).run()


# ── The idea, for the top of the README ─────────────────────────


class Concept(Scene):
    """Python code -> one video per slide -> HTML, PDF, PowerPoint or a live window.

    Swiss grid, in the style of the author's IE 2026 talk: white paper, near-black
    ink, one green accent, Helvetica Neue in light weights. Three columns between
    the margins; every column hangs from the same top lines and is set flush left.
    """

    PAPER, INK, MUTED, FAINT, ACCENT = "#FFFFFF", "#161615", "#57554F", "#D9D6CE", "#3F7A22"
    FONT = "Helvetica Neue"
    LEFT, RIGHT, GUTTER = -6.48, 6.48, 0.6
    TITLE = 3.05     # top of the column titles
    COMMAND = 2.55   # top of the command under each title
    RULE = 2.1       # hairline under the column heads
    CONTENT = 1.65   # every column's content hangs from here
    CAPTION = -2.65  # top of the caption row

    def text(self, s, size, color=None, weight=NORMAL, font=None):
        # Set at twice the size and scaled down: small Manim text kerns badly.
        extra = {"line_spacing": 0.5} if "\n" in s else {}
        return Text(s, font=font or self.FONT, font_size=size * 2, weight=weight,
                    color=color or self.INK, **extra).scale(0.5)

    @staticmethod
    def hang(mob, x, top):
        return mob.move_to([x + mob.width / 2, top - mob.height / 2, 0])

    def head(self, x, name, command, width):
        title = self.hang(self.text(name, 32), x, self.TITLE)
        cmd = self.hang(self.text(command, 17, self.MUTED, font=MONO), x, self.COMMAND)
        rule = Line([x, self.RULE, 0], [x + width, self.RULE, 0], color=self.FAINT, stroke_width=1.5)
        return title, cmd, rule

    def show_head(self, parts):
        title, cmd, rule = parts
        self.play(FadeIn(title, shift=UP * 0.15), FadeIn(cmd), Create(rule), run_time=0.7)

    def construct(self):
        self.camera.background_color = ManimColor(self.PAPER)
        width = (self.RIGHT - self.LEFT - 2 * self.GUTTER) / 3
        xs = [self.LEFT + i * (width + self.GUTTER) for i in range(3)]

        # 1. the talk is Python code
        lines = ["self.play(Create(sq))", "self.next_slide()", "self.play(Rotate(sq))",
                 "self.next_slide()", "self.play(Write(txt))"]
        code = VGroup(*[
            self.text(l, 19, self.INK if i % 2 == 0 else self.ACCENT, font=MONO)
            for i, l in enumerate(lines)
        ])
        for i, line in enumerate(code):
            self.hang(line, xs[0], self.CONTENT - i * 0.52)
        caption1 = self.hang(self.text("Write the talk in Python.", 20, self.MUTED), xs[0], self.CAPTION)

        self.show_head(self.head(xs[0], "Manim", "talk.py", width))
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.15) for l in code], lag_ratio=0.2),
                  FadeIn(caption1), run_time=1.2)

        # 2. Manim Slides cuts it at every next_slide(): one video per slide
        frames, tags = VGroup(), VGroup()
        for k in range(3):
            frame = Rectangle(width=2.0, height=1.125, stroke_width=0,
                              fill_color="#F2F1ED", fill_opacity=1)
            self.hang(frame, xs[1], self.CONTENT - k * (1.125 + 0.3))
            tag = self.text(f"slide {k + 1}", 18, self.MUTED)
            self.hang(tag, frame.get_right()[0] + 0.3, frame.get_top()[1])
            frames.add(frame); tags.add(tag)
        caption2 = self.hang(self.text("Each slide gets rendered\ninto a video.", 20, self.MUTED), xs[1], self.CAPTION)
        marker = Rectangle(width=0.05, height=0.3, stroke_width=0, fill_color=self.ACCENT,
                           fill_opacity=1)

        self.show_head(self.head(xs[1], "Manim Slides", "manim-slides render", width))

        def square(frame):
            sq = Square(side_length=0.46, color=self.ACCENT, stroke_width=3)
            return sq.move_to(frame).shift(LEFT * 0.4)

        marker.move_to([xs[0] - 0.22, code[0].get_y(), 0])
        s1 = square(frames[0])
        self.play(FadeIn(marker), FadeIn(frames[0], tags[0]), run_time=0.45)
        self.play(Create(s1), run_time=0.7)

        s2 = square(frames[1])
        self.play(marker.animate.set_y(code[2].get_y()), FadeIn(frames[1], tags[1], s2), run_time=0.45)
        self.play(Rotate(s2, PI / 2), run_time=0.7)

        s3 = square(frames[2])
        hi = self.text("Hi!", 22).next_to(s3, RIGHT, buff=0.3)
        self.play(marker.animate.set_y(code[4].get_y()), FadeIn(frames[2], tags[2], s3), run_time=0.45)
        self.play(Write(hi), FadeIn(caption2), run_time=0.7)

        # 3. present it anywhere
        outputs = [("HTML", "Reveal.js, in any browser"), ("PDF", "one page per slide"),
                   ("PPTX", "PowerPoint"), ("Live", "manim-slides present")]
        rows = []
        for k, (name, what) in enumerate(outputs):
            top = self.CONTENT - k * 0.98
            label = self.hang(self.text(name, 24, self.ACCENT if k == 0 else self.INK), xs[2], top)
            desc = self.text(what, 16 if name == "Live" else 18, self.MUTED,
                             font=MONO if name == "Live" else None)
            self.hang(desc, xs[2], label.get_bottom()[1] - 0.14)
            rule = Line([xs[2], top - 0.78, 0], [xs[2] + width, top - 0.78, 0],
                        color=self.FAINT, stroke_width=1)
            rows.append(VGroup(label, desc, rule))
        caption3 = self.hang(self.text("Present!", 20, self.MUTED), xs[2], self.CAPTION)

        self.play(FadeOut(marker), run_time=0.3)
        self.show_head(self.head(xs[2], "Your talk", "manim-slides convert", width))
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.12) for r in rows], lag_ratio=0.2),
                  FadeIn(caption3), run_time=1.2)
        self.wait(3.5)
