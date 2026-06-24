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

def cells_connected(cell_a: Cell, cell_b: Cell) -> bool:
    # check cell_a and cell_b are adjacent coords
    if not adjacent(cell_a, cell_b):
        return False
    return False #todo


def connected_neighbors(grid: GridState, cell: Cell) -> list[Cell]:
    """All orthogonally adjacent cells that share a pipe connection with `cell`."""
    neighbors = []
    for direction in Direction:
        # get the neighbor cell in that direction from the grid:
        adj_x = cell.x + direction.dir_x
        adj_y = cell.y + direction.dir_y
        if not in_bounds(adj_x, adj_y):
            continue
        neighbor = grid.grid[adj_y][adj_x]
        if cells_connected(cell, neighbor):
            neighbors.append(neighbor)
    return neighbors
