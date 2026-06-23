"""
Mutable game state.
- set by physics loop
- read by draw loop 
"""

from dataclasses import dataclass, field

from game.types import Cell
from game.spritesheet import AnimatedSprite
from game.config import GRID_COLS, GRID_ROWS

INITIAL_X = 400.0
INITIAL_Y = 225.0
    
@dataclass
class GridState:
    show_grid: bool = False
    curr_hovered_cell: Cell | None = None

    grid: list[list[int]] = field(
        default_factory=lambda: [[0] * GRID_COLS for _ in range(GRID_ROWS)]
    )    
    
@dataclass
class GameState:

    grid_state: GridState = field(default_factory=GridState)

    # Loaded after init_window (needs a GL context), so it starts as None.
    sprite: AnimatedSprite | None = None
