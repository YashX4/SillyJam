"""
Asset-specific glue for the ballbot dialog speaker.

The ballbot ships as individual 33x38 PNG frames (one folder per color). We use
the red variant and animate through its 4 frames so it looks like he's talking.
"""

import pyray as rl

from game.spritesheet import FrameSprite

BALLBOT_FRAME_WIDTH = 33
BALLBOT_FRAME_HEIGHT = 38

# Red variant (assets/images/ballbot/1), frames in order.
BALLBOT_FRAMES = [
    "assets/images/ballbot/1/ballred1.png",
    "assets/images/ballbot/1/ballred2.png",
    "assets/images/ballbot/1/ballred3.png",
    "assets/images/ballbot/1/ballred4.png",
]


def load_ballbot(fps: float = 8.0) -> FrameSprite:
    """Load the ballbot frames as an animated sprite. Call after rl.init_window()."""
    textures = [rl.load_texture(path) for path in BALLBOT_FRAMES]
    return FrameSprite(textures, fps=fps)
