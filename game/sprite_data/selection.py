"""
Asset-specific glue for the cell-hover selection highlight.

Ships as 4 individual 32x32 PNG frames (one CELL_SIZE square) that loop to
form a pulsing selection marker drawn over the cell under the cursor.
"""

import pyray as rl

from game.spritesheet import FrameSprite

SELECTION_FRAME_COUNT = 4

SELECTION_FRAMES = [
    f"assets/images/ui/selection/UI_Flat_Select02a_{i}.png"
    for i in range(1, SELECTION_FRAME_COUNT + 1)
]


def load_selection_sprite(fps: float = 8.0) -> FrameSprite:
    """Load the selection frames as an animated sprite. Call after rl.init_window()."""
    textures = [rl.load_texture(path) for path in SELECTION_FRAMES]
    return FrameSprite(textures, fps=fps)
