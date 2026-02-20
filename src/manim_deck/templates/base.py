"""Base TemplateSlide class for Manim Slides research presentations.

Inherit from TemplateSlide and override `section_titles` and `construct()`
to build your deck.  All visual constants come from a Theme object so you
can restyle your entire presentation in one line.

Example
-------
>>> from manim_deck import TemplateSlide
>>> from manim_deck.templates import DARK_THEME
>>>
>>> class MyTalk(TemplateSlide):
...     section_titles = ["Intro", "Method", "Results", "Conclusion"]
...     def construct(self):
...         self.title_slide("My Great Talk", occasion="NeurIPS 2025")
...         self.section_slide(1, "Intro")
...         self.list_slide("Contributions", ["Point A", "Point B"])
"""

from __future__ import annotations

from manim import * # noqa: F401
from manim_slides import Slide 
from manim.utils.color import ManimColor

from manim_deck.config import load_defaults
from manim_deck.templates.theme import Theme, DARK_THEME

DEFAULT_RUN_TIME = 0.9


class TemplateSlide(Slide):
    """Reusable base class for Manim Slides presentations.

    Class attributes to override in your subclass:
        section_titles : list[str]   — ordered section names for the progress bar.
        author         : str         — your name (shown on title slide footer).
        email          : str         — your email (available for custom slides).
        theme          : Theme       — visual theme (defaults to DARK_THEME).
    """

    section_titles: list[str] = []
    author: str = ""
    email: str = ""
    theme: Theme = DARK_THEME

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        defaults = load_defaults()
        if not self.author:
            self.author = defaults.author
        if not self.email:
            self.email = defaults.email
        self.camera.background_color = ManimColor(self.theme.bg)
        self.slide_counter = 0
        self.wait_time_between_slides = 0.1
        self.current_section: int = 0

    # ── internal helpers 

    def _show_slide_count(self):
        """Display the current slide number in the bottom-left corner."""
        num = Text(str(self.slide_counter), font_size=24, color=self.theme.text)
        num.to_corner(DL, buff=0.5)
        self.add(num)

    def _anim(self, mobject, text_anim=None):
        """Return an animation for *mobject*.  Defaults to FadeIn."""
        if text_anim is None:
            text_anim = FadeIn
        return text_anim(mobject)

    # ── canvas management

    def update_canvas(self, show_slide_count: bool = True):
        """Advance to a new slide, clear the stage, bump the counter."""
        self.next_slide()
        self.clear()
        self.slide_counter += 1
        if show_slide_count:
            self._show_slide_count()

    # ── slide types

    def title_slide(
        self,
        title_text: str,
        *,
        logos: list[str] | None = None,
        occasion: str = "",
        run_time: float = DEFAULT_RUN_TIME,
        scale_title: float = 1.0,
        scale_occasion: float = 1.0,
        text_anim=None,
    ):
        """Full-width title slide with optional logos and occasion line."""
        self.next_slide()
        self.clear()

        t = self.theme

        if logos:
            logo_group = (
                Group(*[ImageMobject(p).set_height(1) for p in logos])
                .arrange(RIGHT, buff=1)
                .to_corner(UR)
            )
            self.play(FadeIn(logo_group), run_time=run_time)

        title = (
            Text(title_text, font_size=t.title_size, color=t.accent)
            .move_to(ORIGIN)
            .scale(scale_title)
        )
        self.play(self._anim(title, text_anim), run_time=run_time)

        if self.author or occasion:
            parts = [p for p in (self.author, occasion) if p]
            footer = (
                Text(" — ".join(parts), font_size=t.body_size, color=t.text)
                .to_edge(DOWN)
                .scale(scale_occasion)
            )
            self.play(self._anim(footer, text_anim), run_time=run_time)

        self.wait()

    def section_slide(
        self,
        number: int,
        text: str,
        *,
        write_num: bool = False,
        run_time: float = DEFAULT_RUN_TIME,
        text_anim=None,
    ):
        """Full-screen section divider with progress bar."""
        self.update_canvas(show_slide_count=False)
        t = self.theme

        num_mob = (
            Text(str(number), font_size=144, color=t.accent)
            if write_num
            else VGroup()
        )
        title = Text(text, font_size=72, color=t.accent)
        if write_num:
            title.next_to(num_mob, DOWN)
        else:
            title.move_to(ORIGIN)

        footer = self.get_progress_mobject(number)
        self.play(
            self._anim(num_mob, text_anim),
            self._anim(title, text_anim),
            FadeIn(footer, shift=UP * 0.2),
            run_time=run_time,
        )
        self.current_section = number

    def statement_slide(
        self,
        statement_text: str | Mobject,
        *,
        add_footer: bool = False,
        run_time: float = DEFAULT_RUN_TIME,
        text_anim=None,
    ):
        """Centred statement — pass a string or a pre-built Mobject."""
        self.update_canvas()
        t = self.theme

        if isinstance(statement_text, str):
            statement = Text(
                statement_text, font_size=42, color=t.text
            ).move_to(ORIGIN)
        else:
            statement = statement_text.move_to(ORIGIN)

        self.current_statement_text = statement

        footer = (
            self.get_progress_mobject(self.current_section) if add_footer else VGroup()
        )
        self.play(
            self._anim(statement, text_anim),
            FadeIn(footer, shift=UP * 0.2),
            run_time=run_time,
        )

    def fade_statement(self, run_time: float = DEFAULT_RUN_TIME):
        """Fade out the last statement shown by `statement_slide`."""
        if hasattr(self, "current_statement_text") and self.current_statement_text:
            self.play(FadeOut(self.current_statement_text), run_time=run_time)
            self.current_statement_text = None

    def text_slide(
        self,
        title_text: str,
        body_lines: list[str],
        *,
        add_footer: bool = False,
        run_time: float = DEFAULT_RUN_TIME,
        text_anim=None,
    ):
        """Heading + paragraph body."""
        self.update_canvas()
        t = self.theme

        header = Text(title_text, font_size=60, color=t.accent).to_edge(UP)
        body = Paragraph(
            *body_lines, font_size=t.body_size, color=t.text
        ).next_to(header, DOWN, buff=0.7)

        footer = (
            self.get_progress_mobject(self.current_section) if add_footer else VGroup()
        )
        self.play(
            self._anim(header, text_anim),
            self._anim(body, text_anim),
            FadeIn(footer, shift=UP * 0.2),
            run_time=run_time,
        )

    def list_slide(
        self,
        title_text: str,
        items: list[str],
        *,
        add_footer: bool = False,
        run_time: float = DEFAULT_RUN_TIME,
        lagged_start: bool = True,
        text_anim=None,
    ):
        """Heading + bulleted list, optionally revealed one-by-one."""
        self.update_canvas()
        t = self.theme

        header = Text(title_text, font_size=t.heading_size, color=t.accent).to_corner(
            UL, buff=1.5
        )
        bullets = (
            BulletedList(*items, font_size=t.body_size, buff=0.3)
            .set_color(t.text)
            .next_to(header, DOWN, buff=1.5)
            .to_edge(LEFT, buff=1.5)
        )
        footer = (
            self.get_progress_mobject(self.current_section) if add_footer else VGroup()
        )

        if lagged_start:
            self.play(self._anim(header, text_anim), run_time=run_time)
            for bullet in bullets:
                self.play(self._anim(bullet, text_anim), run_time=run_time)
                self.next_slide()
        else:
            self.play(
                self._anim(header, text_anim),
                self._anim(bullets, text_anim),
                FadeIn(footer, shift=UP * 0.2),
                run_time=run_time,
            )

    def image_slide(
        self,
        title_text: str,
        image_path: str,
        *,
        image_height: float = 5.0,
        caption: str = "",
        add_footer: bool = False,
        run_time: float = DEFAULT_RUN_TIME,
        text_anim=None,
    ):
        """Heading + centred image with optional caption."""
        self.update_canvas()
        t = self.theme

        header = Text(title_text, font_size=t.heading_size, color=t.accent).to_edge(UP)
        img = ImageMobject(image_path).set_height(image_height)

        group = VGroup(img)
        if caption:
            cap = Text(caption, font_size=24, color=t.text).next_to(img, DOWN, buff=0.2)
            group.add(cap)
        group.next_to(header, DOWN, buff=0.5)

        footer = (
            self.get_progress_mobject(self.current_section) if add_footer else VGroup()
        )
        self.play(
            self._anim(header, text_anim),
            FadeIn(group),
            FadeIn(footer, shift=UP * 0.2),
            run_time=run_time,
        )

    def code_slide(
        self,
        title_text: str,
        code: str,
        *,
        language: str = "python",
        font_size: int = 18,
        run_time: float = DEFAULT_RUN_TIME,
        text_anim=None,
    ):
        """Heading + syntax-highlighted code block."""
        self.update_canvas()
        t = self.theme

        header = Text(title_text, font_size=t.heading_size, color=t.accent).to_edge(UP)
        code_block = Code(
            code_string=code,
            language=language,
            background="window",
            add_line_numbers=True,
            paragraph_config={"font_size": font_size},
        ).next_to(header, DOWN, buff=0.5)

        self.play(
            self._anim(header, text_anim),
            FadeIn(code_block),
            run_time=run_time,
        )

    def two_column_slide(
        self,
        title_text: str,
        left: Mobject,
        right: Mobject,
        *,
        add_footer: bool = False,
        run_time: float = DEFAULT_RUN_TIME,
        text_anim=None,
    ):
        """Heading + two side-by-side content areas."""
        self.update_canvas()
        t = self.theme

        header = Text(title_text, font_size=t.heading_size, color=t.accent).to_edge(UP)
        columns = VGroup(left, right).arrange(RIGHT, buff=1.0).next_to(header, DOWN, buff=0.6)

        footer = (
            self.get_progress_mobject(self.current_section) if add_footer else VGroup()
        )
        self.play(
            self._anim(header, text_anim),
            FadeIn(columns),
            FadeIn(footer, shift=UP * 0.2),
            run_time=run_time,
        )

    # ── progress bar

    def get_progress_mobject(
        self, current_section_num: int, *, add_label: bool = False
    ) -> VGroup:
        """Build a footer progress-bar Mobject (does NOT add it to scene)."""
        t = self.theme
        titles = self.section_titles
        n = len(titles)
        if n == 0:
            return VGroup()

        y = -self.camera.frame_height / 2 + 0.5
        start_x = -self.camera.frame_width / 2 + 1.5
        end_x = self.camera.frame_width / 2 - 1.5
        step = (end_x - start_x) / (n - 1) if n > 1 else 0

        idx = max(0, current_section_num - 1)
        cx = start_x + step * idx

        line_before = Line(
            [start_x, y, 0], [cx, y, 0], stroke_color=t.text, stroke_width=2 
        )
        line_after = Line(
            [cx, y, 0], [end_x, y, 0], stroke_color=t.text, stroke_width=2
        ).set_opacity(0.3)

        dots = VGroup()
        labels = VGroup()
        for i, title in enumerate(titles):
            x = start_x + step * i
            dot = Circle(
                radius=0.08,
                stroke_color=t.text,
                fill_color=t.text,
                fill_opacity=1.0,
            ).move_to([x, y, 0])

            if i == idx:
                dot.set_color(t.accent).scale(1.5)
                if add_label:
                    lbl = Text(title, font_size=24, color=t.accent).next_to(
                        dot, UP, buff=0.15
                    )
                    labels.add(lbl)
            elif i > idx:
                dot.set_opacity(0.3)
            dots.add(dot)

        return VGroup(line_before, line_after, dots, labels)
