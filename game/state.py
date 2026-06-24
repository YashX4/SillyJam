"""
Mutable game state.
- set by physics loop
- read by draw loop 
"""

from dataclasses import dataclass, field
from enum import Enum, auto

import pyray as rl

from game import grid
from game.dialog import DialogState
from game.types import Boiler, Cell, Gear, PipeSprite
from game.sprite_data.parallax import ParallaxBackground
from game.spritesheet import AnimatedSprite, FrameSprite, SpriteSheet
from game.config import BOILER_SPAN, GEAR_SPAN, GRID_COLS, GRID_ROWS


class Scene(Enum):
    """Which top-level screen the game is currently showing."""

    MENU = auto()
    PLAYING = auto()
    
@dataclass
class GridState:
    show_grid: bool = False

    # Debug rectangle: red outline spanning from `debug_rect_tl` (top-left cell)
    # to `debug_rect_br` (bottom-right cell), inclusive. Toggled with ";".
    show_debug_rect: bool = False
    debug_rect_tl: Cell = field(default_factory=lambda: Cell(x=0, y=0))
    debug_rect_br: Cell = field(default_factory=lambda: Cell(x=4, y=4))

    def get_hover_cell(self, mouse_x, mouse_y) -> Cell:
        coords: Cell = grid.pixel_to_cell(mouse_x, mouse_y)
        if grid.in_bounds(coords.x, coords.y):
            return self.grid[coords.y][coords.x]
        return coords

    grid: list[list[Cell]] = field(
        default_factory=lambda: [[Cell(x=x, y=y, pipe=PipeSprite.AIR) for x in range(GRID_COLS)] for y in range(GRID_ROWS)]
    )
    def set_pipe(self, col: int, row: int, new_pipe: PipeSprite) -> None:
        """Set the pipe sprite of the cell at (col, row).

        Cells covered by a boiler or gear are reserved and cannot hold a pipe.
        """
        if grid.in_bounds(col, row) and not self.cell_reserved(col, row):
            self.grid[row][col].pipe = new_pipe

    def toggle_source(self, col: int, row: int) -> None:
        """Toggle whether the cell at (col, row) is a source.

        Cells covered by a boiler or gear are reserved and cannot be a source.
        """
        if grid.in_bounds(col, row) and not self.cell_reserved(col, row):
            self.grid[row][col].is_source = not self.grid[row][col].is_source

    # Each placed boiler tracks its own top-left (col, row) and accumulated heat.
    # Each boiler spans BOILER_SPAN cells in both directions (a 2x2 block).
    boilers: list[Boiler] = field(default_factory=list)

    # Each placed gear tracks its own top-left (col, row) and spans a 2x2 block.
    gears: list[Gear] = field(default_factory=list)

    def cell_in_boiler(self, col: int, row: int) -> bool:
        """True if (col, row) falls within any placed boiler's 2x2 footprint."""
        for boiler in self.boilers:
            if (
                boiler.col <= col < boiler.col + BOILER_SPAN
                and boiler.row <= row < boiler.row + BOILER_SPAN
            ):
                return True
        return False

    def cell_in_gear(self, col: int, row: int) -> bool:
        """True if (col, row) falls within any placed gear's 2x2 footprint."""
        for gear in self.gears:
            if (
                gear.col <= col < gear.col + GEAR_SPAN
                and gear.row <= row < gear.row + GEAR_SPAN
            ):
                return True
        return False

    def cell_reserved(self, col: int, row: int) -> bool:
        """True if (col, row) is covered by any placed boiler or gear."""
        return self.cell_in_boiler(col, row) or self.cell_in_gear(col, row)

    def place_boiler(self, col: int, row: int) -> bool:
        """Place a boiler with (col, row) as its top-left cell.

        Returns False if the 2x2 footprint would fall outside the grid, overlap
        an existing boiler or gear, or cover a cell that already holds a pipe or
        source.
        """
        if not (
            grid.in_bounds(col, row)
            and grid.in_bounds(col + BOILER_SPAN - 1, row + BOILER_SPAN - 1)
        ):
            return False
        for r in range(row, row + BOILER_SPAN):
            for c in range(col, col + BOILER_SPAN):
                cell = self.grid[r][c]
                if (
                    self.cell_reserved(c, r)
                    or cell.pipe is not PipeSprite.AIR
                    or cell.is_source
                ):
                    return False
        self.boilers.append(Boiler(col=col, row=row))
        return True

    def place_gear(self, col: int, row: int) -> bool:
        """Place a gear with (col, row) as its top-left cell.

        Returns False if the 2x2 footprint would fall outside the grid, overlap
        an existing boiler or gear, or cover a cell that already holds a pipe or
        source.
        """
        if not (
            grid.in_bounds(col, row)
            and grid.in_bounds(col + GEAR_SPAN - 1, row + GEAR_SPAN - 1)
        ):
            return False
        for r in range(row, row + GEAR_SPAN):
            for c in range(col, col + GEAR_SPAN):
                cell = self.grid[r][c]
                if (
                    self.cell_reserved(c, r)
                    or cell.pipe is not PipeSprite.AIR
                    or cell.is_source
                ):
                    return False
        self.gears.append(Gear(col=col, row=row))
        return True
    
@dataclass
class GameState:

    initial_game_time: float = 0.0
    last_flow_step_time: float = -float('inf')
    scene: Scene = Scene.MENU
    grid_state: GridState = field(default_factory=GridState)
    dialog: DialogState = field(default_factory=DialogState)

    # World camera: pan/zoom across the (much larger than viewport) grid.
    camera: rl.Camera2D = field(
        default_factory=lambda: rl.Camera2D(
            rl.Vector2(0.0, 0.0),  # offset (screen-space)
            rl.Vector2(0.0, 0.0),  # target (world-space point at offset)
            0.0,                   # rotation
            1.0,                   # zoom
        )
    )

    # Loaded after init_window (needs a GL context), so they start as None.
    sprite: AnimatedSprite | None = None
    background: ParallaxBackground | None = None
    pipe_sheet: SpriteSheet | None = None
    water_pipe_sheet: SpriteSheet | None = None
    ballbot: FrameSprite | None = None
    pump_sprite: FrameSprite | None = None
    boiler_sprite: FrameSprite | None = None
    gear_sprite: AnimatedSprite | None = None
    selection_sprite: FrameSprite | None = None
    # rl.Music is a cffi factory (not a class), so it can't go in a `| None`
    # union that's evaluated at class definition; quote it as a forward ref.
    music: "rl.Music | None" = None
    robot_talk: "rl.Sound | None" = None
