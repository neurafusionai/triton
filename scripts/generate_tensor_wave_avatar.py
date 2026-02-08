#!/usr/bin/env python3
"""Generate a Tensor Wave avatar SVG concept for Triton branding."""

from __future__ import annotations

import argparse
import math
from pathlib import Path


DARK_BLUE = "#0A2540"
CYAN = "#00D4AA"
LIGHT_CYAN = "#67F5D7"
GRID = "#1D5D88"


def wave_path(width: int, height: int) -> str:
    mid_y = height * 0.53
    amp = height * 0.18
    points = []
    for i in range(33):
        x = width * i / 32
        phase = i / 32 * 2.4 * math.pi
        y = mid_y - amp * math.sin(phase) * math.exp(-((i - 16) / 19) ** 2)
        points.append((x, y))

    commands = [f"M 0,{height}", f"L 0,{points[0][1]:.2f}"]
    commands.extend(f"L {x:.2f},{y:.2f}" for x, y in points[1:])
    commands.extend([f"L {width},{height}", "Z"])
    return " ".join(commands)


def thread_grid(width: int, height: int) -> str:
    cells_x = 8
    cells_y = 6
    padding = width * 0.12
    cell_w = (width - 2 * padding) / cells_x
    cell_h = (height * 0.4) / cells_y
    y0 = height * 0.56

    rects = []
    for row in range(cells_y):
        for col in range(cells_x):
            alpha = 0.15 + 0.55 * ((row + col) % 4) / 3
            x = padding + col * cell_w
            y = y0 + row * cell_h
            rects.append(
                f'<rect x="{x:.2f}" y="{y:.2f}" width="{cell_w - 1.8:.2f}" height="{cell_h - 1.8:.2f}" '
                f'rx="2" fill="{GRID}" fill-opacity="{alpha:.2f}" />'
            )
    return "\n      ".join(rects)


def t_crest(width: int, height: int) -> str:
    cx = width * 0.52
    cy = height * 0.34
    top_w = width * 0.34
    stem_w = width * 0.09
    stem_h = height * 0.24
    top_h = height * 0.06

    x_left = cx - top_w / 2
    x_stem = cx - stem_w / 2
    y_top = cy
    y_stem = cy + top_h

    return (
        f'<rect x="{x_left:.2f}" y="{y_top:.2f}" width="{top_w:.2f}" height="{top_h:.2f}" '
        f'rx="6" fill="{LIGHT_CYAN}" />\n'
        f'      <rect x="{x_stem:.2f}" y="{y_stem:.2f}" width="{stem_w:.2f}" height="{stem_h:.2f}" '
        f'rx="6" fill="{LIGHT_CYAN}" />'
    )


def build_svg(size: int) -> str:
    width = size
    height = size
    wave = wave_path(width, height)
    grid = thread_grid(width, height)
    crest = t_crest(width, height)

    return f"""<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 {width} {height}\" role=\"img\" aria-label=\"Triton Tensor Wave avatar concept\">
  <defs>
    <linearGradient id=\"bg\" x1=\"0\" x2=\"0\" y1=\"0\" y2=\"1\">
      <stop offset=\"0%\" stop-color=\"{DARK_BLUE}\" />
      <stop offset=\"100%\" stop-color=\"#051425\" />
    </linearGradient>
    <linearGradient id=\"wave\" x1=\"0\" x2=\"1\" y1=\"0\" y2=\"0\">
      <stop offset=\"0%\" stop-color=\"#1090CF\" />
      <stop offset=\"70%\" stop-color=\"{CYAN}\" />
      <stop offset=\"100%\" stop-color=\"{LIGHT_CYAN}\" />
    </linearGradient>
    <filter id=\"glow\" x=\"-20%\" y=\"-20%\" width=\"140%\" height=\"140%\">
      <feGaussianBlur stdDeviation=\"4\" result=\"blur\"/>
      <feMerge><feMergeNode in=\"blur\"/><feMergeNode in=\"SourceGraphic\"/></feMerge>
    </filter>
  </defs>
  <rect width=\"100%\" height=\"100%\" fill=\"url(#bg)\" rx=\"22\" />
  <g>
    <path d=\"{wave}\" fill=\"url(#wave)\" />
    <path d=\"{wave}\" fill=\"none\" stroke=\"{LIGHT_CYAN}\" stroke-opacity=\"0.55\" stroke-width=\"2.3\"/>
  </g>
  <g filter=\"url(#glow)\">
      {grid}
  </g>
  <g filter=\"url(#glow)\">
      {crest}
  </g>
</svg>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--size", type=int, default=512, help="Canvas size in pixels.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/branding/tensor-wave-avatar.svg"),
        help="Output SVG path.",
    )
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build_svg(args.size), encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
