"""
Asset-specific glue for the boiler.

The boiler ships as 13 individual 64x64 PNG frames. At CELL_SIZE=32 a 64x64
sprite covers a 2x2 block of cells, so a boiler occupies 4 cells with its
placement cell as the top-left corner.
"""

import pyray as rl

from game.spritesheet import FrameSprite

BOILER_FRAME_SIZE = 64  # 2x2 cells at CELL_SIZE=32
BOILER_FRAME_COUNT = 13

BOILER_FRAMES = [
    f"assets/images/animated_64_64_boiler/boiler{i}.png"
    for i in range(1, BOILER_FRAME_COUNT + 1)
]


def load_boiler_sprite(fps: float = 12.0) -> FrameSprite:
    """Load the boiler frames as an animated sprite. Call after rl.init_window()."""
    textures = [rl.load_texture(path) for path in BOILER_FRAMES]
    return FrameSprite(textures, fps=fps)
