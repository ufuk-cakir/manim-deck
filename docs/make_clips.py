"""Render the README clips and turn them into looping animated images.

    uv run python docs/make_clips.py                    # every clip
    uv run python docs/make_clips.py Themes Mobjects    # some clips
    uv run python docs/make_clips.py --video in.mp4 --out talk.webp --width 1280 --speed 1.2
    uv run python docs/make_clips.py --video in.mp4 --out talk.gif   # for Google Slides

The scenes live in docs/readme_clips.py. Renders go to docs/.build/
(gitignored), clips to docs/assets/. The output format follows the file
extension: .webp (full colour, 30 fps, what the README uses) or .gif (for
tools without WebP support, such as Google Slides).

Needs ffmpeg, and img2webp from libwebp for .webp (`brew install webp`).
The gallery clips at the top of the README come from the author's talks,
whose code is not in this repo; `--video` is how they were made.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

DOCS = Path(__file__).resolve().parent
ROOT = DOCS.parent
BUILD = DOCS / ".build"
ASSETS = DOCS / "assets"

# scene in readme_clips.py -> clip name in docs/assets/
CLIPS = {
    "Concept": "concept",
    "Mobjects": "mobjects",
    "Animations": "animations",
    "Positioning": "positioning",
    "MyScene": "scene",
    "MyPresentation": "next-slide",
    "MyConferenceTalk": "first-talk",
    "SlideTypes": "slide-types",
    "Themes": "themes",
    "Pipeline": "pipeline-module",
    "Callout": "callout-module",
    "NeuralNet": "neural-net-module",
    "CellularAutomata": "ca-module",
}
SPEED = {"CellularAutomata": 1.5}   # clips that play faster than real time
WIDTHS = {"Concept": 1280}          # clips shown full width in the README

WIDTH = 960   # px; README cells show clips at ~400 px, so this is sharp on retina screens
FPS = 30
QUALITY = 80  # WebP quality


def render(scene: str) -> Path:
    """Render one scene at 1080p30 and return the video path."""
    subprocess.run(
        [
            sys.executable, "-m", "manim", "render", "-qh", "--fps", str(FPS),
            "--media_dir", str(BUILD),
            str(DOCS / "readme_clips.py"), scene,
        ],
        cwd=ROOT,
        check=True,
    )
    return BUILD / "videos" / "readme_clips" / f"1080p{FPS}" / f"{scene}.mp4"


def to_webp(video: Path, out: Path, *, width: int, fps: int, speed: float, quality: int):
    """Lossy animated WebP. A keyframe every 5 frames stops lossy leftovers
    from earlier frames piling up as blotches on flat backgrounds."""
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            ["ffmpeg", "-v", "error", "-i", str(video), "-vf",
             f"setpts=PTS/{speed},fps={fps},scale={width}:-2:flags=lanczos",
             f"{tmp}/%05d.png"],
            check=True,
        )
        frames = sorted(str(p) for p in Path(tmp).glob("*.png"))
        subprocess.run(
            ["img2webp", "-loop", "0", "-lossy", "-q", str(quality), "-m", "4",
             "-kmin", "4", "-kmax", "5", "-d", str(round(1000 / fps)), *frames,
             "-o", str(out)],
            check=True,
            stdout=subprocess.DEVNULL,
        )


def to_gif(video: Path, out: Path, *, width: int, fps: int, speed: float):
    """GIF with one palette per clip (256 colours, so keep fps and width modest)."""
    graph = (
        f"setpts=PTS/{speed},fps={fps},scale={width}:-1:flags=lanczos,split[a][b];"
        "[a]palettegen=stats_mode=diff[p];"
        "[b][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle"
    )
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(video),
         "-filter_complex", graph, "-loop", "0", str(out)],
        check=True,
    )


def convert(video: Path, out: Path, *, width: int = WIDTH, fps: int = FPS,
            speed: float = 1.0, quality: int = QUALITY):
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.suffix == ".gif":
        to_gif(video, out, width=width, fps=min(fps, 15), speed=speed)
    else:
        to_webp(video, out, width=width, fps=fps, speed=speed, quality=quality)
    shown = out.relative_to(ROOT) if out.is_relative_to(ROOT) else out
    print(f"{shown}  {out.stat().st_size / 1e6:.1f} MB")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("scenes", nargs="*", help=f"scenes to render (default: all of {list(CLIPS)})")
    parser.add_argument("--video", type=Path, help="convert this video instead of rendering")
    parser.add_argument("--out", type=Path, help="output path for --video (.webp or .gif)")
    parser.add_argument("--width", type=int, default=WIDTH)
    parser.add_argument("--fps", type=int, default=FPS)
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--quality", type=int, default=QUALITY, help="WebP quality, 0-100")
    args = parser.parse_args()
    opts = dict(width=args.width, fps=args.fps, quality=args.quality)

    if args.video:
        out = args.out or ASSETS / f"{args.video.stem}.webp"
        convert(args.video, out, speed=args.speed, **opts)
        return

    unknown = [s for s in args.scenes if s not in CLIPS]
    if unknown:
        parser.error(f"unknown scenes {unknown}; known: {list(CLIPS)}")
    for scene in args.scenes or CLIPS:
        convert(render(scene), ASSETS / f"{CLIPS[scene]}.webp",
                speed=SPEED.get(scene, args.speed),
                **{**opts, "width": WIDTHS.get(scene, args.width)})


if __name__ == "__main__":
    main()
