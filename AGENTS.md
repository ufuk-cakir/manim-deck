# AGENTS.md

manim-deck is a Python package (`src/manim_deck`) of slide templates and animation
modules for research talks, built on [Manim Community](https://github.com/ManimCommunity/manim)
and [Manim Slides](https://github.com/jeertmans/manim-slides). Each talk is a
script in `talks/<name>/` that imports from the package.

## Commands

Run everything through `uv run` from the repo root (`manim-slides render` writes
`slides/` into the current directory, and `manim_deck.toml` there holds the default author).

- Install: `uv sync`
- Render a talk while iterating: `uv run manim-slides render -ql talks/<name>/main.py <Scene>`
- See a talk: `uv run python tools/preview.py talks/<name>/main.py <Scene>` writes
  `preview/<Scene>/NN.png` (the last frame of each slide, what the audience sees during
  the pause) and `preview/<Scene>/sheet.png`. Open these PNGs: they are your eyes.
- Export: `uv run manim-slides convert <Scene> talk.html` (add `--one-file` to embed the videos)
- README animations: `uv run python docs/make_clips.py [Scene ...]` renders the scenes in
  `docs/readme_clips.py` at 1080p30 into looping WebP files in `docs/assets/` (needs ffmpeg and
  `img2webp` from libwebp). The crash-course scenes and `MyPresentation` are printed in full in
  `README.md`; edit the scene and its README copy together.

`pyproject.toml` pins manim < 0.22, manim-slides 5.x and Pillow < 13; the comment there
gives the reason for each pin. Keep the pins unless you have rendered the example talk and
every README clip with a newer combination. Write Manim Community code
(`Create`, `MathTex`, `Code(code_string=...)`), the API in the docs at docs.manim.community.

## Where code goes

- `src/manim_deck/templates/base.py`: `TemplateSlide`, with one method per slide type
  (`title_slide`, `list_slide`, ...), `update_canvas()` and the progress bar.
- `src/manim_deck/templates/theme.py`: the `Theme` dataclass. Take colours and font sizes
  from `self.theme` (in a module: `slide.theme`), so a talk restyles in one line.
- `src/manim_deck/animations/<name>.py`: a reusable **module**, `XModule(slide, *, options).run()`.
  It builds mobjects, plays them through `slide.play(...)`, may call `slide.next_slide()`
  between its animations, and leaves its group on `self.mobject`. `pipeline.py` is the reference.
- `src/manim_deck/animations/custom/`: the author's modules from wildfire talks, kept as
  examples. Some need images, data or the private `jwf` simulator. Change them only when asked.
- `talks/<name>/main.py`: one talk. One method per slide, each starting with
  `self.update_canvas()`, called in order from `construct()`, so slides reorder by moving a line.
  Talk-only helpers stay in the talk folder; a helper moves to `animations/` when a second talk needs it.
- Data for a slide: a separate script computes it and saves `.npz` or `.json` in the talk folder;
  slide code loads and draws. Numbers on slides come from those files.
- Generated and gitignored: `media/`, `slides/`, `preview/`, `docs/.build/`. Commit sources and `docs/assets/`.

## Building a slide

1. Plan the slide as **one animation per click**, with a `self.next_slide()` after each. `next_slide(loop=True)` makes
   the following animation repeat until the click; `auto_next=True` continues without one.
2. Render at `-ql` and run `tools/preview.py`.
3. Open every still of the slides you touched and `sheet.png`. Fix and repeat.

Done when the render finishes without a Traceback, every still you touched shows no
overlapping text, nothing outside the frame or inside the slide-number corner (bottom left),
and no empty frame, and, if you changed a module or scene the README shows, `docs/make_clips.py`
has rebuilt those clips.

For a new visual direction (theme, background, transitions), build one or two slides,
show the author the stills, and roll it out after they agree.

Slide text: short descriptive headings and plain sentences, one idea per slide.
Spoken explanation belongs in the author's notes.

## Gotchas

Found with manim 0.20-0.21 and manim-slides 5.6-5.7. Add each new trap here with its fix.

- Stills: `manim -s` (`save_last_frame`) and `--dry_run` crash on `Slide` classes. Render the
  video and take frames with `tools/preview.py` or `ffmpeg -sseof -0.3 -i in.mp4 -update 1 out.png`.
- `VGroup` takes only VMobjects. Group an `ImageMobject` with `Group`.
- Light themes: pass `color=` to the `MathTex`/`Tex` constructor. Parts without a colour
  (operators like `=`, `+`) render white, which is invisible on a light background.
- Colour words inside a `Text` with `t2c={"word": COLOR}` (and `t2w` for weight) at
  construction; `Text` has no `set_color_by_text`.
- `Text(line_spacing=0.5)` gives comfortable body leading and `0.3` tight two-line titles;
  the default puts lines almost touching.
- `DoubleArrow(..., max_tip_length_to_length_ratio=0.5)` draws two equal tips; animate it with `GrowFromCenter`.
- Short arrows keep their shaft with `max_stroke_width_to_length_ratio=100`.
- A `ValueTracker` you animate: put updaters on a separate `Mobject()` that reads the tracker.
  An updater on the tracker itself runs on the animation's target copy and jumps to the end.
- Mobject subclasses: Manim already uses the attribute `dim` and the attribute `target`;
  choose other names.
- After `play(LaggedStart(...))` or `AnimationGroup`, the wrapper group stays in the scene.
  To clear the parts, remove every top-level mobject in `self.mobjects` that contains them.
- A mobject that rebuilds its `submobjects` every frame leaves frozen copies behind. Keep a
  fixed pool of parts and update each with `part.become(new)`.
- `StreamLines` needs `padding >= noise_factor / 2`; with less, the lines come out empty.
- When the manim child process crashes, `manim-slides render` can hang. Watch the output
  for a Traceback.
- Long renders on macOS: run them under `caffeinate -i` so sleep does not stall them.
