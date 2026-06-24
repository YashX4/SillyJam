"""
Asset-specific glue for assets/images/Pipes.png.

The sheet is a 15x4 grid of 32x32 frames. The first row's 15 frames line up
with the PipeSprite enum (NORTH_SOUTH=0 .. WEST=14), so we expose just those
and index them directly by a cell's pipe_sprite value.
"""

from game.spritesheet import SpriteSheet

PIPES_SHEET_PATH = "assets/images/pipes_with_air_space.png"
# Companion sheet: identical frame layout but with water in each pipe.
PIPES_WATER_SHEET_PATH = "assets/images/pipes_with_air_space_water.png"
PIPES_FRAME_SIZE = 32
PIPES_COLUMNS = 15
PIPES_FRAME_COUNT = 15  # one full row, matching PipeSprite (0..14)


def _load_sheet(path: str) -> SpriteSheet:
    return SpriteSheet(
        path,
        frame_width=PIPES_FRAME_SIZE,
        frame_height=PIPES_FRAME_SIZE,
        frame_count=PIPES_FRAME_COUNT,
        columns=PIPES_COLUMNS,
    )


def load_pipe_sheet() -> SpriteSheet:
    """Load the dry pipe sheet as a SpriteSheet. Call after rl.init_window()."""
    return _load_sheet(PIPES_SHEET_PATH)


def load_water_pipe_sheet() -> SpriteSheet:
    """Load the water-filled pipe sheet as a SpriteSheet. Call after rl.init_window()."""
    return _load_sheet(PIPES_WATER_SHEET_PATH)
