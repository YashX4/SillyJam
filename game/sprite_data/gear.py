"""
Asset-specific glue for the gear.

The gear ships as a single horizontal sprite sheet of 4 frames, each 40x40.
At CELL_SIZE=32 a gear covers a 2x2 block of cells (64x64), so the 40x40 frames
are scaled up at draw time to fill that footprint.
"""

from game.spritesheet import AnimatedSprite, SpriteSheet

GEAR_SHEET = "assets/images/Gear_5_Silver_spritesheet.png"
GEAR_FRAME_SIZE = 40
GEAR_FRAME_COUNT = 4


def load_gear_sprite(fps: float = 12.0) -> AnimatedSprite:
    """Load the gear sheet as an animated sprite. Call after rl.init_window()."""
    sheet = SpriteSheet(
        GEAR_SHEET,
        frame_width=GEAR_FRAME_SIZE,
        frame_height=GEAR_FRAME_SIZE,
        frame_count=GEAR_FRAME_COUNT,
    )
    return AnimatedSprite(sheet, fps=fps)
