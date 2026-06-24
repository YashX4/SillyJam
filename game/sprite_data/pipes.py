"""
Asset-specific glue for assets/images/Pipes.png.

The sheet is a 15x4 grid of 32x32 frames. The first row's 15 frames line up
with the PipeSprite enum (NORTH_SOUTH=0 .. WEST=14), so we expose just those
and index them directly by a cell's pipe_sprite value.
"""

import pyray as rl

from game.spritesheet import FrameSprite, SpriteSheet

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


# Pump animation: ships as 4 individual 32x32 frames, drawn over source cells.
PUMP_PIPE_FRAMES = [
    f"assets/images/pump_pipe_animation/pump_pipe{i}.png" for i in range(1, 5)
]


def load_pump_pipe_sprite(fps: float = 8.0) -> FrameSprite:
    """Load the pump pipe frames as an animated sprite. Call after rl.init_window()."""
    textures = [rl.load_texture(path) for path in PUMP_PIPE_FRAMES]
    return FrameSprite(textures, fps=fps)
