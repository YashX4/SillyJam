"""Grid helpers: convert between cell coordinates and pixel coordinates.

A cell is identified by its (col, row) position in the grid.
"""

from game.config import CELL_SIZE, GRID_COLS, GRID_ROWS
from game.types import Cell, Direction, PipeSprite

def cell_to_px(cell: Cell) -> tuple[int, int]:
    """Return the top-left pixel (x, y) of the given cell."""
    return cell_coords_to_top_left_pixel(cell.x, cell.y)


def cell_coords_to_top_left_pixel(col: int, row: int) -> tuple[int, int]:
    """Return the top-left pixel (x, y) of the given cell."""
    return (col * CELL_SIZE, row * CELL_SIZE)


def pixel_to_cell(x: float, y: float) -> Cell:
    """Return the (col, row) of the cell containing the given pixel."""
    col = int(x // CELL_SIZE)
    row = int(y // CELL_SIZE)
    return Cell(x=col, y=row, color=(0, 0, 0))


def pipe_at(grid: list[list[int]], col: int, row: int) -> PipeSprite:
    """The pipe in a cell. Out-of-bounds cells are treated as AIR."""
    if not (0 <= col < GRID_COLS and 0 <= row < GRID_ROWS):
        return PipeSprite.AIR
    return PipeSprite(grid[row][col])


def cells_connected(grid: list[list[int]], a: Cell, b: Cell) -> bool:
    """True if a and b are orthogonally adjacent and their pipes open toward
    each other: a must have an opening facing b, and b the opposite opening
    facing back at a."""
    direction = Direction.from_delta(b.x - a.x, b.y - a.y)
    if direction is None:
        return False
    a_pipe = pipe_at(grid, a.x, a.y)
    b_pipe = pipe_at(grid, b.x, b.y)
    return direction in a_pipe.openings and direction.opposite in b_pipe.openings


def connected_neighbors(grid: list[list[int]], cell: Cell) -> list[Cell]:
    """All orthogonally adjacent cells that share a pipe connection with `cell`."""
    neighbors = []
    for direction in Direction:
        neighbor = Cell(
            x=cell.x + direction.dx, y=cell.y + direction.dy, color=(0, 0, 0)
        )
        if cells_connected(grid, cell, neighbor):
            neighbors.append(neighbor)
    return neighbors
