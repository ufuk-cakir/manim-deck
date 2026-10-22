"""Render a talk at low quality and save one still per slide, plus a contact sheet.

    uv run python tools/preview.py talks/example-talk/main.py ExampleTalk
    uv run python tools/preview.py talks/example-talk/main.py ExampleTalk -q h --cols 4

Writes preview/<Scene>/NN.png (the last frame of each slide, i.e. what the
audience sees while you talk) and preview/<Scene>/sheet.png (all of them on
one image). Faster to check than scrubbing a video, and it is how a coding
agent can look at its own slides. Needs ffmpeg on the PATH.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("file", type=Path, help="talk script, e.g. talks/my-talk/main.py")
    parser.add_argument("scene", help="slide class name")
    parser.add_argument("-q", default="l", choices="lmhpk", help="render quality (default: l)")
    parser.add_argument("--cols", type=int, default=5, help="columns in the contact sheet")
    parser.add_argument("--width", type=int, default=480, help="width of one tile in px")
    parser.add_argument("--out", type=Path, default=ROOT / "preview")
    args = parser.parse_args()

    subprocess.run(
        [sys.executable, "-m", "manim_slides", "render", f"-q{args.q}",
         str(args.file.resolve()), args.scene],
        cwd=ROOT,
        check=True,
    )

    slides = json.loads((ROOT / "slides" / f"{args.scene}.json").read_text())["slides"]
    out = args.out / args.scene
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)

    for i, slide in enumerate(slides, start=1):
        # Decode the last 0.3 s and keep overwriting one PNG: the file ends up
        # holding the final frame, which is what the presenter pauses on.
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-sseof", "-0.3", "-i", str(ROOT / slide["file"]),
             "-update", "1", str(out / f"{i:02d}.png")],
            check=True,
        )

    rows = -(-len(slides) // args.cols)
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-framerate", "1", "-i", str(out / "%02d.png"),
         "-vf", f"scale={args.width}:-1,tile={args.cols}x{rows}:padding=4:color=white",
         "-frames:v", "1", str(out / "sheet.png")],
        check=True,
    )
    print(f"{len(slides)} slides -> {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}/")


if __name__ == "__main__":
    main()
