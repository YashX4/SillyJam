"""
Mutable game state.
- set by physics loop
- read by draw loop 
"""

from dataclasses import dataclass, field

from game import grid
from game.types import Cell, PipeSprite
from game.spritesheet import AnimatedSprite, SpriteSheet
from game.config import GRID_COLS, GRID_ROWS

INITIAL_X = 400.0
INITIAL_Y = 225.0
    
@dataclass
class GridState:
    show_grid: bool = False
    curr_hovered_cell: Cell = field(default_factory=lambda: Cell(x=0, y=0, color=(0, 0, 0), pipe=PipeSprite.AIR))

    grid: list[list[Cell]] = field(
        default_factory=lambda: [[Cell(x=x, y=y, color=(0, 0, 0), pipe=PipeSprite.AIR) for x in range(GRID_COLS)] for y in range(GRID_ROWS)]
    )
    def set_pipe(self, col: int, row: int, new_pipe: PipeSprite) -> None:
        """Set the pipe sprite of the cell at (col, row)."""
        if grid.in_bounds(col, row):
            self.grid[row][col].pipe = new_pipe
    
@dataclass
class GameState:

    grid_state: GridState = field(default_factory=GridState)

    # Loaded after init_window (needs a GL context), so they start as None.
    sprite: AnimatedSprite | None = None
    pipe_sheet: SpriteSheet | None = None
