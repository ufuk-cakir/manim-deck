"""Example presentation using manim_deck.

Render:  manim-slides render talks/example-talk/main.py ExampleTalk
Present: manim-slides ExampleTalk
"""

from manim import *
from manim_deck import TemplateSlide
from manim_deck.templates import DARK_THEME
from manim_deck.animations.pipeline import PipelineModule
from manim_deck.animations.callout import CalloutModule


class ExampleTalk(TemplateSlide):
    # ── configuration ────────────────────────────────────
    section_titles = ["Introduction", "Method", "Results", "Conclusion"]
    theme = DARK_THEME

    def construct(self):
        # Title
        self.title_slide(
            "My Research Talk",
            occasion="Lab Meeting",
        )

        # Section 1
        self.section_slide(1, "Introduction")

        self.statement_slide("Why does this problem matter?")

        self.list_slide(
            "Motivation",
            [
                "Existing methods fail under uncertainty",
                "Real-world decisions require fast inference",
                "We propose a new framework",
            ],
        )

        # Section 2
        self.section_slide(2, "Method")

        # Reusable pipeline animation
        self.update_canvas()
        PipelineModule(
            self,
            steps=["Environment", "Agent", "Policy", "Reward"],
        ).run()
        self.next_slide()

        self.code_slide(
            "Implementation",
            code='''import jax
import jax.numpy as jnp

def policy(params, obs):
    """Simple policy network."""
    x = jnp.tanh(obs @ params["w1"])
    return jnp.softmax(x @ params["w2"])''',
        )

        # Section 3
        self.section_slide(3, "Results")

        self.update_canvas()
        CalloutModule(
            self,
            title="Key Finding",
            body="Our approach achieves 2x faster convergence\nwith 30% fewer parameters.",
        ).run()
        self.next_slide()

        # Section 4
        self.section_slide(4, "Conclusion")

        self.list_slide(
            "Summary",
            [
                "We introduced X",
                "We showed Y improves Z",
                "Code available at github.com/...",
            ],
        )

        self.statement_slide("Questions?")
