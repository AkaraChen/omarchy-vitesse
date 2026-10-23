#!/usr/bin/env python3
"""Render a placeholder preview.png for every theme.

These are palette cards, not desktop screenshots. Replace them with real
screenshots once the themes have been used for a while:

    omarchy capture screenshot fullscreen save

Then resize to roughly 1600x1000 and drop the result in
`themes/<slug>/preview.png`.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from generate import VARIANTS, build_colors

ROOT = Path(__file__).resolve().parents[1]
THEMES_DIR = ROOT / "themes"

WIDTH, HEIGHT = 1600, 1000
FONT = "JetBrainsMono-NF-Regular"
FONT_BOLD = "JetBrainsMono-NF-Bold"

TITLES = {
    "vitesse-light": "Vitesse Light",
    "vitesse-light-soft": "Vitesse Light Soft",
    "vitesse-dark": "Vitesse Dark",
    "vitesse-dark-soft": "Vitesse Dark Soft",
    "vitesse-black": "Vitesse Black",
}

NORMAL = ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white")
BRIGHT = (
    "br-black",
    "br-red",
    "br-green",
    "br-yellow",
    "br-blue",
    "br-magenta",
    "br-cyan",
    "br-white",
)


def swatches(colors: dict[str, str]) -> list[tuple[str, str]]:
    normal = [
        colors["background"],
        colors["red"],
        colors["green"],
        colors["yellow"],
        colors["blue"],
        colors["magenta"],
        colors["cyan"],
        colors["foreground"],
    ]
    bright = [
        colors["muted"],
        colors["bright_red"],
        colors["bright_green"],
        colors["bright_yellow"],
        colors["bright_blue"],
        colors["bright_magenta"],
        colors["bright_cyan"],
        colors["bright_foreground"],
    ]
    return list(zip(NORMAL, normal)) + list(zip(BRIGHT, bright))


def render(slug: str, theme_dir: Path) -> None:
    design = build_colors(VARIANTS[slug])
    terminal = build_colors(VARIANTS[slug], terminal=True)

    title = TITLES.get(slug, slug.replace("-", " ").title())
    background = design["background"]
    foreground = design["foreground"]
    muted = design["muted"]
    surface = design["lighter_background"]
    accent = design["accent"]

    args = [
        "magick",
        "-size",
        f"{WIDTH}x{HEIGHT}",
        f"xc:{background}",
        "-gravity",
        "NorthWest",
        # Card
        "-fill",
        surface,
        "-stroke",
        "none",
        "-draw",
        "roundrectangle 70,70 1530,930 28,28",
        "-fill",
        "none",
        "-stroke",
        muted,
        "-strokewidth",
        "1",
        "-draw",
        "roundrectangle 70,70 1530,930 28,28",
        # Title
        "-font",
        FONT_BOLD,
        "-pointsize",
        "92",
        "-fill",
        foreground,
        "-annotate",
        "+150+240",
        title,
        # Subtitle
        "-font",
        FONT,
        "-pointsize",
        "30",
        "-fill",
        muted,
        "-annotate",
        "+154+340",
        f"Omarchy theme · {VARIANTS[slug]['mode']}",
        # Accent hex, top right
        "-gravity",
        "NorthEast",
        "-pointsize",
        "28",
        "-fill",
        accent,
        "-annotate",
        "+150+180",
        f"accent {accent}",
        "-gravity",
        "NorthWest",
        # Divider
        "-stroke",
        muted,
        "-strokewidth",
        "1",
        "-draw",
        "line 150,380 1450,380",
    ]

    for index, (label, value) in enumerate(swatches(terminal)):
        row, column = divmod(index, 8)
        x = 150 + column * 166
        y = 430 + row * 160
        args += [
            "-fill",
            value,
            "-stroke",
            muted,
            "-strokewidth",
            "1",
            "-draw",
            f"roundrectangle {x},{y} {x + 146},{y + 90} 10,10",
            "-font",
            FONT,
            "-pointsize",
            "18",
            "-fill",
            muted,
            "-stroke",
            "none",
            "-annotate",
            f"+{x + 4}+{y + 120}",
            label,
        ]

    args += [
        "-font",
        FONT,
        "-pointsize",
        "24",
        "-fill",
        muted,
        "-annotate",
        "+150+870",
        "ported from antfu/vscode-theme-vitesse",
    ]

    subprocess.run(args + [str(theme_dir / "preview.png")], check=True)
    print(f"wrote {theme_dir / 'preview.png'}")


def main() -> int:
    for slug in TITLES:
        theme_dir = THEMES_DIR / slug
        if not (theme_dir / "colors.toml").is_file():
            print(f"missing {theme_dir / 'colors.toml'}, run tools/generate.py first")
            return 1
        render(slug, theme_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
