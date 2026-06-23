"""Grid helpers: convert between cell coordinates and pixel coordinates.

A cell is identified by its (col, row) position in the grid.
"""

from game.config import CELL_SIZE


def cell_to_top_left_pixel(col: int, row: int) -> tuple[int, int]:
    """Return the top-left pixel (x, y) of the given cell."""
    return col * CELL_SIZE, row * CELL_SIZE


def pixel_to_cell(x: float, y: float) -> tuple[int, int]:
    """Return the (col, row) of the cell containing the given pixel."""
    return int(x // CELL_SIZE), int(y // CELL_SIZE)
