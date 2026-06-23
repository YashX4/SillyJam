# type cell which contains an x and y coordinate in the grid and a color value:
from dataclasses import dataclass


@dataclass
class Cell:
    x: int
    y: int
    color: tuple[int, int, int]