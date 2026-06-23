"""Grid helpers: convert between cell coordinates and pixel coordinates.

A cell is identified by its (col, row) position in the grid.
"""

from dataclasses import dataclass

from game.config import CELL_SIZE

# type cell which contains an x and y coordinate in the grid and a color value:
@dataclass
class Cell:
    x: int
    y: int
    color: tuple[int, int, int]

def cell_to_top_left_pixel(col: int, row: int) -> tuple[int, int]:
    """Return the top-left pixel (x, y) of the given cell."""
    return (col * CELL_SIZE, row * CELL_SIZE)


def pixel_to_cell(x: float, y: float) -> Cell:
    """Return the (col, row) of the cell containing the given pixel."""
    col = int(x // CELL_SIZE)
    row = int(y // CELL_SIZE)
    return Cell(x=col, y=row, color=(0, 0, 0))
