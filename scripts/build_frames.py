from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "assets" / "codex-spritesheet-v4.webp"
OUTPUT = ROOT / "src" / "frames.js"
CELL_WIDTH = 192
CELL_HEIGHT = 208
ALPHA_THRESHOLD = 64

MOVE_SEQUENCE = (
    [(0, column) for column in range(6)]
    + [(1, column) for column in range(8)]
    + [(2, column) for column in range(8)]
    + [(0, column) for column in range(6)]
)
WORK_SEQUENCE = [(7, column) for column in range(6)]


def hex_color(pixel: tuple[int, int, int, int]) -> str:
    return "#%02x%02x%02x" % pixel[:3]


def render(sequence: list[tuple[int, int]], width: int, height: int, atlas: Image.Image):
    frames = []
    for row, column in sequence:
        cell = atlas.crop((
            column * CELL_WIDTH,
            row * CELL_HEIGHT,
            (column + 1) * CELL_WIDTH,
            (row + 1) * CELL_HEIGHT,
        )).resize((width, height), Image.Resampling.LANCZOS)
        pixels = cell.load()
        output_rows = []
        for y in range(0, height, 2):
            runs = []
            for x in range(width):
                top = pixels[x, y]
                bottom = pixels[x, min(y + 1, height - 1)]
                top_visible = top[3] > ALPHA_THRESHOLD
                bottom_visible = bottom[3] > ALPHA_THRESHOLD
                if top_visible and bottom_visible:
                    item = ("▀", hex_color(top), hex_color(bottom))
                elif top_visible:
                    item = ("▀", hex_color(top), None)
                elif bottom_visible:
                    item = ("▄", hex_color(bottom), None)
                else:
                    item = (" ", None, None)
                if runs and runs[-1][1:] == list(item[1:]):
                    runs[-1][0] += item[0]
                else:
                    runs.append([item[0], item[1], item[2]])
            output_rows.append([
                {"text": text, "fg": foreground, "bg": background}
                for text, foreground, background in runs
            ])
        frames.append(output_rows)
    return frames


def main() -> None:
    if not ASSET.exists():
        raise SystemExit(
            "Missing local sprite sheet: assets/codex-spritesheet-v4.webp\n"
            "Add a sprite sheet you are authorized to use, then rerun this command."
        )
    with Image.open(ASSET) as image:
        if image.size != (1536, 1872):
            raise SystemExit(f"Expected a 1536x1872 sprite sheet; found {image.width}x{image.height}.")
        atlas = image.convert("RGBA")
    data = {
        "large": {
            "move": render(MOVE_SEQUENCE, 36, 40, atlas),
            "work": render(WORK_SEQUENCE, 36, 40, atlas),
        },
        "small": {
            "move": render(MOVE_SEQUENCE, 28, 30, atlas),
            "work": render(WORK_SEQUENCE, 28, 30, atlas),
        },
    }
    OUTPUT.write_text("export const FRAMES = " + json.dumps(data, separators=(",", ":")) + ";\n", encoding="utf-8")
    print(f"Generated {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
