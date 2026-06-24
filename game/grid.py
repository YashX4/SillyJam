"""Grid helpers: convert between cell coordinates and pixel coordinates.

A cell is identified by its (col, row) position in the grid.
"""

from game.config import CELL_SIZE, GRID_COLS, GRID_ROWS
from game.state import GridState
from game.types import Cell, Direction, PipeSprite

def in_bounds(col: int, row: int) -> bool:
    """Return True if the given cell coordinates are within the grid."""
    return 0 <= col < GRID_COLS and 0 <= row < GRID_ROWS

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


def adjacent(cell_a: Cell, cell_b: Cell) -> bool:
    """return true if the cells are adjacent (not diagonal)"""
    dx = cell_a.x - cell_b.x
    dy = cell_a.y - cell_b.y
    return abs(dx) + abs(dy) == 1

def cells_connected(from_cell: Cell, to_cell: Cell, direction: Direction) -> bool:
    # check from_cell and to_cell are adjacent coords
    if not adjacent(from_cell, to_cell):
        return False
    if direction.opposite() in to_cell.pipe.openings():
        return True
    return False


def connected_neighbors(grid: GridState, cell: Cell) -> list[Cell]:
    """All orthogonally adjacent cells that share a pipe connection with `cell`."""
    neighbors = []
    for direction in Direction:
        adj_x: int  = cell.x + direction.dir_x
        adj_y: int  = cell.y + direction.dir_y
        if not in_bounds(adj_x, adj_y):
            continue
        adj_cell: Cell = grid.grid[adj_y][adj_x]
        if cells_connected(cell, adj_cell, direction):
            neighbors.append(adj_cell)
    return neighbors
