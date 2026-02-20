# Manim Research Slides Template for Academic Presentations
**Ufuk Çakır**

This repository includes templates for making animated research presentations with
[Manim](https://www.manim.community/) and [Manim Slides](https://manim-slides.eertmans.be/).


> This repo gives you a reusable Python package (`manim_deck`) with
> pre-built slide templates and animation modules. You can fork, customise, and use it to
> build your next cool conference talk!


---

## Quick start

```bash
# 1. Clone (or fork) this repo
git clone https://github.com/ufuk-cakir/manim-deck.git
cd manim-deck

# 2. Install with uv (creates a venv automatically with python 3.11)
uv sync

# 3. Render the example talk
uv run manim-slides render talks/example-talk/main.py ExampleTalk

# 4. Present it
uv run manim-slides ExampleTalk
```

Have Fun!

> **⚠️ Note:** This template has not been extensively tested across all platforms and configurations. 
> If you encounter any issues or have questions, please feel free to [submit an issue on GitHub](https://github.com/ufuk-cakir/manim-deck/issues) or reach out directly. Contributions and feedback are very welcome!

---

## Project structure

```
manim-deck/
│
├── pyproject.toml              # Package definition (uv / pip)
├── README.md                  
│
├── src/
│   └── manim_deck/             # The importable package
│       ├── __init__.py
│       ├── templates/
│       │   ├── __init__.py
│       │   ├── base.py         # TemplateSlide is the core class
│       │   └── theme.py        # Theme dataclass + built-in themes
│       └── animations/         # Module to hold your reusable animation classes
│           ├── __init__.py
│           ├── pipeline.py     # Example: animated pipeline diagram
│           └── callout.py      # Example: highlight / callout box
│
└── talks/                      # A folder for your individual talks (not importable, just scripts)
    └── example-talk/
        ├── main.py             # The main script that holds your talk content
        └── images/             # Any images for this talk
```

**Key idea:** The `manim_deck` package holds everything reusable (templates,
themes, animation modules). Each talk in `talks/` is a standalone script that
imports from the package. When you build a cool new animation for one talk,
move it into `manim_deck/animations/` and it's available everywhere.

---

## Why Manim for research presentations?

If you ever watched a [3Blue1Brown](https://www.3blue1brown.com/) video, you have
what Manim can do!

**Why I think you should use it for academic presentations**

- **You want your audience to stay engaged.** Animated visuals keep your
  audience focused in ways that static bullet points can not do.
- **Step-by-step animations** let you build up complex ideas incrementally, and is
  perfect for explaining algorithms, architectures, or experimental pipelines, where you do not want to overwhelm your audience with all the details at once.
- **Building the animation forces you to think.** Translating your research
  into an animation sequence makes you distil the core message in a way that is accessible to a broad audience.
- **Everything is version-controlled.** Your slides are `.py` files, which makes it easy to track changes or revert to old versions.
- **PROGRAMMATIC.** Evyerthing is Python. Which means you can use for loops, functions, classes to build complex animations. You need to draw 50 boxes? Thats way easier with a loop than copy-pasting in PowerPoint. You want to reuse the same architecture diagram across multiple talks, but with different labels? A reusable animation module is perfect for that!!!

**The tradeoffs:**

- Steeper learning curve than drag-and-drop tools.
- Iteration is slower (render → check → tweak → re-render).
- Not great for last-minute slide reshuffling 5 minutes before your talk.



---

## Core Manim concepts (justcrash course)

This is by no means a comprehensive Manim tutorial! There are so many great resources out there to dive deeper, but this is just to get you started and familiar with the core concepts.

### 1. Mobjects (Mathematical Objects)

Everything on screen is a **Mobject**. Text, shapes, arrows, equations are all Python objects that have additional properties and methods.

```python
from manim import *

circle = Circle(radius=1, color=BLUE)
label  = Text("Hello", font_size=36)
eq     = MathTex(r"E = mc^2")
arrow  = Arrow(LEFT, RIGHT)
```

### 2. Animations

Animations **transform Mobjects over time**. You trigger them with `self.play()`.

```python
self.play(Create(circle))              # draw 
self.play(circle.animate.shift(RIGHT)) # move 
self.play(Transform(circle, square))   # morph 
self.play(FadeOut(circle))             # remove 
```

Common animations: `FadeIn`, `FadeOut`, `Create`, `Write`, `GrowArrow`,
`Transform`, `Rotate`, `LaggedStart`, `AnimationGroup`.

### 3. Positioning

```python
mob.move_to(ORIGIN)           # absolute position
mob.to_edge(UP)               # snap to edge
mob.to_corner(UR)             # snap to corner
mob.shift(LEFT * 2)           # relative move
mob.next_to(other, RIGHT)     # relative to another Mobject
```

### 4. Scenes

A **Scene** is the canvas. You subclass it and implement `construct()`:

```python
class MyScene(Scene):
    def construct(self):
        sq = Square(color=GREEN)
        self.play(Create(sq))
        self.play(sq.animate.rotate(PI / 4))
        self.wait()
```

Render with: `manim render my_file.py MyScene`

---

## From Manim to Manim Slides


Manim Slides extends Manim with a `Slide` class. The main new concept is
**`self.next_slide()`** which creates a pause point (like pressing the arrow key in
PowerPoint).

```python
from manim_slides import Slide

class MyPresentation(Slide):
    def construct(self):
        title = Text("Hello, A2I!")
        self.play(Write(title))

        self.next_slide()          # this creates a breakpoint in your presentation!

        self.play(FadeOut(title))
        conclusion = Text("Thanks!")
        self.play(FadeIn(conclusion))
```

### Rendering & presenting

```bash
# Render (generates animation frames)
manim-slides render presentation.py MyPresentation

# Present live (arrow keys / click to advance)
manim-slides MyPresentation

# Export to a self-contained HTML file (great for sharing)
manim-slides convert MyPresentation output.html --open

# Export to PDF (one image per slide)
manim-slides convert MyPresentation output.pdf
```

The HTML export uses **Reveal.js** under the hood, so you get keyboard
navigation, fullscreen mode, and speaker notes for free.


> **Personal Tip** I find that the live presentantion mode uses a lot of memory and crashes sometimes, so I prefer to export to HTML and present from the browser to be safe.

---

## Using the `manim_deck` template

### First steps

Create a new folder in `talks/` and a `main.py`:

```python
from manim import *
from manim_deck import TemplateSlide
from manim_deck.templates import DARK_THEME

class MyConferenceTalk(TemplateSlide):
    section_titles = ["Motivation", "Method", "Experiments", "Conclusion"]
    author = "Your Name" # If you do not set this, it fill fall back to the deafults defined in `manim_deck.toml`
    theme = DARK_THEME

    def construct(self):
        self.title_slide("My Paper Title", occasion="ICML 2025")

        self.section_slide(1, "Motivation")
        self.statement_slide("Current methods struggle with X.")
        self.list_slide("Challenges", [
            "Challenge A is hard because ...",
            "Challenge B remains unsolved",
            "We need a new approach",
        ])

        self.section_slide(2, "Method")
        # ... your content here ...

        self.section_slide(4, "Conclusion")
        self.statement_slide("Questions?")
```

### Available slide types
These are the slide types that are defined in `TemplateSlide` and ready to use. 
You can also create your own custom slide types by subclassing `TemplateSlide` and adding new methods.

| Method | What it does |
|---|---|
| `title_slide(title, occasion=...)` | Full-width title with author + event |
| `section_slide(n, title)` | Section divider with progress bar |
| `statement_slide(text)` | Centred single statement |
| `list_slide(title, items)` | Heading + bulleted list (revealed one-by-one) |
| `text_slide(title, lines)` | Heading + paragraph body |
| `code_slide(title, code)` | Heading + syntax-highlighted code block |
| `image_slide(title, path)` | Heading + centred image |
| `two_column_slide(title, left, right)` | Side-by-side layout |

Every method accepts `add_footer=True` to show the progress bar and
`text_anim=Write` (or any Manim animation class) to change the entrance
animation.

### Themes

Themes are simple dataclasses that control general design. Create your own or use a built-in:

```python
from manim_deck.templates import Theme

MY_THEME = Theme(
    name="oxford",
    bg="#002147",           # Oxford blue
    panel="#0A3060",
    accent="#F0C808",       # Gold
    text="#FFFFFF",
    heading_size=52,
    body_size=34,
)

class OxfordTalk(TemplateSlide):
    theme = MY_THEME
    # ...
```

---

## Writing reusable animation modules

The key pattern: an animation module is a class that receives the slide
instance and has a `.run()` method.

```python
# src/manim_deck/animations/my_module.py

from manim import *

class NeuralNetModule:
    """Draws and animates a simple feedforward network."""

    def __init__(self, slide, *, layers=(4, 6, 6, 2)):
        self.slide = slide
        self.layers = layers

    def run(self):
        s = self.slide
        # ... build your Mobjects and call s.play() ...
```

Then use it in any talk:

```python
from manim_deck.animations.my_module import NeuralNetModule

class AnyTalk(TemplateSlide):
    def construct(self):
        self.update_canvas()
        NeuralNetModule(self, layers=(3, 8, 8, 1)).run()
        self.next_slide()
```

**Included example modules:**

- `PipelineModule` — animated left-to-right pipeline with labelled boxes.
- `CalloutModule` — highlighted panel for key results or definitions

Add your own to `src/manim_deck/animations/` and then you can import them everywhere.

### Contribute your templates via PR

If you build a polished, reusable animation module, consider opening a Pull Request
so others can use it too.

For example: if you create a clean animation of an **autoencoder architecture**
(encoder, latent space, decoder) that works well for research talks, consider creating a PR!

---

## Staying in sync with upstream updates

If you forked this repo, you can pull new templates and animation modules:

```bash
# One-time: add the original repo as a remote
git remote add upstream https://github.com/ufuk-cakir/manim-deck.git

# Whenever you want updates
git fetch upstream
git merge upstream/main
```

Your talks in `talks/` won't conflict because the shared code lives in `src/`.

Alternatively, if you want to keep your talks in a completely separate repo,
you can install `manim_deck` directly from the template repo:

```bash
# In your separate talks repo
uv add git+https://github.com/ufuk-cakir/manim-deck.git
```

This way `manim_deck` is a dependency and updates with `uv sync`.

---

## Tips & workflow

- **Render at low quality while iterating:** `manim-slides render -ql main.py MyTalk`
  (`-ql` = low quality, much faster). Once you are happy, render the final version in high quality (`-qh`), or even 4k (`-qk`) if you want to future-proof it.
- **Use `self.next_slide()`!** More pause points = more control during
  the live talk. You can always skip through them quickly.
- **Test the HTML export early.** If you're presenting from a browser (e.g. on
  someone else's machine), make sure the export works before the day of.
- **Disable caching**: For large animations it is usually best to disable caching in manim using the `--disable_caching` flag.

---

## Useful resources

- [Manim Community docs](https://docs.manim.community/) — comprehensive API
  reference and tutorials
- [Manim Slides docs](https://manim-slides.eertmans.be/) — the slides extension
- [3Blue1Brown's Manim repo](https://github.com/3b1b/manim) — the original
  (different API, but great for inspiration)
- [Manim Community Discord](https://www.manim.community/discord/) — active
  community for help and showcase

---

## License

MIT — use this however you like. 
If you use this template in your research presentations, a short acknowledgement is appreciated!! :))


GitHub: https://github.com/ufuk-cakir
Website: https://cakir-ufuk.de/

---

## Disclaimer
Parts of this repository were developed with the assistance of Claude Opus 4.6 (Feb 19, 2026).  
All design decisions, structure, and final implementations were reviewed and curated by the author.
