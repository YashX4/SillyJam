"""
Mutable game state.
- set by physics loop
- read by draw loop 
"""

from dataclasses import dataclass, field
from enum import Enum, auto

from game import grid
from game.types import Cell, PipeSprite
from game.spritesheet import AnimatedSprite, SpriteSheet
from game.config import GRID_COLS, GRID_ROWS

INITIAL_X = 400.0
INITIAL_Y = 225.0


class Scene(Enum):
    """Which top-level screen the game is currently showing."""

    MENU = auto()
    PLAYING = auto()
    
@dataclass
class GridState:
    show_grid: bool = False
    
    def get_hover_cell(self, mouse_x, mouse_y) -> Cell:
        coords: Cell = grid.pixel_to_cell(mouse_x, mouse_y)
        if grid.in_bounds(coords.x, coords.y):
            return self.grid[coords.y][coords.x]
        return coords

    grid: list[list[Cell]] = field(
        default_factory=lambda: [[Cell(x=x, y=y, pipe=PipeSprite.AIR) for x in range(GRID_COLS)] for y in range(GRID_ROWS)]
    )
    def set_pipe(self, col: int, row: int, new_pipe: PipeSprite) -> None:
        """Set the pipe sprite of the cell at (col, row)."""
        if grid.in_bounds(col, row):
            self.grid[row][col].pipe = new_pipe

    def toggle_source(self, col: int, row: int) -> None:
        """Toggle whether the cell at (col, row) is a source."""
        if grid.in_bounds(col, row):
            self.grid[row][col].is_source = not self.grid[row][col].is_source
    
@dataclass
class GameState:

    initial_game_time: float = 0.0
    last_flow_step_time: float = -float('inf')
    scene: Scene = Scene.MENU
    grid_state: GridState = field(default_factory=GridState)

    # Loaded after init_window (needs a GL context), so they start as None.
    sprite: AnimatedSprite | None = None
    pipe_sheet: SpriteSheet | None = None
    water_pipe_sheet: SpriteSheet | None = None
