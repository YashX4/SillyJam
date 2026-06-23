"""
Mutable game state.
- set by physics loop
- read by draw loop 
"""

from dataclasses import dataclass
from game.spritesheet import AnimatedSprite

INITIAL_X = 400.0
INITIAL_Y = 225.0
@dataclass
class GameState:
    move_speed: float = 150.0
    x: float = INITIAL_X
    y: float = INITIAL_Y

    # Position after the previous physics step, used to interpolate the render.
    prev_x: float = INITIAL_X
    prev_y: float = INITIAL_Y

    show_grid: bool = False

    # Loaded after init_window (needs a GL context), so it starts as None.
    sprite: AnimatedSprite | None = None
    