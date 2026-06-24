"""
Asset-specific glue for assets/images/Pipes.png.

The sheet is a 15x4 grid of 32x32 frames. The first row's 15 frames line up
with the PipeSprite enum (NORTH_SOUTH=0 .. WEST=14), so we expose just those
and index them directly by a cell's pipe_sprite value.
"""

from game.spritesheet import SpriteSheet

PIPES_SHEET_PATH = "assets/images/pipes_with_air_space.png"
PIPES_FRAME_SIZE = 32
PIPES_COLUMNS = 15
PIPES_FRAME_COUNT = 15  # one full row, matching PipeSprite (0..14)


def load_pipe_sheet() -> SpriteSheet:
    """Load Pipes.png as a SpriteSheet. Call after rl.init_window()."""
    return SpriteSheet(
        PIPES_SHEET_PATH,
        frame_width=PIPES_FRAME_SIZE,
        frame_height=PIPES_FRAME_SIZE,
        frame_count=PIPES_FRAME_COUNT,
        columns=PIPES_COLUMNS,
    )
